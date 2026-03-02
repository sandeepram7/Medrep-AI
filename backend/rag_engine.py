"""
rag_engine.py — Core RAG pipeline: query → classify → retrieve → augment → generate.

Pipeline:
  1. Classify user intent & extract drug names
  2. Handle symptom-only queries (no LLM needed)
  3. Retrieve from ChromaDB (all 6 collections) + OpenFDA live API
  4. Inject raw JSON records & patient-info for exact grounding
  5. Build augmented prompt with all context
  6. Send to OpenAI llama-3.1-8b-instant with mode-aware system prompt
  7. Consolidate sources & return structured response
"""

import os
import json
import re
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from data_loader import get_chroma_client, get_drugs_master, get_interactions
from openfda_client import get_full_drug_data

load_dotenv()

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds between retries on rate-limit

# ── LLM Setup ──
_llm = None


def get_llm():
    global _llm
    if _llm is None:
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not set."
            )
        model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        _llm = ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0.3,
            max_tokens=2048,
        )
        print(f"  ✓ LLM initialized: {model_name}")
    return _llm


# ── System Prompts ──
SYSTEM_DOCTOR = """You are MedRep AI, a digital medical representative for licensed healthcare professionals (HCPs) in India.
You provide evidence-based, non-promotional drug information drawn from a curated database of high-volume primary care molecules.

Your role mirrors that of a pharmaceutical medical information specialist: factual, structured, and grounded in approved product information.
You do not diagnose or prescribe. You summarise labeled information, guideline-consistent considerations, and database insights to support, not replace, the clinician's judgment.

RESPONSE RULES:
1. ONLY use facts, numbers, and clinical claims that appear in the LOCAL DATABASE CONTEXT or OPENFDA CLINICAL DATA sections provided with each query.
2. If the provided context does not contain information about something, say: "This is not covered in our current database. I recommend consulting the product's approved prescribing information or contacting the manufacturer."
3. NEVER generate drug information, mechanisms of action, dosing, or safety data from your general training knowledge. Stick strictly to the provided context.
4. Cite your data source inline: (Source: drugs_master.json), (Source: jan_aushadhi_prices.csv), (Source: interactions.json), (Source: comparisons.json), (Source: reimbursement.json), (Source: OpenFDA label).
5. Structure answers in clear clinical sections as appropriate: Indication, Dosing, Safety & Contraindications, Drug Interactions, Reimbursement (CGHS/ESIC/PM-JAY), Pricing (Brand vs Jan Aushadhi).
6. When comparing drugs, present a balanced, evidence-based view. Reference specific comparison parameters from the database.
7. For pricing, always show both Brand MRP and Jan Aushadhi generic price with savings percentage when available in context.
8. Speak in a professional, concise, clinical tone — like a medical science liaison, not a chatbot.
9. At the end of your response, suggest 1-2 related follow-up areas the HCP might want to explore (e.g., "Would you like to see interaction data?" or "I can also provide the CGHS coverage details.").
10. Never say how many drugs are in the database. If asked about an unsupported drug, say: "I don't currently have detailed information on that molecule in our database, but I can help with common primary care drugs like paracetamol, amoxicillin, metformin, atorvastatin, etc. Which specific drug are you interested in?"
18. DOMAIN BOUNDARIES: If the user asks about something completely outside medicines/healthcare (food, recipes, poems, general knowledge), do NOT say "This is not available in our database." Instead say something like: "I'm a drug information tool for healthcare professionals. I can't help with that topic, but I can answer questions about specific medicines, their safety, interactions, prices, and coverage."
11. IMPORTANT: If the context contains INTERACTION ALERT data, you MUST prominently surface it in your response with a clear warning. Do not bury interaction warnings — lead with them when relevant to the user's question.
12. If the context contains comparison data for the drug(s) mentioned, proactively reference it — e.g., "Our comparison data shows..." or "Compared to alternatives..."
13. When the user mentions a condition (e.g., 'cardiac issues', 'diabetes') AND a specific drug, check the interaction scenarios for that drug (e.g., clopidogrel + omeprazole, metformin + NSAIDs, ARBs + NSAIDs) and surface any relevant alerts or safer alternatives from context.
14. Only list sources in the source panel that you actually used in generating the answer. Do not include sources you didn't reference.
15. Paraphrase clinical information in your own words rather than copying label text verbatim. For example, instead of reproducing FDA label wording, summarize the key clinical points concisely.
16. If the user only describes symptoms without naming a drug or giving a working diagnosis (e.g., 'I have fever and dry cough'), do not propose a specific medicine. Explain that this tool provides drug-specific information for HCPs, ask for the drug name and clinical context (diagnosis, comorbidities), and recommend that patients see a doctor for diagnosis.
17. Prefer concise summaries; default to 2-4 short paragraphs and bullet lists rather than long essays, unless the user explicitly asks for detailed explanation.
19. OUTPUT FORMAT: Always respond in **Markdown prose** (headings, bullet lists, bold, etc.). NEVER respond with raw JSON, XML, or code blocks containing structured data. Your answer must be readable human text, not a data structure.
"""

