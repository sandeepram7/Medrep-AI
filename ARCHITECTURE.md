# MedRep AI — Technical Architecture

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | React + Vite + Tailwind CSS | Fast, modern, component-based |
| Backend | Flask (Python) | Team familiarity |
| RAG Pipeline | LangChain + ChromaDB | Standard RAG tooling, well-documented |
| LLM | OpenAI GPT-4o-mini | High quality, fast, cost-effective |
| Embeddings | ONNX MiniLM-L6 (local via ChromaDB) | No GPU required, runs locally |
| Clinical Data | OpenFDA API (optional live enrichment) | Free, used to augment local data |
| Pricing Data | Jan Aushadhi CSV (local) | 94 pre-collected drug variants |
| Reimbursement | Structured JSON (local) | Converted from dataset_paln.md YAML |

---

## Data Flow

```
Doctor types a question
         │
         ▼
┌─────────────────────────────┐
│  QUERY PROCESSOR            │
│  • Extract drug name(s)     │
│  • Detect intent:           │
│    - drug info / MOA        │
│    - interaction check      │
│    - reimbursement query    │
│    - price comparison       │
│  • Create embedding vector  │
└─────────────────────────────┘
         │
    ┌────┴─────────────────┐
    ▼                      ▼
┌──────────────┐  ┌───────────────────┐
│ ChromaDB     │  │ OpenFDA API       │
│ (Local Data) │  │ (Live Clinical)   │
│              │  │                   │
│ • Jan Aus.   │  │ • /drug/label.json│
│   prices     │  │   → MOA, dosing,  │
│ • Reimburse- │  │     interactions, │
│   ment rules │  │     warnings,     │
│ • Drug       │  │     adverse rxns  │
│   comparisons│  │                   │
│ • Interaction│  │ • /drug/event.json│
│   scenarios  │  │   → real-world    │
│              │  │     adverse counts│
└──────────────┘  └───────────────────┘
    │                      │
    └────┬─────────────────┘
         ▼
┌─────────────────────────────┐
│  CONTEXT AGGREGATION        │
│  Combine local + live data  │
│  Attach source citations    │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  OpenAI GPT-4o-mini LLM     │
│  System prompt + context    │
│  + user query               │
│  → Structured response      │
│  → Source list for proof     │
│    panel                    │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  RESPONSE TO UI             │
│  • Drug info (doctor view)  │
│  • Drug info (patient view) │
│  • Source citations (proof) │
│  • Savings card (if prices) │
│  • Interaction alerts       │
└─────────────────────────────┘
```

---

## API Endpoints (Flask)

| Method | Endpoint | Purpose | Input | Output |
|--------|----------|---------|-------|--------|
| POST | `/api/query` | Main RAG query | `{ question, mode: "doctor"\|"patient" }` | `{ answer, sources[], drug_card?, alerts[] }` |
| GET | `/api/drug/<name>` | Structured drug card | Drug name in URL | `{ info, prices, reimbursement, interactions }` |
| POST | `/api/interact` | Drug conflict check | `{ drugs: ["metformin", "ibuprofen"] }` | `{ conflicts[], severity, recommendation }` |
| GET | `/api/health` | Health check | None | `{ status: "ok" }` |

---

## Project Structure

