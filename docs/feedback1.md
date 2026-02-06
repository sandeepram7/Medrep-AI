Great track. If you’re building a **digital medical representative** for **20–25 drugs**, the right way to scope this is to work **backwards from what an HCP will actually ask**—not from what pharma PDFs contain.

Below is a **practical, HCP-driven question framework**. If your system can answer **these questions reliably**, your chatbot will feel genuinely useful (and defensible in a hackathon).

---

## 1️⃣ Drug Identity & Positioning

**“What is this drug and where does it fit?”**

**Typical HCP questions**

* What is this drug indicated for?
* Is it first-line / second-line / add-on therapy?
* Which patient population is it approved for?
* Is this on-label or off-label?

**You should have**

* Brand name + generic name
* Therapeutic area & indication(s)
* Line of therapy
* Patient eligibility criteria (age, disease stage, biomarkers if applicable)
* FDA / EMA / CDSCO approval status
* Launch year

---

## 2️⃣ Mechanism of Action (MOA) – **High Priority**

**“How does this drug work, really?”**

**Typical HCP questions**

* What is the mechanism of action?
* What pathway does it target?
* How is this different from other drugs in the same class?
* Why does this work better (or differently) than existing therapies?

**You should have**

* Clear MOA explanation (lay + technical version)
* Drug class (e.g., monoclonal antibody, small molecule, kinase inhibitor)
* Target receptor / enzyme / pathway
* Differentiation vs competitors (mechanism-level, not marketing)
* Visual / stepwise MOA description (even if text-only)

---

## 3️⃣ Clinical Evidence & Efficacy

**“Why should I trust this drug?”**

**Typical HCP questions**

* What trials support this drug?
* What were the key endpoints?
* How effective is it compared to standard of care?
* In which patients did it perform best?

**You should have**

* Pivotal trials (name, phase, population)
* Key endpoints and outcomes
* Summary of efficacy results
* Comparator used in trials
* Head-to-head data (if available)
* Real-world evidence (if public)

> ⚠️ Keep it **fact-based**, not promotional.

---

## 4️⃣ Safety Profile & Tolerability

**“Is it safe for my patient?”**

**Typical HCP questions**

* What are the common side effects?
* What are the serious adverse events?
* Any black box warnings?
* How does safety compare to alternatives?

**You should have**

* Common adverse events (frequency)
* Serious / rare adverse events
* Contraindications
* Boxed warnings (if any)
* Drug-drug interactions
* Monitoring requirements

---

## 5️⃣ Dosing & Administration

**“How do I actually prescribe this?”**

**Typical HCP questions**

* What is the recommended dose?
* Oral or injectable?
* Frequency?
* Any renal/hepatic dose adjustments?
* Can it be self-administered?

**You should have**

* Standard dosing
* Route of administration
* Titration schedule (if any)
* Dose adjustments
* Missed dose guidance
* Storage requirements

---

## 6️⃣ Comparison & Differentiation (Critical for Adoption)

**“Why this drug over another?”**

**Typical HCP questions**

* How does this compare to Drug X?
* Is it better tolerated?
* Does it work faster?
* Is adherence better?

**You should have**

* Key competitors
* Differentiation across:

  * MOA
  * Efficacy
  * Safety
  * Dosing convenience
* Where it wins / where it doesn’t
* Use-case positioning (e.g., refractory patients)

---

## 7️⃣ Reimbursement & Access (Administrative Goldmine)

**“Can my patient actually get this?”**

**Typical HCP questions**

* Is this covered by insurance?
* Difference between private vs public plans?
* What is the prior authorization process?
* Is there copay support?
* What if insurance denies it?

**You should have**

* Coverage status (public vs private)
* Typical prior authorization requirements
* Reimbursement codes (if public)
* Step-therapy requirements
* Appeals process overview

---

## 8️⃣ Patient Support Programs

**“How do I help my patient afford or manage this?”**

**Typical HCP questions**

* Are there copay assistance programs?
* Free drug programs?
* Bridge programs while approval is pending?
* Who do I contact?

**You should have**

* Patient assistance program details
* Eligibility criteria
* Enrollment process
* Contact information
* Turnaround timelines

---

## 9️⃣ Practical Prescribing FAQs

**“Edge cases I see in clinic”**

**Typical HCP questions**

* Can I use this with Drug Y?
* What if the patient has comorbidities?
* What if they switch from another therapy?
* When should I stop treatment?

**You should have**

* Switching guidance
* Combination therapy rules
* Use in special populations
* Discontinuation criteria

---

## 1️⃣0️⃣ Regulatory & Labeling (Guardrails)

**“What can I legally say/do?”**

**You should have**

* Official label (structured)
* On-label vs off-label flags
* Safety disclaimers
* Source citation for every claim

---

## 🔑 For a Hackathon: Minimum Viable Coverage (MVP)

If time is tight, **prioritize these 6**:

1. Indication & positioning
2. MOA + differentiation
3. Clinical evidence summary
4. Safety profile
5. Dosing & administration
6. Reimbursement + support programs

If your chatbot nails **these**, it will feel like a real digital rep.

---

## 🧠 Pro Tip (Judges Love This)

Structure your data so the agent can:

* Answer **“why”**, not just **“what”**
* Switch tone: **scientific ↔ operational**
* Cite sources for every answer
* Say **“I don’t have evidence for that”** when needed

---

If you want, next I can help you:

* Design a **drug knowledge schema (JSON / tables)**
* Create **example HCP questions** for demo
* Define **what NOT to answer (compliance guardrails)**
* Architect the **RAG + citation flow**

Just tell me where you want to go next.
