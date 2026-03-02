"""
app.py — Flask entry point for MedRep AI backend.

Endpoints:
  POST /api/query         — main RAG chat (accepts {query, mode})
  GET  /api/drug/<name>   — structured drug lookup
  POST /api/interact      — drug-drug interaction check
  POST /api/transcribe    — speech-to-text (local Whisper)
  GET  /api/health        — health check
"""

import os
import json
import traceback
import tempfile

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from data_loader import load_all, get_drugs_master, get_interactions
from openfda_client import get_full_drug_data
from rag_engine import query as rag_query



# ── App Setup ──
app = Flask(__name__)
CORS(app)

# Load data into ChromaDB on startup
print("\n🏥 MedRep AI — Starting up...\n")
_chroma_client = load_all()


# ── Routes ──


@app.route("/", methods=["GET"])
def root():
    """Redirect to frontend or show API info."""
    return jsonify({
        "message": "MedRep AI Backend API",
        "tip": "Open http://localhost:5173 for the frontend UI",
        "endpoints": ["/api/health", "/api/query", "/api/drug/<name>", "/api/interact"],
    })


@app.route("/api/health", methods=["GET"])
def health():
    """Simple health check."""
    master = get_drugs_master()
    return jsonify({
        "status": "ok",
        "drugs_loaded": len(master["drugs"]),
        "llm_configured": bool(os.getenv("GROQ_API_KEY", "")),
    })


@app.route("/api/query", methods=["POST"])
def query_endpoint():
    """
    Main RAG endpoint. Accepts:
      { "query": "...", "mode": "doctor" | "patient" }
    Returns:
      { "response": "...", "intent": "...", "drugs": [...], "sources": [...] }
    """
    body = request.get_json(silent=True) or {}
    user_query = body.get("query", "").strip()
    mode = body.get("mode", "doctor")

    if not user_query:
        return jsonify({"error": "Missing 'query' field"}), 400

    if mode not in ("doctor", "patient"):
        mode = "doctor"

    try:
        result = rag_query(user_query, mode)
        return jsonify(result)
    except RuntimeError as e:
        # Gemini API key not set
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        traceback.print_exc()
        err_str = str(e).lower()
        if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str:
            return jsonify({
                "error": "The AI model is temporarily rate-limited. Please wait a moment and try again.",
                "retry": True,
            }), 429
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route("/api/drug/<name>", methods=["GET"])
def drug_lookup(name):
    """
    Structured drug lookup by generic name or ID.
    Returns master data + OpenFDA label.
    """
    master = get_drugs_master()
    name_lower = name.lower().strip()

    # Find by ID or generic_name
    drug = None
    for d in master["drugs"]:
        if d["id"] == name_lower or d["generic_name"].lower() == name_lower:
            drug = d
            break

    # Try brand name match
    if not drug:
        for d in master["drugs"]:
            if name_lower in [b.lower() for b in d.get("brands", [])]:
                drug = d
                break

    if not drug:
        return jsonify({"error": f"Drug '{name}' not found"}), 404

    # Fetch OpenFDA data
    openfda_name = drug.get("openfda_name", drug["generic_name"])
    fda = get_full_drug_data(openfda_name)

    return jsonify({
        "drug": drug,
        "openfda": fda,
        "sources": ["drugs_master.json", "OpenFDA"] if fda["has_label"] else ["drugs_master.json"],
    })


@app.route("/api/interact", methods=["POST"])
def interact_endpoint():
    """
    Check for drug-drug interaction.
    Accepts: { "drug_a": "metformin", "drug_b": "ibuprofen" }
    Returns matching scenario or "no known interaction".
    """
    body = request.get_json(silent=True) or {}
    drug_a = body.get("drug_a", "").strip().lower()
    drug_b = body.get("drug_b", "").strip().lower()

    if not drug_a or not drug_b:
        return jsonify({"error": "Missing drug_a or drug_b"}), 400

    data = get_interactions()

    # Check scenarios
    for sc in data["scenarios"]:
        a = sc["drug_a"]["id"] if isinstance(sc["drug_a"], dict) else sc["drug_a"]
        b = sc["drug_b"]["id"] if isinstance(sc["drug_b"], dict) else sc["drug_b"]
        if (a == drug_a and b == drug_b) or (a == drug_b and b == drug_a):
            return jsonify(sc)

    # Check interaction_pairs
    for key in [f"{drug_a}+{drug_b}", f"{drug_b}+{drug_a}"]:
        val = data.get("interaction_pairs", {}).get(key)
        if val and val != 0:
            # Resolve scenario ref
            ref = val.get("scenario_ref") if isinstance(val, dict) else None
            if ref:
                for sc in data["scenarios"]:
                    if sc["id"] == ref:
                        return jsonify({**sc, "pair_match": val})
            return jsonify(val if isinstance(val, dict) else {"scenario_ref": val, "pair_key": key})

    # Check additional_flags
    for key in [f"{drug_a}+{drug_b}", f"{drug_b}+{drug_a}"]:
        flag = data.get("additional_flags", {}).get(key)
        if flag and flag != 0:
            return jsonify(flag)

    return jsonify({
        "noInteraction": True,
        "message": f"No pre-authored interaction found for {drug_a} + {drug_b}. "
                   "The LLM can still check OpenFDA data via the /api/query endpoint.",
    })


@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files: return jsonify({"error": "No audio file"}), 400
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            request.files["audio"].save(tmp.name)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as a: res = client.audio.transcriptions.create(model="whisper-large-v3", file=a)
        os.unlink(tmp_path)
        return jsonify({"text": res.text})
    except Exception as e: return jsonify({"error": str(e)}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500


# ── Entry Point ──
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 MedRep AI backend running on http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)




