"""
openfda_client.py — Fetch live drug data from the US FDA's public API.

Endpoints used:
  /drug/label.json  — prescribing info (MOA, dosing, interactions, warnings)
  /drug/event.json  — real-world adverse event report counts

Note: OpenFDA uses US names. Paracetamol → "acetaminophen", Salbutamol → "albuterol sulfate".
The openfda_name field in drugs_master.json handles this mapping.
"""

import requests
from functools import lru_cache

BASE = "https://api.fda.gov/drug"
TIMEOUT = 4  # seconds — keep low to avoid slow responses


@lru_cache(maxsize=64)
def get_drug_label(openfda_name: str) -> dict | None:
    """
    Fetch the most recent drug label for a given generic name.
    Returns a dict with extracted fields, or None on failure.
    """
    try:
        r = requests.get(
            f"{BASE}/label.json",
            params={
                "search": f'openfda.generic_name:"{openfda_name}"',
                "limit": 1,
            },
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            return None

        results = r.json().get("results", [])
        if not results:
            return None

        label = results[0]

        def _first(field):
            """Extract first item from label array field."""
            val = label.get(field, [])
            if isinstance(val, list) and val:
                return val[0]
            return val if val else None

        return {
            "source": "OpenFDA",
            "generic_name": openfda_name,
            "indications_and_usage": _first("indications_and_usage"),
            "mechanism_of_action": _first("mechanism_of_action"),
            "dosage_and_administration": _first("dosage_and_administration"),
            "contraindications": _first("contraindications"),
            "drug_interactions": _first("drug_interactions"),
            "adverse_reactions": _first("adverse_reactions"),
            "warnings": _first("warnings"),
            "pregnancy": _first("pregnancy"),
        }
    except (requests.RequestException, ValueError, KeyError):
        return None


@lru_cache(maxsize=64)
def get_adverse_events(openfda_name: str, top_n: int = 10) -> list[dict]:
    """
    Fetch top adverse event reaction counts for a drug.
    Returns a list of {"reaction": str, "count": int}.
    """
    try:
        r = requests.get(
            f"{BASE}/event.json",
            params={
                "search": f'patient.drug.openfda.generic_name:"{openfda_name}"',
                "count": "patient.reaction.reactionmeddrapt.exact",
            },
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            return []

        results = r.json().get("results", [])
        return [
            {"reaction": item["term"], "count": item["count"]}
            for item in results[:top_n]
        ]
    except (requests.RequestException, ValueError, KeyError):
        return []


def get_full_drug_data(openfda_name: str) -> dict:
    """
    Combine label + adverse events into one response.
    """
    label = get_drug_label(openfda_name)
    adverse = get_adverse_events(openfda_name)

    return {
        "label": label,
        "top_adverse_events": adverse,
        "openfda_name": openfda_name,
        "has_label": label is not None,
        "has_adverse_data": len(adverse) > 0,
    }
