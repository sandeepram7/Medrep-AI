"""
data_loader.py — Load all JSON/CSV data files into ChromaDB collections.

Collections created:
  drug_info       — 31 master drug records (one doc per drug)
  comparisons     — 9 comparison tables (one doc per table)
  interactions    — 6 interaction scenarios + pair index
  reimbursement   — 6 drug-category coverage buckets + 5 scheme defs
  pricing         — 94 Jan Aushadhi price rows (one doc per row)
  patient_info    — 31 mechanism-of-action + patient-friendly summaries
"""

import json
import csv
import os
from pathlib import Path

import chromadb
from chromadb.config import Settings

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"


def _load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_csv_rows(filename):
    rows = []
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def get_chroma_client():
    """Persistent ChromaDB client stored at project-root/chroma_db/."""
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )


def load_drug_info(client):
    """Load drugs_master.json → drug_info collection."""
    col = client.get_or_create_collection("drug_info")
    if col.count() > 0:
        return col  # already loaded

    master = _load_json("drugs_master.json")
    docs, ids, metas = [], [], []

    for drug in master["drugs"]:
        # Build a rich text doc for embedding similarity search
        text_parts = [
            f"Drug: {drug['generic_name']}",
            f"Category: {drug['category']}",
            f"Strength: {drug.get('primary_strength', 'N/A')}",
            f"Brands: {', '.join(drug.get('brands', []))}",
        ]
        if drug.get("brand_mrp"):
            text_parts.append(
                f"Brand MRP: ₹{drug['brand_mrp']['mrp']} ({drug['brand_mrp']['name']}, {drug['brand_mrp']['pack']})"
            )
        if drug.get("jan_aushadhi_mrp"):
            text_parts.append(
                f"Jan Aushadhi: ₹{drug['jan_aushadhi_mrp']['mrp']} ({drug['jan_aushadhi_mrp']['variant']}, {drug['jan_aushadhi_mrp']['pack']})"
            )
        if drug.get("savings_percent"):
            text_parts.append(f"Savings: {drug['savings_percent']}%")
        if drug.get("cghs_codes"):
            text_parts.append(f"CGHS codes: {', '.join(drug['cghs_codes'])}")
        if drug.get("cghs_entry"):
            text_parts.append(f"CGHS entry: {drug['cghs_entry']}")
        if drug.get("esic_status"):
            text_parts.append(f"ESIC status: {drug['esic_status']}")
        if drug.get("esic_detail"):
            text_parts.append(f"ESIC detail: {drug['esic_detail']}")

        doc = "\n".join(text_parts)
        docs.append(doc)
        ids.append(drug["id"])
        metas.append({
            "id": drug["id"],
            "generic_name": drug["generic_name"],
            "category": drug["category"],
            "openfda_name": drug.get("openfda_name", drug["generic_name"]),
            "has_manual_comparisons": str(drug.get("has_manual_comparisons", False)),
            "has_manual_interactions": str(drug.get("has_manual_interactions", False)),
        })

    col.add(documents=docs, ids=ids, metadatas=metas)
    print(f"  ✓ drug_info: {col.count()} documents")
    return col


def load_comparisons(client):
    """Load comparisons.json → comparisons collection."""
    col = client.get_or_create_collection("comparisons")
    if col.count() > 0:
        return col

    data = _load_json("comparisons.json")
    docs, ids, metas = [], [], []

    for comp in data["comparisons"]:
        # Build searchable text from comparison table
        text_parts = [
            f"Comparison: {comp['title']}",
            f"Category: {comp['category']}",
            f"Drugs compared: {', '.join(comp['drugs'])}",
        ]
        for param in comp.get("parameters", []):
            text_parts.append(f"\n{param.get('name', '')}:")
            for drug_id, value in param.get("values", {}).items():
                text_parts.append(f"  {drug_id}: {value}")
        if comp.get("key_takeaway"):
            text_parts.append(f"\nKey takeaway: {comp['key_takeaway']}")
        if comp.get("evidence"):
            text_parts.append(
                f"Evidence: {', '.join(e.get('name', str(e)) if isinstance(e, dict) else str(e) for e in comp['evidence'])}"
            )

        docs.append("\n".join(text_parts))
        ids.append(str(comp["id"]))
        metas.append({
            "id": str(comp["id"]),
            "title": comp["title"],
            "category": comp["category"],
            "drugs": ", ".join(comp["drugs"]),
        })

    col.add(documents=docs, ids=ids, metadatas=metas)
    print(f"  ✓ comparisons: {col.count()} documents")
    return col