SYSTEM_PATIENT = """You are MedRep AI, a friendly health information assistant for patients in India.
You explain medicines in simple, everyday language that any patient can understand.
You help patients understand their prescribed medicines better — what they do, how to take them safely, what to watch out for, and how to save money using government schemes.

RESPONSE RULES:
1. ONLY use facts from the LOCAL DATABASE CONTEXT or OPENFDA CLINICAL DATA provided below. Never add information from your general knowledge.
2. If the context doesn't cover a specific medicine, say: "I don't have details on that medicine right now. Please ask your doctor or pharmacist."
11. DOMAIN BOUNDARIES: If the user asks about something completely outside medicines/healthcare (food, recipes, poems, general knowledge), do NOT say "I don't have that information." Instead say something like: "I'm a medicine information assistant. I can't help with that topic, but I can explain your medicines, their safety, and how to save money on them."
3. NEVER diagnose conditions or recommend which medicine to take. If a user asks which medicine to take or describes symptoms (e.g., 'I have fever and cough, what should I take?'), explain that you cannot recommend treatment and that they must consult a doctor. You may mention that doctors commonly use certain medicines for such problems only in very general, educational terms, without telling the user what they personally should take.
4. Avoid medical jargon. Use analogies and simple words. When the context contains a PATIENT-FRIENDLY INFO section, prefer that wording over the technical mechanism.
5. Do NOT give specific dosing instructions — say "Take exactly as your doctor prescribed."
6. For pricing, explain that 'Jan Aushadhi' is a government-run generic pharmacy scheme in India, and show how much cheaper the Jan Aushadhi version is compared to a popular brand, using the exact prices from context.
7. Keep answers warm, reassuring, and easy to scan. Use short paragraphs and bullet points.
8. Structure your response with clear sections when appropriate: What this medicine does, How to take it safely, Important warnings, Cost savings.
9. End with a simple suggestion like: "Want to know about side effects?" or "I can also tell you where to find this medicine cheaper."
10. If a user appears to be a healthcare professional asking clinical questions, gently suggest that they use the professional (doctor) version of MedRep AI for more detailed, technical information.
12. OUTPUT FORMAT: Always respond in **Markdown prose** (headings, bullet lists, bold, etc.). NEVER respond with raw JSON, XML, or code blocks containing structured data. Your answer must be readable human text, not a data structure.
"""


# ── Drug Name Index (for extraction) ──
_drug_index = None


