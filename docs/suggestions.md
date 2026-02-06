Small edits I’d still recommend, take it only if you think it is necessary

A. These are wording/strength issues, not core‑facts problems:

1. **PPIs (id: 5) – “never/always” language**

   - Current key_takeaway:
     - “CRITICAL: Never use Omeprazole with Clopidogrel. Always choose Pantoprazole for cardiac patients needing GI protection.” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/c42f4cef-c717-4795-aaf7-d48e20a10532/comparisons.json)
   - Safer, guideline‑compatible wording:
     - “Avoid omeprazole/esomeprazole with clopidogrel when alternatives exist; prefer pantoprazole or another weak CYP2C19 inhibitor (e.g., rabeprazole) for GI protection.” [acc](https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2019/06/27/14/22/2018-cholesterol-clinical-practice-guidelines)
   - Also in `evidence`, change “AHA/ACC/ESC: Pantoprazole preferred with DAPT” to something like:
     - “Cardiology guidance: Avoid omeprazole/esomeprazole with clopidogrel; use pantoprazole or other low‑CYP2C19‑inhibiting PPI.” [acc](https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2019/06/27/14/22/2018-cholesterol-clinical-practice-guidelines)
2. **Antiplatelets (id: 4) – absolutes**

   - Key_takeaway currently:
     - “DAPT is mandatory post-PCI… Always use Pantoprazole (not Omeprazole) for GI protection with Clopidogrel.” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/c42f4cef-c717-4795-aaf7-d48e20a10532/comparisons.json)
   - Suggest:
     - “DAPT is standard after PCI (duration tailored to ischaemic vs bleeding risk)… For GI protection with clopidogrel, avoid omeprazole/esomeprazole and prefer pantoprazole or a similar low‑interaction PPI.” [acc](https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2019/06/27/14/22/2018-cholesterol-clinical-practice-guidelines)
3. **Metformin “always first” phrasing (id: 8)**

   - `First-line Status` says “Metformin always starts first”; key_takeaway already mentions SGLT2i/GLP‑1 RA early in high‑risk patients. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC11196467/)
   - I’d slightly soften to:
     - “Metformin is standard first‑line for most T2DM; add or consider SGLT2i/GLP‑1 RA early in patients with ASCVD/HF/CKD when accessible.”
4. **Paracetamol CV risk line (id: 7)**

   - Under “Cardiovascular Risk” it says “Paracetamol: None”. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/c42f4cef-c717-4795-aaf7-d48e20a10532/comparisons.json)
   - Better: “Lowest relative CV risk; main limitation is hepatic toxicity at high or chronic doses” (you already hint at this in the GI row, so just align wording). [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10459253/table/pharmaceuticals-16-01084-t003/)

If you make those 3–4 text tweaks, the comparisons.json will be fully in line with all the corrections and nuance we’ve worked through.

B. For drug master Minor ESIC clean‑ups you can still do

A few entries are marked `not_verified` even though the ESIC PDF clearly lists them:

- **Aspirin**

  - ESIC has “Soluble Aspirin” tablets (acetyl salicylic acid 350 mg effervescent) under non‑opioid analgesics. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
  - You currently have `esic_status: "not_verified"` for aspirin 75 mg. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/e1348719-f39e-4bba-8d2c-45003ebb47ec/drugs_master.json)
  - Suggested change: set `esic_status: "yes"` with `esic_detail` like “Soluble aspirin 350 mg tablets listed; no 75 mg cardio‑dose in this schedule.”
- **Cefuroxime**

  - ESIC schedule includes cefuroxime injections (750 mg, 1.5 g) and cefuroxime+clavulanate tablets/injections. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
  - Your entry has `esic_status: "not_verified"`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/e1348719-f39e-4bba-8d2c-45003ebb47ec/drugs_master.json)
  - Suggested change:
    - If you want to be precise: `esic_status: "fdc_only"` for **oral** cefuroxime (because the tablet entries in the schedule are cefuroxime+clavulanate), and maybe a note that injections exist as plain cefuroxime.
    - For a simple flag: `esic_status: "yes"` with detail explaining both plain inj and FDC tablets are present.
- **Levofloxacin**

  - ESIC list clearly has a levofloxacin 500 mg injection. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
  - Your JSON marks it `not_verified`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/e1348719-f39e-4bba-8d2c-45003ebb47ec/drugs_master.json)
  - Suggested: `esic_status: "yes"` with `esic_detail`: “Levofloxacin 500 mg injection listed; no oral form in this schedule.”
- **Rabeprazole**

  - ESIC schedule has rabeprazole tablets and rabeprazole+mosapride cap FDC in the PPI section. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
  - Your entry says `esic_status: "not_verified"` but `esic_detail` already hints “ESIC schedule lists rabeprazole in PPI slot”. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/e1348719-f39e-4bba-8d2c-45003ebb47ec/drugs_master.json)
  - Suggested: just set `esic_status: "yes"` and keep/clarify the detail.