```
MediThon/
│
├── data/                          # All data files
│   ├── drugs_master.json          # 31 curated drugs with pricing, brands & scheme mappings
│   ├── jan_aushadhi_prices.csv    # 94 variant prices (existing CSV, renamed)
│   ├── reimbursement.json         # PM-JAY, CGHS, ESIC, Private rules per drug
│   ├── interactions.json          # Cross-category conflict scenarios
│   └── comparisons.json          # Drug-vs-drug comparison notes
│
├── backend/                       # Flask Backend
│   ├── app.py                     # Flask app entry point + routes
│   ├── rag_engine.py              # LangChain + ChromaDB pipeline
│   ├── openfda_client.py          # OpenFDA API integration
│   ├── data_loader.py             # Load JSONs into ChromaDB
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # API keys (OPENAI_API_KEY)
│
├── frontend/                      # React Frontend
│   ├── src/
│   │   ├── App.jsx                # Router (Chat + Drug Explorer pages)
│   │   ├── pages/
│   │   │   ├── ChatPage.jsx       # Main chat interface with HCP/Patient mode
│   │   │   └── DrugExplorer.jsx   # Browsable drug catalog with search/filter
│   │   ├── components/
│   │   │   ├── Layout.jsx         # Sidebar + page layout
│   │   │   └── Sidebar.jsx        # Navigation sidebar
│   │   └── services/
│   │       └── api.js             # API client (sendQuery, getDrug, etc.)
│   └── package.json
│
├── chroma_db/                     # Vector database (auto-generated, not committed)
│
├── docs/                          # Planning & reference docs
│   └── archive/                   # Non-indexed reference material
│
├── README.md
├── LICENSE
└── top_essential_drugs_variants.csv
```

---

## ChromaDB Collections

| Collection | Contents | Source |
|------------|----------|--------|
| `drug_info` | Drug names, categories, OpenFDA query mappings | drugs_master.json |
| `pricing` | Jan Aushadhi prices + brand prices per drug | CSV + brand price data |
| `reimbursement` | Scheme rules per drug bucket | reimbursement.json |
| `comparisons` | Drug-vs-drug differentiation notes | comparisons.json |
| `interactions` | Cross-category conflict scenarios | interactions.json |

---

## OpenFDA Queries (Optional Live Enrichment)

OpenFDA provides supplementary clinical data for our drugs. These calls are **optional** — the system works fully with local data alone, and OpenFDA enriches responses when available:

**Drug Label (main info):**
```
GET https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1
```
Returns: indications, MOA, dosing, contraindications, drug_interactions, adverse_reactions, warnings

**Adverse Event Counts:**
```
GET https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:{drug_name}&count=patient.reaction.reactionmeddrapt.exact
```
Returns: Top adverse reactions with real-world report counts

**Note:** Paracetamol → use "acetaminophen" for OpenFDA (US name)

---

## LLM System Prompts

**Doctor Mode (HCP-facing):**
```
You are MedRep AI, a digital medical representative for licensed healthcare professionals in India.
You provide evidence-based, non-promotional drug information drawn from a curated database.
ONLY use facts from the provided LOCAL DATABASE CONTEXT and OPENFDA CLINICAL DATA.
NEVER generate drug info from training data. Cite sources inline.
Do not diagnose or recommend treatment based solely on symptoms — require a working diagnosis or specific drug.
Structure: Indication, Dosing, Safety, Interactions, Reimbursement, Price.
Suggest follow-up areas the HCP might want to explore.
```

**Patient Mode (educational, shown by HCPs to patients):**
```
You are MedRep AI explaining a medicine in simple, everyday language.
ONLY use facts from the provided context. Never add from training data.
Avoid all medical jargon. Do NOT give dosing instructions.
For pricing, explain Jan Aushadhi savings simply. Keep answers warm and concise.
```

## Key Design Decisions

- **Symptom-based queries**: The system detects symptom-only questions (fever, cough, etc. without a drug name) and responds with a professional pivot — guiding HCPs to specify a drug or working diagnosis, rather than refusing bluntly.
- **`has_manual_comparisons` / `has_manual_interactions` flags**: Each drug in `drugs_master.json` carries these boolean flags. The RAG engine uses them to avoid hallucinating comparisons/interactions when no curated data exists.
- **Archived docs are NOT indexed**: Only `data/*.json` and `data/*.csv` are ingested into ChromaDB. All markdown reference docs in `docs/archive/` are excluded from the RAG corpus.
- **Follow-up suggestions**: After each response, the UI shows clickable follow-up chips (pricing, coverage, interactions, comparisons) to guide HCPs deeper — mimicking how a real med rep proactively offers related information.