def _get_drug_index():
    """Build a lookup: lowercase generic_name → drug dict."""
    global _drug_index
    if _drug_index is None:
        master = get_drugs_master()
        _drug_index = {}
        for drug in master["drugs"]:
            _drug_index[drug["generic_name"].lower()] = drug
            _drug_index[drug["id"]] = drug
            # Also index brand names
            for brand in drug.get("brands", []):
                _drug_index[brand.lower()] = drug
    return _drug_index


def extract_drug_names(query: str) -> list[dict]:
    """Extract known drug references from the user's query."""
    index = _get_drug_index()
    query_lower = query.lower()
    found = {}

    # Sort keys by length (longest first) to match multi-word names first
    for key in sorted(index.keys(), key=len, reverse=True):
        if key in query_lower and index[key]["id"] not in found:
            found[index[key]["id"]] = index[key]

    return list(found.values())


def classify_intent(query: str) -> str:
    """Simple keyword-based intent classification."""
    q = query.lower()
    drugs_found = extract_drug_names(query)

    # Symptom-based queries (no specific drug mentioned) → refuse
    symptom_words = ["fever", "cough", "headache", "pain", "cold", "vomit", "nausea",
                     "diarrhea", "infection", "swelling", "rash", "itch", "dizzy",
                     "breathless", "chest pain", "stomach", "throat", "fatigue",
                     "weakness", "bleeding", "what should i take", "what medicine",
                     "suggest medicine", "recommend", "which medicine", "what can i take"]
    if any(w in q for w in symptom_words) and not drugs_found:
        return "symptom"

    interaction_words = ["interact", "conflict", "combine", "together", "mix",
                         "safe to take", "safe", "adding", "can i take", "can i use",
                         "can i consume", "is it ok", "along with", "on top of"]
    if any(w in q for w in interaction_words) and len(drugs_found) >= 2:
        return "interaction"

    compare_words = ["compare", "vs", "versus", "better", "difference", "which one", "prefer"]
    if any(w in q for w in compare_words):
        return "comparison"

    reimburse_words = ["reimburse", "insurance", "cover", "cghs", "esic", "pm-jay", "pmjay", "jan aushadhi", "scheme", "claim"]
    if any(w in q for w in reimburse_words):
        return "reimbursement"

    price_words = ["price", "cost", "cheap", "expensive", "mrp", "generic", "save", "saving", "afford"]
    if any(w in q for w in price_words):
        return "pricing"

    # If no drugs found AND no medical/drug-related keywords → off-topic
    if not drugs_found:
        medical_words = [
            "drug", "medicine", "tablet", "capsule", "dose", "dosage", "mg",
            "prescription", "side effect", "adverse", "contraindication",
            "doctor", "patient", "treatment", "therapy", "antibiotic",
            "painkiller", "anti-inflammatory", "antihypertensive", "antidiabetic",
            "pharma", "clinical", "indication", "mechanism", "pharmacology",
            "generic", "brand", "formulation", "injection", "syrup", "ointment",
            "health", "medical", "hospital", "clinic", "surgery",
            "blood pressure", "sugar", "cholesterol", "diabetes", "hypertension",
            "cardiac", "renal", "hepatic", "liver", "kidney",
            "cghs", "esic", "pm-jay", "jan aushadhi", "reimbursement",
        ]
        if not any(w in q for w in medical_words):
            return "off_topic"

    return "drug_info"