The remaining `not_verified` entries (doxycycline, ciprofloxacin, etc.) are fine to leave as‑is if you haven’t manually checked them against the ESIC PDF yet.

## Bottom line

- For the **35‑drug master list**, all **CGHS codes** and **ESIC statuses** for the drugs we focused on (pain, common antibiotics, diabetes, CV, PPIs, key respiratory drugs) align with the CGHS and ESIC documents and with our merged coverage table. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/60a02f71-8bde-4d77-ae1c-622eba874830/List_of_Medicines-MSO_Formulary_CGHS_As_on_CGHS_website_-_25.08.2014.pdf)
- To fully match reality, I’d just update ESIC status/details for **aspirin, cefuroxime, levofloxacin, and rabeprazole** from `not_verified` to accurate `yes/fdc_only` as above.

C. For interactions.json, the structure and most scenarios are good; only a few clinical‑nuance fixes are needed. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)

## Scenarios 1–4: OK with minor nuance

1. **Metformin + NSAIDs (Scenario 1)**

   - Mechanism and risk description are correct.
   - “Severity: high” is true **for CKD/elderly/dehydrated patients**; for a young diabetic with normal kidneys it is more “moderate”.
   - Your recommendation “Use paracetamol instead” is fine; no change needed. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
2. **Clopidogrel + Omeprazole (Scenario 2)**

   - Mechanism, risk, and pantoprazole as safer PPI are all correct.
   - The scenario text is fully aligned with what we discussed; no change needed. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
3. **ARBs + NSAIDs (Scenario 3)**

   - Description of afferent (NSAID) + efferent (ARB) effects and AKI risk is accurate; recommendation to prefer paracetamol or keep NSAID dose/length minimal is good. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
   - This can stay as‑is.
4. **Metformin + IV contrast (Scenario 4)**

   - Mechanism and idea of holding metformin around contrast are correct. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
   - Modern guidance is a bit more selective (based on eGFR and contrast route), but your “hold 48 h and check renal function” is a **safe conservative rule**.

## Scenario 5: Atorvastatin + Azithromycin

- Content is broadly safe but a bit over‑attributed to **QT from atorvastatin**.
- Suggested tweaks:
  - Emphasise that **QT risk is primarily from azithromycin**, and is clinically important in patients with baseline QT prolongation, electrolyte disturbance, or other QT‑prolonging drugs.
  - You can keep “severity: moderate”, but I’d add: “Interaction clinically important mainly in high‑risk patients; short 3–5 day courses are usually safe.” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
  - If you want one line on myopathy: “Unlike clarithromycin/erythromycin, azithromycin has minimal CYP3A4 effect, so statin myopathy risk is lower but still monitor if symptoms occur.”

## Scenario 6: “Salbutamol + Clopidogrel”

- The **scenario text** is correct: it’s really about “cardiac disease + high salbutamol use”, not clopidogrel specifically. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
- Only the `interaction_pairs` mapping is slightly misleading:
  - You currently map `salbutamol+clopidogrel` → this scenario. That suggests a mechanistic interaction with clopidogrel, which does not exist.
- Fix:
  - Either remove `salbutamol+clopidogrel` from `interaction_pairs`, or map more appropriate pairs like `salbutamol+digoxin`, `salbutamol+furosemide`, or `salbutamol+beta_blocker` depending on what your system supports.
  - Keep the scenario itself as a **clinical pattern**: “frequent SABA use in CAD/HF patient → tachycardia, hypokalaemia, arrhythmia risk; step up ICS (budesonide) to reduce SABA reliance.” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)

## Additional flag: Aspirin + Ibuprofen

- Mechanism and warning (“ibuprofen blocks aspirin’s antiplatelet effect”) are correct.
- The **recommendation** should change: right now it says “Use Paracetamol or Diclofenac instead.” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)
- For a cardiac patient on aspirin, diclofenac is a poor alternative (highest CV risk among common NSAIDs).
- Better wording:
  - “Avoid concurrent use in patients on low‑dose aspirin for cardioprotection. Prefer paracetamol. If an NSAID is essential, consider the lowest effective dose of an alternative (e.g., short‑course naproxen with PPI) and separate dosing from aspirin; avoid long‑term diclofenac in CVD patients.”

## Metformin + NSAIDs interaction_pairs

- Mapping `metformin+ibuprofen/diclofenac/aceclofenac` → Scenario 1 is fine, provided your UI makes it clear the risk is **much higher in CKD/elderly/volume‑depleted** patients and lower but still present in others. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/3fca57e6-185c-44ae-8a4c-8bd99e2daa2c/interactions.json)

