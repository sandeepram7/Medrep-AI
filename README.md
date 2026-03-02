---
title: Medic API
emoji: 💊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---
# 💊 MedRep AI - Digital Medical Representative

> An AI-powered chatbot delivering instant, accurate drug information to Indian healthcare professionals — with cited sources, interaction safety checks, and reimbursement guidance.

![Status](https://img.shields.io/badge/Status-In%20Development-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🎯 What It Does

MedRep AI answers three types of questions Indian doctors face daily:

1. **Scientific** — What is this drug's mechanism of action? How does it differ from alternatives?
2. **Administrative** — Is this covered under PM-JAY / CGHS / ESIC / private insurance? What's the Jan Aushadhi price?
3. **Safety** — Can I prescribe this to a diabetic patient already on Metformin? What are the conflicts?

Every answer comes with a **source citation** displayed in a proof panel.

---

## 💡 Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Drug Info + MOA** | Mechanism of action, indications, dosing, adverse reactions (via OpenFDA) |
| ⚖️ **Drug Comparison** | How does Atorvastatin differ from Rosuvastatin? Evidence-based comparison |
| ⚠️ **Conflict Detection** | Cross-category interaction alerts (e.g., Metformin + Ibuprofen in diabetic patients) |
| 📋 **Reimbursement Guide** | PM-JAY, CGHS, ESIC, and private insurance coverage per drug |
| 💰 **Savings Calculator** | Jan Aushadhi generic price vs branded price with % savings |
| 🔍 **Proof Panel** | Every claim shows its source — OpenFDA, Jan Aushadhi list, scheme documents |
| 👤 **Patient View** | One-click toggle to see the same info in simple, non-medical language |

---

## 💊 Drug Coverage

35 essential medicines across 6 categories — India's most-prescribed OPD drugs:

| Category | Drugs |
|----------|-------|
| Pain / Fever | Paracetamol, Ibuprofen, Diclofenac, Aceclofenac, Aspirin |
| Antibiotics | Amoxicillin, Amox+Clav, Azithromycin, Cefixime, Ceftriaxone, Cefuroxime, Metronidazole, Doxycycline, Levofloxacin/Ciprofloxacin |
| Diabetes | Metformin, Glimepiride, Insulin |
| Cardiovascular | Amlodipine, Losartan, Telmisartan, Atorvastatin, Rosuvastatin, Clopidogrel, Aspirin+Clopidogrel |
| Gastric / GI | Pantoprazole, Omeprazole, Rabeprazole, Ondansetron |
| Respiratory | Salbutamol, Montelukast+Levocetirizine, Budesonide |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Flask (Python) |
| RAG Pipeline | LangChain + ChromaDB |
| LLM | Google Gemini API (free) |
| Embeddings | sentence-transformers (GPU) |
| Clinical Data | OpenFDA API (live) |
| Pricing Data | Jan Aushadhi CSV (local) |

---

## ⚠️ Disclaimer

**For informational purposes only.** Does not constitute medical advice. Always verify drug information with official sources and consult qualified healthcare professionals before making clinical decisions.

---

## 📄 License

This project is licensed under the MIT License.