# ── ChromaDB Retrieval ──
def retrieve_context(query: str, intent: str, drug_names: list[dict]) -> dict:
    """
    Query relevant ChromaDB collections based on intent and extracted drugs.
    Returns a dict of context pieces.
    """
    client = get_chroma_client()
    context = {"local": [], "openfda": [], "sources": []}

    drug_ids = [d["id"] for d in drug_names]

    # Always search drug_info for mentioned drugs
    if drug_names:
        drug_col = client.get_collection("drug_info")
        for drug in drug_names:
            try:
                result = drug_col.get(ids=[drug["id"]])
                if result["documents"]:
                    context["local"].append(result["documents"][0])
                    context["sources"].append(f"drugs_master.json ({drug['generic_name']})")
            except Exception:
                pass

        # ALWAYS also pull pricing data for mentioned drugs
        try:
            price_col = client.get_collection("pricing")
            for drug in drug_names:
                price_results = price_col.query(
                    query_texts=[drug["generic_name"]],
                    n_results=3,
                )
                for doc in price_results["documents"][0]:
                    if doc not in context["local"]:
                        context["local"].append(doc)
                if price_results["documents"][0]:
                    context["sources"].append(f"jan_aushadhi_prices.csv ({drug['generic_name']})")
        except Exception:
            pass

        # ALWAYS also pull reimbursement data for mentioned drugs
        try:
            reimb_col = client.get_collection("reimbursement")
            for drug in drug_names:
                reimb_results = reimb_col.query(
                    query_texts=[drug["generic_name"]],
                    n_results=2,
                )
                for doc in reimb_results["documents"][0]:
                    if doc not in context["local"]:
                        context["local"].append(doc)
                if reimb_results["documents"][0]:
                    context["sources"].append(f"reimbursement.json ({drug['generic_name']})")
        except Exception:
            pass

        # ALWAYS pull interaction data for mentioned drugs
        try:
            int_col = client.get_collection("interactions")
            for drug in drug_names:
                int_results = int_col.query(
                    query_texts=[drug["generic_name"]],
                    n_results=2,
                )
                for doc in int_results["documents"][0]:
                    if doc not in context["local"]:
                        context["local"].append(doc)
                if int_results["documents"][0]:
                    context["sources"].append(f"interactions.json ({drug['generic_name']})")
        except Exception:
            pass

        # ALWAYS pull comparison data for mentioned drugs
        try:
            comp_col = client.get_collection("comparisons")
            for drug in drug_names:
                comp_results = comp_col.query(
                    query_texts=[drug["generic_name"]],
                    n_results=2,
                )
                for doc in comp_results["documents"][0]:
                    if doc not in context["local"]:
                        context["local"].append(doc)
                if comp_results["documents"][0]:
                    context["sources"].append(f"comparisons.json ({drug['generic_name']})")
        except Exception:
            pass

        # ALWAYS pull patient_info (mechanism + patient summary) for mentioned drugs
        try:
            pi_col = client.get_collection("patient_info")
            for drug in drug_names:
                try:
                    pi_result = pi_col.get(ids=[drug["id"]])
                    if pi_result["documents"]:
                        context["local"].append(pi_result["documents"][0])
                        context["sources"].append(f"patient_info.json ({drug['generic_name']})")
                except Exception:
                    # Try query-based fallback
                    pi_results = pi_col.query(
                        query_texts=[drug["generic_name"]],
                        n_results=1,
                    )
                    for doc in pi_results["documents"][0]:
                        if doc not in context["local"]:
                            context["local"].append(doc)
                    if pi_results["documents"][0]:
                        context["sources"].append(f"patient_info.json ({drug['generic_name']})")
        except Exception:
            pass

        # Direct interaction pair lookup for ALL drug pairs
        if len(drug_ids) >= 2:
            from itertools import combinations
            for id_a, id_b in combinations(drug_ids, 2):
                interaction_data = _lookup_interaction_pair(id_a, id_b)
                if interaction_data:
                    context["local"].insert(0, f"INTERACTION ALERT ({id_a} + {id_b}):\n{json.dumps(interaction_data, indent=2)}")
                    if "interactions.json (direct pair)" not in context["sources"]:
                        context["sources"].append("interactions.json (direct pair)")

    # Intent-specific retrieval
    if intent == "interaction":
        try:
            int_col = client.get_collection("interactions")
            results = int_col.query(query_texts=[query], n_results=3)
            for doc in results["documents"][0]:
                if doc not in context["local"]:
                    context["local"].append(doc)
            context["sources"].append("interactions.json")
        except Exception:
            pass

    elif intent == "comparison":
        try:
            comp_col = client.get_collection("comparisons")
            results = comp_col.query(query_texts=[query], n_results=3)
            for doc in results["documents"][0]:
                context["local"].append(doc)
            context["sources"].append("comparisons.json")
        except Exception:
            pass

    elif intent == "reimbursement":
        try:
            reimb_col = client.get_collection("reimbursement")
            results = reimb_col.query(query_texts=[query], n_results=4)
            for doc in results["documents"][0]:
                context["local"].append(doc)
            context["sources"].append("reimbursement.json")
        except Exception:
            pass

    elif intent == "pricing":
        try:
            price_col = client.get_collection("pricing")
            results = price_col.query(query_texts=[query], n_results=5)
            for doc in results["documents"][0]:
                context["local"].append(doc)
            context["sources"].append("jan_aushadhi_prices.csv")
        except Exception:
            pass

    else:  # drug_info — broad search
        for collection_name in ["comparisons", "reimbursement", "pricing"]:
            try:
                col = client.get_collection(collection_name)
                results = col.query(query_texts=[query], n_results=2)
                for doc in results["documents"][0]:
                    context["local"].append(doc)
            except Exception:
                pass

    # OpenFDA live API enrichment for mentioned drugs
    for drug in drug_names:
        openfda_name = drug.get("openfda_name", drug["generic_name"])
        try:
            fda_data = get_full_drug_data(openfda_name)
            if fda_data["has_label"]:
                label = fda_data["label"]
                relevant = {k: v for k, v in label.items() if v and k != "source"}
                context["openfda"].append(json.dumps(relevant, indent=2)[:3000])
                context["sources"].append(f"OpenFDA ({openfda_name})")
                print(f"  ✓ OpenFDA label fetched for {openfda_name}")
            else:
                print(f"  ⚠ No OpenFDA label found for {openfda_name}")
            if fda_data["has_adverse_data"]:
                ae_text = ", ".join(
                    f"{ae['reaction']} ({ae['count']})"
                    for ae in fda_data["top_adverse_events"][:5]
                )
                context["openfda"].append(
                    f"Top adverse events for {openfda_name}: {ae_text}"
                )
                print(f"  ✓ OpenFDA adverse events fetched for {openfda_name}")
        except Exception as e:
            print(f"  ✗ OpenFDA fetch failed for {openfda_name}: {e}")

    return context