If you implement these small edits (especially: remove “salbutamol+clopidogrel” as a direct pair and stop recommending diclofenac as an “instead” for aspirin patients), your interactions.json will be consistent with the rest of your updated clinical logic.

C. For reimbursement.json, the overall structure and logic are consistent with what we’ve established; only a couple of ESIC lines need tightening. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

## Scheme‑level blocks

- **PM‑JAY**: Package‑based, in‑hospital only, no OPD drug reimbursement — correct and consistent with HBP 2.0 docs. [ayushmanup](https://ayushmanup.in/assets/doc/FAQ-English.pdf)
- **CGHS**: Employer‑based, formulary‑driven, 1‑month dispensing (3 months for travel), chronic NCD coverage — matches CGHS/MSO/VMS documents. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/60a02f71-8bde-4d77-ae1c-622eba874830/List_of_Medicines-MSO_Formulary_CGHS_As_on_CGHS_website_-_25.08.2014.pdf)
- **ESIC**: “All listed drugs routinely available at ESIC facilities; emergency private prescriptions may be reimbursed” matches ESIC policy and the dispensary schedule you shared. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
- **Jan Aushadhi & private insurance**: Correctly described as low‑cost generics (no reimbursement) vs hospitalisation‑focused insurance with limited OPD drug cover. [thehealthmaster](https://thehealthmaster.com/wp-content/uploads/2023/01/Jan-Aushadhi-Medicine-list-2023.pdf)

No changes needed at scheme level.

## Category blocks vs our agreed coverage

### 1) Pain / fever / NSAIDs

Current ESIC line:

> “Paracetamol: YES… Ibuprofen: YES… Diclofenac: YES… Aceclofenac: NO. **Aspirin: not verified in schedule.**” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

From ESIC PDF, soluble aspirin 350 mg tablets are indeed listed under non‑opioid analgesics. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
Suggested tweak:

- Change aspirin part to:
  - “Aspirin: YES (soluble 350 mg analgesic tablets; no 75 mg cardio‑dose in this schedule).”

Everything else in this block matches our ESIC reading. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

### 2) Antibiotics

ESIC line:

> “Amoxicillin: FDC ONLY… Azithromycin: KIT ONLY… Cefixime: YES… Ceftriaxone: FDC ONLY… Metronidazole: NO. **Doxycycline/Levofloxacin/Ciprofloxacin: not verified.**” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

This is all correct relative to the ESIC schedule:

- Amox plain missing, only FDCs. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
- Azithro only in fluconazole+azithromycin+secnidazole kit. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
- Cefixime and ceftriaxone present exactly as described. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
- Metronidazole absent. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
- You truly haven’t checked doxy/levo/cipro line‑by‑line, so “not verified” is honest; optionally you can later update levofloxacin to “YES (500 mg injection)” once you confirm in the PDF. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)

### 3) Diabetes

ESIC line:

> “Metformin: FDC ONLY… Glimepiride: NO… Human Insulin: YES…” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

This exactly matches the ESIC schedule we parsed (DPP‑4 combos only for metformin, no glimepiride, multiple human insulin entries). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)

### 4) Cardiovascular

ESIC line:

> “Amlodipine: FDC ONLY… Losartan: YES… Telmisartan: FDC ONLY… Atorvastatin: YES… Rosuvastatin: YES… Clopidogrel: NO…” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

All of this is in line with the ESIC PDF: standalone losartan and both statins are present; amlodipine/telmisartan only in FDCs; clopidogrel absent (ticlopidine present instead). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)

### 5) Gastrointestinal (PPIs / ondansetron)

ESIC line:

> “Pantoprazole: NO. Omeprazole: NO. ESIC uses rabeprazole and esomeprazole in PPI slot. Ondansetron: YES (4mg tablets).” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

- ESIC PPI block indeed contains rabeprazole, rabeprazole+mosapride and esomeprazole, not pantoprazole/omeprazole. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
- Ondansetron 4 mg tablets are listed. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)
  This is correct and matches our earlier table.

### 6) Respiratory

ESIC line:

> “Salbutamol: YES… Budesonide: YES… Montelukast: FDC ONLY…” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/38884de1-4bf6-4a43-94c5-a3033c1c4e73/reimbursement.json)

This matches the ESIC schedule (salbutamol in multiple forms, budesonide inhaler/respules and combos, montelukast only in FDCs). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/50611236-e3c4-4fc5-b923-bcf4ab3b3131/drugschedule280912.pdf)

---

**Net:** reimbursement.json is aligned with our updates. The only concrete fix I’d make is to upgrade **aspirin** in the pain/fever block from “not verified” to “YES (soluble 350 mg analgesic tablets; no 75 mg cardio‑dose)” so it’s fully consistent with the ESIC PDF and your drugs_master.json. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/50564800/e1348719-f39e-4bba-8d2c-45003ebb47ec/drugs_master.json)
