These prompts are very solid and aligned with your architecture and safety goals; they’re good enough to ship with just a few targeted tweaks.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/19247944-e99e-4e00-afa6-f2acdd3e6308/ARCHITECTURE.md)]

I’ll highlight what’s strong, then suggest small but important additions.

---

## What’s already strong

* **Clear personas:** Doctor prompt is explicitly for licensed HCPs; patient prompt is clearly non‑diagnostic and explanatory.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/19247944-e99e-4e00-afa6-f2acdd3e6308/ARCHITECTURE.md)]
* **Hard constraint to RAG context:** “ONLY use facts… NEVER generate from general knowledge” matches your RAG design and will drastically reduce hallucinations.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/19247944-e99e-4e00-afa6-f2acdd3e6308/ARCHITECTURE.md)]
* **Structured sections:** Indication, dosing, safety, interactions, reimbursement, pricing – this maps exactly to what HCPs want and to your JSON fields.[drugs_master.json**+1**](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/e1348719-f39e-4bba-8d2c-45003ebb47ec/drugs_master.json)
* **Interaction & comparison emphasis:** Rules 11–13 in SYSTEM_DOCTOR force the model to surface interaction alerts and comparison data when present – this leverages `interactions.json` and `comparisons.json` properly.[interactions.json**+1**](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
* **No drug‑count leakage / unsupported drug handling:** Rule 10 is exactly what you need to avoid the “I only know 31 drugs” problem.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/e1348719-f39e-4bba-8d2c-45003ebb47ec/drugs_master.json)]
* **Patient safety:** SYSTEM_PATIENT forbids diagnosis, treatment recommendation, and dosing, and pushes price explanations + “ask your doctor” – very good.

---

## Suggested tweaks for SYSTEM_DOCTOR

You’re 90% there. I’d add/adjust three things:

1. **Explicitly block symptom‑only prescribing**
   Add a rule (around 3 or 10):

   > “If the user only describes symptoms without naming a drug or giving a working diagnosis (e.g., ‘I have fever and dry cough’), do not propose a specific medicine. Instead, explain that this tool is for drug‑specific information for HCPs, ask for the drug name and context (diagnosis, comorbidities), and recommend that patients see a doctor for diagnosis.”
   >

   This encodes the behaviour you’ve been manually crafting for fever/cold questions.
2. **Clarify “information, not prescription”**
   Right after “Your role mirrors that of a pharmaceutical medical information specialist…”, add:

   > “You do not diagnose or prescribe. You summarise labeled information, guideline‑consistent considerations, and database insights to support, not replace, the clinician’s judgment.”
   >

   This keeps you firmly on the med‑info / digital rep side, not decision support that chooses regimens.
3. **Tighten rule 13 (condition + drug)**
   Rule 13 is powerful but slightly vague. Rephrase to:

   > “When the user mentions a condition (e.g., ‘cardiac issues’, ‘diabetes’) **and** a specific drug, check the interaction scenarios for that drug (e.g., clopidogrel + omeprazole; metformin + NSAIDs; ARBs + NSAIDs) and surface any relevant alerts or safer alternatives.”
   >

   That nudges the model to tie to the actual IDs you have in `interactions.json` (metformin, losartan, clopidogrel, omeprazole, etc.) rather than hallucinating condition‑based logic.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)]

Optionally, add one line about brevity:

> “Prefer concise summaries; default to 2–4 short paragraphs and bullet lists rather than long essays, unless the user explicitly asks for detailed explanation.”

This keeps answers readable in a clinic context.

---

## Suggested tweaks for SYSTEM_PATIENT

Mostly great; just a couple of safety clarifications:

1. **Reinforce that it’s not for choosing medicines**
   Rule 3 already says “NEVER diagnose or recommend which medicine to take.” I’d add:

   > “If a user asks which medicine to take or describes their symptoms (e.g., ‘I have fever and cough, what should I take?’), explain that you cannot recommend treatment and that they must consult a doctor. You may mention that doctors commonly use certain medicines for such problems only in very general, educational terms, without telling the user what they personally should take.”
   >
2. **Scope Jan Aushadhi explanation**
   In rule 6, you might slightly rephrase:

   > “When pricing data is available, explain that ‘Jan Aushadhi’ is a government‑run generic pharmacy scheme in India, and show how much cheaper the Jan Aushadhi version is compared to a popular brand, using the exact prices from context.”
   >

   That ties directly to what’s in your CSV and JSON.[reimbursement.json**+1**](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)
3. **Encourage linking back to doctor mode**
   Add a final rule:

   > “If a user appears to be a healthcare professional asking clinical questions, gently suggest that they use the professional (doctor) version of MedRep AI for more detailed, technical information.”
   >

This keeps your boundary between patient education and HCP content clear.

---

## Implementation tip

Given these prompts and your architecture:

* Use **intent classification** before choosing SYSTEM_DOCTOR vs SYSTEM_PATIENT (e.g., route obvious symptom/patient‑style queries to PATIENT mode that then says “see your doctor”).[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/19247944-e99e-4e00-afa6-f2acdd3e6308/ARCHITECTURE.md)]
* In doctor mode, always pass in the **exact slices of JSON** relevant to the detected drugs + any matched interaction/comparison entries, so the “ONLY use provided context” constraint doesn’t cripple the model.

With these small additions, your prompts are fully aligned with your RAG stack and the “digital medical rep” track, and they should behave well both with judges and with a real HCP reviewer.