def _lookup_interaction_pair(drug_a: str, drug_b: str) -> dict | None:
    """Direct lookup in interactions.json for a specific pair."""
    data = get_interactions()

    # Check scenarios
    for sc in data["scenarios"]:
        a = sc["drug_a"]["id"] if isinstance(sc["drug_a"], dict) else sc["drug_a"]
        b = sc["drug_b"]["id"] if isinstance(sc["drug_b"], dict) else sc["drug_b"]
        if (a == drug_a and b == drug_b) or (a == drug_b and b == drug_a):
            return sc

    # Check interaction_pairs
    for key_combo in [f"{drug_a}+{drug_b}", f"{drug_b}+{drug_a}"]:
        val = data.get("interaction_pairs", {}).get(key_combo)
        if val and val != 0:
            # Resolve the linked scenario
            ref = val.get("scenario_ref") if isinstance(val, dict) else None
            if ref:
                for sc in data["scenarios"]:
                    if sc["id"] == ref:
                        return {**sc, "pair_specific": val}
            return val if isinstance(val, dict) else {"scenario_ref": val}

    # Check additional_flags
    for key_combo in [f"{drug_a}+{drug_b}", f"{drug_b}+{drug_a}"]:
        flag = data.get("additional_flags", {}).get(key_combo)
        if flag and flag != 0:
            return flag

    return None


# ── Main Query Function ──