def load_interactions(client):
    """Load interactions.json → interactions collection."""
    col = client.get_or_create_collection("interactions")
    if col.count() > 0:
        return col

    data = _load_json("interactions.json")
    docs, ids, metas = [], [], []

    for sc in data["scenarios"]:
        drug_a = (sc["drug_a"]["id"] if isinstance(sc["drug_a"], dict) else sc["drug_a"]) or ""
        drug_b = (sc["drug_b"]["id"] if isinstance(sc["drug_b"], dict) else sc["drug_b"]) or ""
        drug_a_name = sc["drug_a"]["name"] if isinstance(sc["drug_a"], dict) else str(sc["drug_a"])
        drug_b_name = sc["drug_b"]["name"] if isinstance(sc["drug_b"], dict) else str(sc["drug_b"])

        text_parts = [
            f"Interaction: {sc['title']}",
            f"Drugs: {drug_a_name} + {drug_b_name}",
            f"Severity: {sc.get('severity', 'N/A')}",
            f"Risk: {sc.get('risk', '')}",
            f"Mechanism: {sc.get('mechanism', '')}",
            f"Recommendation: {sc.get('recommendation', '')}",
        ]
        safer = sc.get("safer_alternative")
        if safer and isinstance(safer, dict):
            text_parts.append(f"Safer alternative: {safer.get('name', '')}")
        elif safer:
            text_parts.append(f"Safer alternative: {safer}")

        docs.append("\n".join(text_parts))
        ids.append(str(sc["id"]))
        metas.append({
            "id": str(sc["id"]),
            "drug_a": drug_a,
            "drug_b": drug_b,
            "severity": sc.get("severity") or "",
        })

    # Also index the pair lookup as a single doc for retrieval
    pair_lines = []
    for key, val in data.get("interaction_pairs", {}).items():
        if val == 0:
            continue
        scenario_ref = val.get("scenario_ref", "") if isinstance(val, dict) else str(val)
        pair_lines.append(f"{key} → scenario {scenario_ref}")

    if pair_lines:
        docs.append("Interaction pair index:\n" + "\n".join(pair_lines))
        ids.append("pair_index")
        metas.append({"id": "pair_index", "drug_a": "", "drug_b": "", "severity": ""})

    col.add(documents=docs, ids=ids, metadatas=metas)
    print(f"  ✓ interactions: {col.count()} documents")
    return col


def load_reimbursement(client):
    """Load reimbursement.json → reimbursement collection."""
    col = client.get_or_create_collection("reimbursement")
    if col.count() > 0:
        return col

    data = _load_json("reimbursement.json")
    docs, ids, metas = [], [], []

    # Scheme definitions
    for scheme_id, scheme in data.get("schemes", {}).items():
        text_parts = [
            f"Scheme: {scheme.get('name', scheme_id)}",
            f"Full name: {scheme.get('full_name', '')}",
            f"Type: {scheme.get('type', '')}",
            f"Coverage model: {scheme.get('drug_coverage_model', '')}",
        ]
        if scheme.get("key_rules"):
            text_parts.append("Key rules:")
            for rule in scheme["key_rules"]:
                text_parts.append(f"  • {rule}")

        docs.append("\n".join(text_parts))
        ids.append(f"scheme_{scheme_id}")
        metas.append({"id": scheme_id, "type": "scheme"})

    # Drug coverage buckets
    for category, bucket in data.get("drug_coverage", {}).items():
        text_parts = [
            f"Category: {category}",
            f"Drugs: {', '.join(bucket.get('drugs', []))}",
        ]
        for scheme_id, coverage_text in bucket.get("coverage", {}).items():
            text_parts.append(f"\n{scheme_id}: {coverage_text}")

        docs.append("\n".join(text_parts))
        ids.append(f"coverage_{category}")
        metas.append({"id": category, "type": "coverage", "drugs": ", ".join(bucket.get("drugs", []))})

    col.add(documents=docs, ids=ids, metadatas=metas)
    print(f"  ✓ reimbursement: {col.count()} documents")
    return col


def load_pricing(client):
    """Load jan_aushadhi_prices.csv → pricing collection."""
    col = client.get_or_create_collection("pricing")
    if col.count() > 0:
        return col

    rows = _load_csv_rows("jan_aushadhi_prices.csv")
    docs, ids, metas = [], [], []

    for i, row in enumerate(rows):
        # Build text from CSV columns
        parts = [f"{k}: {v}" for k, v in row.items() if v]
        docs.append("\n".join(parts))
        ids.append(f"price_{i}")
        metas.append({"row_index": str(i)})

    col.add(documents=docs, ids=ids, metadatas=metas)
    print(f"  ✓ pricing: {col.count()} documents")
    return col


def load_patient_info(client):
    """Load patient_info.json → patient_info collection."""
    col = client.get_or_create_collection("patient_info")
    if col.count() > 0:
        return col

    data = _load_json("patient_info.json")
    docs, ids, metas = [], [], []

    for drug in data["drugs"]:
        # Combine mechanism + patient summary into one searchable doc
        text_parts = [
            f"Drug: {drug['generic_name']} ({drug['id']})",
            f"Category: {drug['category']}",
            f"Mechanism of Action: {drug['mechanism']}",
            f"Patient-Friendly Summary: {drug['patient_summary']}",
        ]
        docs.append("\n".join(text_parts))
        ids.append(str(drug["id"]))
        metas.append({
            "generic_name": drug["generic_name"],
            "category": drug["category"],
            "type": "patient_info",
        })

    col.add(documents=docs, ids=ids, metadatas=metas)
    print(f"  ✓ patient_info: {col.count()} documents")
    return col


def load_all():
    """Load all data into ChromaDB. Idempotent — skips if already loaded."""
    print("Loading data into ChromaDB...")
    client = get_chroma_client()
    load_drug_info(client)
    load_comparisons(client)
    load_interactions(client)
    load_reimbursement(client)
    load_pricing(client)
    load_patient_info(client)
    print("All collections loaded.\n")
    return client


# Direct data access (no ChromaDB, for structured endpoints)
def get_drugs_master():
    return _load_json("drugs_master.json")


def get_interactions():
    return _load_json("interactions.json")


def get_comparisons():
    return _load_json("comparisons.json")


def get_reimbursement():
    return _load_json("reimbursement.json")


def get_patient_info():
    return _load_json("patient_info.json")


if __name__ == "__main__":
    load_all()