def _json_to_markdown(obj: dict) -> str:
    """Convert a JSON response from the LLM into readable Markdown."""
    parts = []

    if obj.get("summary"):
        parts.append(obj["summary"])

    if obj.get("interactions"):
        parts.append("\n### Interaction Alerts\n")
        for ix in obj["interactions"]:
            severity = ix.get("severity", "")
            drugs = ", ".join(ix.get("drugs_involved", []))
            badge = f"**{severity}**" if severity else ""
            parts.append(f"- {badge} ({drugs}): {ix.get('description', '')}")
            if ix.get("recommendation"):
                parts.append(f"  - *Recommendation:* {ix['recommendation']}")

    if obj.get("drug_information"):
        parts.append("\n### Drug Information\n")
        if isinstance(obj["drug_information"], dict):
            for k, v in obj["drug_information"].items():
                parts.append(f"- **{k.replace('_', ' ').title()}:** {v}")
        elif isinstance(obj["drug_information"], list):
            for item in obj["drug_information"]:
                parts.append(f"- {item}")

    if obj.get("safety_warnings"):
        parts.append("\n### Safety Warnings\n")
        for w in obj["safety_warnings"]:
            parts.append(f"- ⚠️ {w}")

    if obj.get("recommendations"):
        parts.append("\n### Recommendations\n")
        if isinstance(obj["recommendations"], list):
            for r in obj["recommendations"]:
                parts.append(f"- {r}")
        else:
            parts.append(str(obj["recommendations"]))

    if obj.get("reimbursement"):
        parts.append("\n### Reimbursement\n")
        if isinstance(obj["reimbursement"], dict):
            for k, v in obj["reimbursement"].items():
                parts.append(f"- **{k.replace('_', ' ').title()}:** {v}")
        elif isinstance(obj["reimbursement"], list):
            for r in obj["reimbursement"]:
                parts.append(f"- {r}")

    if obj.get("sources"):
        parts.append("\n---\n*Sources:*")
        for s in obj["sources"]:
            if isinstance(s, dict):
                parts.append(f"- {s.get('database', '')}: {s.get('snippet', '')}")
            else:
                parts.append(f"- {s}")

    if obj.get("disclaimer"):
        parts.append(f"\n> {obj['disclaimer']}")

    # Fallback: if we extracted almost nothing, dump all non-null keys
    if len(parts) <= 1:
        for k, v in obj.items():
            if v and k not in ("summary", "disclaimer"):
                parts.append(f"**{k.replace('_', ' ').title()}:** {v}")

    return "\n".join(parts)


def query(user_query: str, mode: str = "doctor") -> dict:
    """
    Full RAG pipeline: classify → retrieve → augment → generate.

    Args:
        user_query: The user's natural language question.
        mode: "doctor" or "patient" — changes the system prompt tone.

    Returns:
        {
            "response": str,     # LLM-generated answer
            "intent": str,       # classified intent
            "drugs": [str],      # drug names found
            "sources": [str],    # data sources used
        }
    """
    # 1. Classify
    intent = classify_intent(user_query)
    drugs = extract_drug_names(user_query)
    drug_names_list = [d["generic_name"] for d in drugs]

    # 2. Handle off-topic & symptom queries immediately (no LLM call needed)
    if intent == "off_topic":
        if mode == "patient":
            response_text = (
                "I'm a **medicine information assistant** — I help you understand your prescribed medicines "
                "in simple language. I'm not designed for general topics like that.\n\n"
                "Here's what I **can** help you with:\n"
                "- 💊 **Explain your medicine** — what it does and how it works\n"
                "- ⚠️ **Safety tips** — warnings and things to watch out for\n"
                "- 💰 **Save money** — cheaper options at Jan Aushadhi stores\n"
                "- 🏥 **Government coverage** — PM-JAY, CGHS, ESIC schemes\n\n"
                "Try asking something like: *\"Tell me about Paracetamol\"* or "
                "*\"How can I save on my diabetes medicine?\"*"
            )
        else:
            response_text = (
                "I'm a **drug information tool for healthcare professionals**, focused on medicines, "
                "interactions, pricing, and reimbursement for common primary-care drugs. "
                "I'm not designed for general topics outside this scope.\n\n"
                "I can help you with:\n"
                "- **Drug profiles** — indications, dosing, safety, contraindications\n"
                "- **Drug interactions** — clinically significant pairs from our database\n"
                "- **Pricing** — Brand MRP vs Jan Aushadhi generic prices\n"
                "- **Reimbursement** — CGHS, ESIC, PM-JAY coverage details\n\n"
                "Try: *\"Tell me about Atorvastatin\"* or *\"Compare Losartan vs Telmisartan\"*"
            )
        return {
            "response": response_text,
            "intent": intent,
            "drugs": [],
            "sources": ["system"],
        }

    if intent == "symptom":
        if mode == "patient":
            response_text = (
                "I understand you're not feeling well, and I'm sorry to hear that. "
                "However, I'm a medicine information assistant — I can help you understand "
                "a medicine your doctor has prescribed, but **I cannot tell you which medicine to take**.\n\n"
                "**Please visit your doctor** for a proper diagnosis. Only a doctor can examine you "
                "and decide the right treatment.\n\n"
                "Once your doctor prescribes a medicine, I can help you with:\n"
                "- 💊 **What the medicine does** — explained in simple language\n"
                "- ⚠️ **How to take it safely** — important warnings and tips\n"
                "- 💰 **How to save money** — cheaper options at Jan Aushadhi stores\n"
                "- 🏥 **Government scheme coverage** — PM-JAY, CGHS, ESIC\n\n"
                "For example, try asking: *\"Tell me about Paracetamol\"* or *\"How much can I save on Metformin?\"*"
            )
        else:
            response_text = (
                "I'm designed for healthcare professionals and provide drug-specific, evidence-based information. "
                "I cannot safely recommend treatment based on symptoms alone.\n\n"
                "In clinical practice, doctors commonly consider paracetamol for fever relief, "
                "but the right choice and dose depend on age, liver function, pregnancy status, "
                "and other medications the patient is taking.\n\n"
                "**If you're an HCP**, tell me which drug you're considering and I can provide:\n"
                "- Safety profile and contraindications\n"
                "- Drug interactions with the patient's current medications\n"
                "- Jan Aushadhi pricing and savings\n"
                "- CGHS/ESIC/PM-JAY coverage details\n\n"
                "For example: *\"Adult with viral fever on Metformin — is Paracetamol safe? "
                "Show dosing limits, interactions, and Jan Aushadhi price.\"*"
            )
        return {
            "response": response_text,
            "intent": intent,
            "drugs": [],
            "sources": ["system"],
        }

    # 3. Retrieve
    context = retrieve_context(user_query, intent, drugs)

    # 4. Inject raw JSON data for mentioned drugs (exact data, not just embeddings)
    if drugs:
        master = get_drugs_master()
        for drug_entry in drugs:
            for master_drug in master["drugs"]:
                if master_drug["id"] == drug_entry["id"]:
                    raw_json = json.dumps(master_drug, indent=2)
                    header = f"\n=== RAW DATABASE RECORD for {drug_entry['generic_name']} ===\n"
                    context["local"].insert(0, header + raw_json)
                    break

        # Inject patient_info (mechanism + patient-friendly summary) for mentioned drugs
        try:
            from data_loader import get_patient_info
            pi_data = get_patient_info()
            for drug_entry in drugs:
                for pi_drug in pi_data["drugs"]:
                    if pi_drug["id"] == drug_entry["id"]:
                        if mode == "patient":
                            pi_block = (
                                f"\n=== PATIENT-FRIENDLY INFO for {drug_entry['generic_name']} ===\n"
                                f"How it works (simple): {pi_drug['patient_summary']}\n"
                                f"Mechanism (technical): {pi_drug['mechanism']}\n"
                            )
                        else:
                            pi_block = (
                                f"\n=== PHARMACOLOGY for {drug_entry['generic_name']} ===\n"
                                f"Mechanism of Action: {pi_drug['mechanism']}\n"
                                f"Patient-Friendly Summary: {pi_drug['patient_summary']}\n"
                            )
                        context["local"].insert(0, pi_block)
                        break
        except Exception:
            pass

    # 5. Build augmented prompt
    system_prompt = SYSTEM_DOCTOR if mode == "doctor" else SYSTEM_PATIENT

    context_block = ""
    if context["local"]:
        context_block += "=== LOCAL DATABASE CONTEXT (from our JSON/CSV files) ===\n"
        context_block += "\n---\n".join(context["local"][:10])
        context_block += "\n\n"

    if context["openfda"]:
        context_block += "=== OPENFDA CLINICAL DATA (from FDA API) ===\n"
        context_block += "\n---\n".join(context["openfda"][:3])
        context_block += "\n\n"

    if not context["local"] and not context["openfda"]:
        context_block = "=== NO DATA FOUND IN OUR DATABASE ===\nNo matching records found for this query.\n\n"

    augmented_query = f"""IMPORTANT INSTRUCTIONS:
1. ONLY use the data provided below to answer the question. Do NOT add any information from your training data.
2. Every fact you state must come from the context below. Cite the source.
3. If the data below does not contain an answer, say "This information is not available in our database."
4. Do NOT fabricate drug mechanisms, dosing, safety info, or any clinical claims not found below.
5. CRITICAL: Respond in readable Markdown text with headings and bullets. NEVER output JSON, code blocks, or structured data objects.

{context_block}
=== USER QUESTION ===
{user_query}"""

    # 6. Generate (with retry on rate-limit)
    llm = get_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=augmented_query),
    ]

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = llm.invoke(messages)
            break  # success — proceed to step 7
        except Exception as e:
            last_error = e
            err_str = str(e).lower()
            if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str:
                wait = RETRY_DELAY * (attempt + 1)
                print(f"  ⏳ Rate-limited, retrying in {wait}s (attempt {attempt+1}/{MAX_RETRIES})...")
                time.sleep(wait)
            else:
                raise  # Non-rate-limit error, don't retry
    else:
        raise last_error  # All retries exhausted

    # 7. Safety net: if LLM returned JSON instead of prose, convert it
    answer_text = response.content
    stripped = answer_text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            json_obj = json.loads(stripped)
            answer_text = _json_to_markdown(json_obj)
        except json.JSONDecodeError:
            pass  # Not valid JSON, keep as-is
    elif stripped.startswith("```"):
        # Strip code fence wrapper if the LLM wrapped its response in one
        lines = stripped.split("\n")
        if lines[0].startswith("```") and lines[-1].strip() == "```":
            inner = "\n".join(lines[1:-1]).strip()
            if inner.startswith("{"):
                try:
                    json_obj = json.loads(inner)
                    answer_text = _json_to_markdown(json_obj)
                except json.JSONDecodeError:
                    answer_text = inner

    # 8. Consolidate sources & return structured response
    raw_sources = list(set(context["sources"]))
    consolidated = {}
    for s in raw_sources:
        base = s.split(" (")[0] if " (" in s else s
        if base not in consolidated:
            consolidated[base] = []
        if " (" in s:
            drug = s.split(" (")[1].rstrip(")")
            consolidated[base].append(drug)
    clean_sources = []
    for base, drugs_list in consolidated.items():
        if drugs_list:
            clean_sources.append(f"{base} ({', '.join(sorted(set(drugs_list)))})")
        else:
            clean_sources.append(base)

    return {
        "response": answer_text,
        "intent": intent,
        "drugs": drug_names_list,
        "sources": clean_sources,
    }




