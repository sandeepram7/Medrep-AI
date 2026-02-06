# Our plan now:

i am giving u the list of drugs we will focus on

'''

1) Pain / Fever / Anti-inflammatory (Very Common)

Paracetamol

Ibuprofen

Diclofenac

Aceclofenac + Paracetamol

Aspirin (75/150 mg) (cardiac + antiplatelet use)

2) Antibiotics (Very High Priority)

Amoxicillin

Amoxicillin + Clavulanic Acid

Azithromycin

Cefixime

Ceftriaxone

Cefuroxime

Metronidazole

Doxycycline

Levofloxacin / Ciprofloxacin (either one is essential to cover)

3) Diabetes (Extremely High Priority)

Metformin

Glimepiride

Insulin (Regular / Human Mixtard types)

4) Cardiovascular (Most Prescribed Category)

Amlodipine

Losartan

Telmisartan

Atorvastatin

Rosuvastatin

Clopidogrel

Aspirin + Clopidogrel combination (very common cardiac)

5) Gastric / Acid reflux (Very High Usage)

Pantoprazole

Omeprazole / Rabeprazole (any one is essential)

Ondansetron (anti-vomiting, extremely common)

6) Respiratory (Common OPD prescriptions)

Salbutamol

Montelukast + Levocetirizine

Budesonide (inhaler / respules)

'''

now make a structured txt file  in detail for  administrative queries (e.g., details about reimbursement support programs and their difference for private insurance vs public plans) with the links from where u got the data

# What response we got from search for this



Below is a **structured text file (YAML-style)** focused on administrative / reimbursement aspects for your India‑specific use case. It is organized by:

* National/public schemes (PM‑JAY, CGHS, ESIC)
* Private insurance behavior
* Low‑cost generic access (Jan Aushadhi)
* Then, for each of your drugs, how these rules typically apply in practice.

You can save this as `reimbursement_india.txt` or `.yml` and parse it in your agent.

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded-lg font-mono text-sm font-normal visRefresh2026Fonts:font-medium bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end sm:sticky sm:top-xs"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg role="img" class="inline-flex fill-current shrink-0" width="16" height="16"><use xlink:href="#pplx-icon-copy"></use></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-lg text-xs font-thin">text</div></div><div><span><code><span><span>administrative_coverage_india:
</span></span><span>
</span><span>  meta:
</span><span>    scope: "India – reimbursement and access pathways for common outpatient and cardiovascular/diabetes drugs."
</span><span>    intended_use: "Support an AI agent in answering administrative queries about who pays, under which scheme, and what differences exist between public and private coverage for the listed drugs."
</span><span>
</span><span>  # -------------------------------------------------
</span><span>  # 1. PUBLIC / GOVERNMENT PROGRAMS (SCHEME-LEVEL)
</span><span>  # -------------------------------------------------
</span><span>
</span><span>  schemes:
</span><span>
</span><span>    pmjay:
</span><span>      name: "Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (PM-JAY)"
</span><span>      type: "Public, government-funded, secondary and tertiary care insurance."
</span><span>      coverage_model: >
</span><span>        PM-JAY pays hospitals a fixed package rate per procedure/condition for eligible poor and vulnerable families;
</span><span>        the package includes bed charges, investigations, procedures, medicines, and implants during the episode of care
</span><span>        (inpatient + defined pre/post-hospitalisation), not separate per-drug OPD reimbursement. [web:130][web:127][web:115][web:121][web:118][web:124]
</span><span>      scope:
</span><span>        - "Covers ~1350–1900+ medical and surgical packages across ~23 specialties; all pre‑existing diseases are covered for eligible beneficiaries." [web:130][web:121][web:124]
</span><span>        - "No cap on family size or member age; fully cashless and paperless at empanelled public and private hospitals." [web:130]
</span><span>      drugs_relevance: >
</span><span>        For your drug list (paracetamol, antibiotics, metformin, statins, insulin, PPIs, etc.), PM‑JAY does not reimburse the outpatient prescription itself;
</span><span>        instead, when these are used as part of an approved hospitalisation package, their cost is bundled into the package rate paid to the hospital. [web:130][web:127][web:121]
</span><span>      outpatient_medicines: "Not routinely covered as standalone reimbursement; PM-JAY is not an OPD drug-cover scheme."
</span><span>      patient_payment_pattern: >
</span><span>        Eligible patient typically pays zero at point of care for covered hospitalisations;
</span><span>        the hospital is reimbursed directly by the scheme at the package rate, including drugs. [web:130][web:127]
</span><span>      key_links:
</span><span>        - "PM-JAY cost-of-treatment description: https://pib.gov.in/Pressreleaseshare.aspx?PRID=1594170"         # [web:127]
</span><span>        - "Example consolidated HBP 2.0 rate list (Uttar Pradesh): https://ayushmanup.in/assets/doc/HBP-2.0-Rate-List.pdf"  # [web:121]
</span><span>        - "State package master (Assam, PMJAY Package Master portal): https://atalamritabhiyan.assam.gov.in/information-services/pmjay-package-master" # [web:124]
</span><span>        - "Sample state package PDF (Ayushman Bharat – Arogya Karnataka): https://sast.karnataka.gov.in/sast/arogya/pkpdf.php?psch=Ayushman+Bharat+-+Arogya+Karnataka&htype=Government" # [web:118]
</span><span>        - "Legal overview of PM-JAY coverage components: https://www.globallegalinsights.com/practice-areas/pricing-reimbursement-laws-and-regulations/india/" # [web:130]
</span><span>
</span><span>    cghs:
</span><span>      name: "Central Government Health Scheme (CGHS)"
</span><span>      type: "Public, employer-based scheme for Central Government employees, pensioners, and eligible dependents."
</span><span>      coverage_model: >
</span><span>        CGHS provides cashless OPD consultations, free or subsidised medicines from CGHS wellness centres, and
</span><span>        cashless/reimbursed inpatient care at government and empanelled private hospitals at pre‑defined CGHS package rates. [web:122][web:119][web:125]
</span><span>      medicines_policy:
</span><span>        formulary:
</span><span>          description: >
</span><span>            CGHS supplies medicines mainly from its own formulary, which contains around 1,447 generic and 622 branded items;
</span><span>            non‑formulary drugs can sometimes be substituted with therapeutically similar formulary items. [web:122]
</span><span>          reference: "CGHS formulary reference: http://msotransparentnic.in/cghsnew/index.asp"   # [web:122]
</span><span>        issue_rules:
</span><span>          - "CGHS wellness centres supply medicines for a maximum of one month at a time for OPD beneficiaries in normal circumstances." [web:122]
</span><span>          - "In certain situations (e.g., beneficiary going abroad), medicines can be issued up to 3 months." [web:122]
</span><span>        reimbursement_rules:
</span><span>          - "Reimbursement is generally allowed only for treatments/investigations/procedures which have a prescribed CGHS rate and are done at CGHS-empanelled centres, except for defined emergency cases." [web:122][web:119]
</span><span>      drugs_relevance: >
</span><span>        Many of your listed drugs (paracetamol, aspirin, amoxicillin, ceftriaxone, metformin, insulin, statins, PPIs, salbutamol, budesonide, etc.)
</span><span>        are standard generic molecules and typically appear either in the main CGHS formulary or in the 'life-saving medicines' lists. [web:122][web:128]
</span><span>      patient_payment_pattern: >
</span><span>        For eligible CGHS beneficiaries using CGHS wellness centres or empanelled hospitals,
</span><span>        most listed medicines are provided free or at heavily subsidised rates; reimbursement is used mainly when treatment occurs outside the CGHS network under specific rules. [web:122][web:119]
</span><span>      key_links:
</span><span>        - "CGHS medicines/reimbursement instructions: https://www.gconnect.in/orders-in-brief/cghs/issue-medicines-reimbursement-cghs-instructions.html" # [web:122]
</span><span>        - "CAG performance audit on CGHS reimbursements: https://cag.gov.in/uploads/download_audit_report/2022/7%20Chapter%203-062f0e7626babf8.64112400.pdf" # [web:119]
</span><span>        - "CGHS package rate list example (city-wise rates): https://www.cghs.mohfw.gov.in/CGHSGrievance/FormFlowXACTION?hmode=ftpFileDownload&fileName=17062025170805_CGHS-Rate-2024--Thiruvananthapuram.pdf" # [web:125]
</span><span>        - "CGHS life‑saving multiple‑brand medicine list: https://www.cghs.mohfw.gov.in/CGHSGrievance/FormFlowXACTION?hmode=ftpFileDownload&fileName=27082025114224_List+of+Life+Saving+Multiple+Brands+Medicines.pdf" # [web:128]
</span><span>
</span><span>    esic:
</span><span>      name: "Employees’ State Insurance Scheme (ESIS/ESIC)"
</span><span>      type: "Contributory social health insurance for workers in covered establishments."
</span><span>      coverage_model: >
</span><span>        Financed by employer and employee contributions with an additional share from State Governments;
</span><span>        provides comprehensive medical benefit through ESIS hospitals and dispensaries, plus some reimbursement for defined emergency situations in non-recognised hospitals. [web:123][web:120][web:126]
</span><span>      medicines_policy:
</span><span>        - "Routine OPD and IPD medicines for insured persons are supplied within ESIS hospitals/dispensaries as per state formulary and ESIC norms." [web:123]
</span><span>        - "State Governments contribute up to a per‑capita ceiling (e.g., ₹3000 per insured person per year) towards medical benefit costs, over which additional expenditure is borne by the State Government." [web:123]
</span><span>      reimbursement_rules_emergency:
</span><span>        description: >
</span><span>          ESIC guidelines allow reimbursement of emergency treatments (including medicines) obtained at private/non-recognised hospitals
</span><span>          when conditions like sudden heart attack, cerebral haemorrhage, serious accidents, etc., make transfer to ESIC hospitals unsafe;
</span><span>          claims usually must be submitted within one year, and approval lies with the designated State authority. [web:126][web:123]
</span><span>      drugs_relevance: >
</span><span>        All your listed drugs are standard medicines that are routinely used in ESIC facilities;
</span><span>        their cost to the insured worker is generally nil at ESIC facilities, but emergency private-hospital prescriptions may be reimbursed according to ESIC rules. [web:123][web:126]
</span><span>      key_links:
</span><span>        - "General ESIC scheme description: http://www.esicoimbatore.org/esi-scheme/" # [web:123]
</span><span>        - "ESIC reimbursement guidelines (emergency/private treatment): https://esic.gov.in/reimbursement" # [web:126]
</span><span>        - "ESI contribution rates overview: https://cleartax.in/s/esi-rate" # [web:120]
</span><span>
</span><span>    jan_aushadhi:
</span><span>      name: "Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP) – Jan Aushadhi"
</span><span>      type: "Government-run low-cost generic pharmacy network (NOT insurance)."
</span><span>      coverage_model: >
</span><span>        PMBJP runs Jan Aushadhi Kendras that sell essential generic medicines at significantly lower MRPs compared with typical brand-name drugs;
</span><span>        there is no reimbursement—patients pay out of pocket but at heavily discounted generic prices. [web:117][web:114]
</span><span>      data_assets:
</span><span>        - "National product portfolio and MRP list available online with search and CSV/PDF download options." [web:117]
</span><span>        - "Sample state price list shows paracetamol 500 mg tablets, aspirin 150 mg, ceftriaxone-based injectables, metformin-based combos, and biphasic isophane insulin vials with low MRPs." [web:114]
</span><span>      drugs_relevance: >
</span><span>        Many molecules from your list (paracetamol, aspirin, ceftriaxone, metformin, insulin, PPIs, etc.) appear explicitly in Jan Aushadhi price lists,
</span><span>        making PMBJP a key 'administrative answer' when a patient asks about cheaper options. [web:114][web:117]
</span><span>      key_links:
</span><span>        - "Central PMBJP product search & CSV download: https://janaushadhi.gov.in/productportfolio/ProductmrpList" # [web:117]
</span><span>        - "Example state price list including paracetamol, aspirin, ceftriaxone, metformin SR + pioglitazone, biphasic insulin, etc.: https://hfw.assam.gov.in/sites/default/files/swf_utility_folder/departments/hfw_lipl_in_oid_3/menu/information_and_services/Pradhan%20Mantri%20Bhartiya%20Jan%20Aushadhi%20Pariyojna%20-%20Price%20List.pdf" # [web:114]
</span><span>
</span><span>  # -------------------------------------------------
</span><span>  # 2. PRIVATE HEALTH INSURANCE (GENERIC BEHAVIOUR)
</span><span>  # -------------------------------------------------
</span><span>
</span><span>  private_insurance:
</span><span>    regulator: "Insurance Regulatory and Development Authority of India (IRDAI)"
</span><span>    general_rules:
</span><span>      - "Most retail and group health policies in India primarily cover hospitalisation (inpatient) expenses; OPD medicines are usually excluded unless an OPD add-on or special product is purchased." [web:133][web:131][web:132]
</span><span>      - "Medicines used during an admissible hospitalisation (including your listed drugs) are usually covered as part of the overall hospital bill, subject to policy terms and package caps." [web:133]
</span><span>      - "Prescription drug coverage is often linked to an internal formulary – a plan-specific list of permitted medicines; non-formulary drugs may attract higher copay or full out-of-pocket payment." [web:129][web:136]
</span><span>      - "Updated IRDAI health insurance guidelines cap maximum waiting period for pre-existing diseases (like diabetes, hypertension, heart disease) at 3 years and make policies more inclusive; after that, claims for these conditions cannot usually be denied for waiting-period reasons." [web:137][web:140]
</span><span>    formulary_concept:
</span><span>      description: >
</span><span>        Each insurer maintains a list of covered medications (formulary); if a prescribed medication is not on this list,
</span><span>        the policyholder may pay full cost unless they switch to a covered alternative or obtain a formulary exception. [web:129][web:136]
</span><span>      key_points_for_agent:
</span><span>        - "Always ask the user for insurer name, plan name, and whether they have an OPD/drug cover rider."
</span><span>        - "Advise them to check or upload the policy booklet and formulary for precise per-drug coverage."
</span><span>    reimbursement_vs_cashless:
</span><span>      cashless:
</span><span>        description: >
</span><span>          For hospitalisations at network hospitals, claims are processed cashlessly through a TPA (Third Party Administrator) or in-house claims team;
</span><span>          the insured typically does not pay separately for in-hospital medicines like ceftriaxone, insulin drips, PPIs, etc., if the claim is approved. [web:135][web:138]
</span><span>      reimbursement:
</span><span>        description: >
</span><span>          In non-network hospitals or in reimbursement mode, the insured pays all bills upfront (including medications),
</span><span>          then submits documents (bills, discharge summary, prescriptions, diagnostics, claim form) for reimbursement within timelines such as 7–30 days depending on the insurer. [web:133][web:131][web:132]
</span><span>      tpa_role: >
</span><span>        TPAs, licensed by IRDAI, coordinate cashless authorisations and reimbursement claim processing but cannot themselves approve or reject claims beyond the insurer’s policy terms. [web:138][web:141]
</span><span>    key_links:
</span><span>      - "Prescription drug insurance explainer (formulary, coverage logic): https://www.careinsurance.com/blog/insurance-guide-articles/prescription-medications-navigating-coverage-with-health-insurance-plans" # [web:129]
</span><span>      - "Formulary and non-formulary medication concept: https://www.goodrx.com/insurance/health-insurance/medication-not-on-formulary" # [web:136]
</span><span>      - "IRDAI 2024–25 health insurance guideline summaries (waiting periods, inclusivity): https://www.policybazaar.com/health-insurance/general-info/articles/new-irdai-health-insurance-guidelines-you-must-know/" # [web:137]
</span><span>      - "More recent IRDAI guideline summary (pre-existing disease wait capped at 3 years): https://www.finedge.in/blog/health-insurance/updated-irdai-guidelines-for-health-insurance" # [web:140]
</span><span>      - "IRDAI health-insurance/TPA regulations (official PDF): https://aiia.gov.in/wp-content/uploads/2025/08/IRDAI-Health-Insurance-Regulations.pdf" # [web:143]
</span><span>      - "TPA explanation: https://www.policybazaar.com/health-insurance/general-info/articles/third-party-administrator-tpa-in-health-insurance/" # [web:138]
</span><span>      - "Reimbursement claim process explainer: https://www.policybazaar.com/health-insurance/general-info/articles/how-to-file-a-reimbursement-claim-under-health-insurance/" # [web:131]
</span><span>      - "Insurer example showing pre/post-hospitalisation medicine reimbursement: https://www.newindia.co.in/health-insurance/premier-mediclaim-insurance" # [web:133]
</span><span>      - "Mediclaim reimbursement concept and timelines: https://www.sbigeneral.in/blog/health-insurance/health-decoding-insurance/reimbursement-claims-in-mediclaim" # [web:132]
</span><span>
</span><span>  # -------------------------------------------------
</span><span>  # 3. DRUG-SPECIFIC ADMINISTRATIVE NOTES
</span><span>  #     (your six buckets; logic is very similar across drugs)
</span><span>  # -------------------------------------------------
</span><span>
</span><span>  drug_buckets:
</span><span>
</span><span>    pain_fever_antiinflammatory:
</span><span>      drugs: ["Paracetamol", "Ibuprofen", "Diclofenac", "Aceclofenac + Paracetamol", "Aspirin 75/150 mg"]
</span><span>      public_schemes:
</span><span>        pmjay: >
</span><span>          When used during an admissible hospitalisation (e.g., post-MI aspirin, perioperative analgesia), these medicines are paid for as part of the PM-JAY package;
</span><span>          there is no separate outpatient reimbursement for routine fever or pain prescriptions. [web:130][web:127][web:121]
</span><span>        cghs: >
</span><span>          Generic versions of paracetamol, aspirin, and NSAIDs are in the CGHS formulary or supplementary lists, so CGHS beneficiaries generally receive them free at CGHS dispensaries;
</span><span>          if prescribed by empanelled specialists, they are supplied for up to one month at a time. [web:122][web:128]
</span><span>        esic: >
</span><span>          For insured workers treated in ESIC facilities, these medicines are dispensed as per the state ESIS formulary with no direct charge;
</span><span>          in emergency private hospitalisations, their cost can be reimbursed if the episode meets ESIC emergency criteria. [web:123][web:126]
</span><span>      private_insurance: >
</span><span>        In hospitalised episodes (e.g., post‑stent aspirin, analgesia after surgery), the cost of these drugs is part of the overall hospital bill covered by the policy;
</span><span>        routine OPD prescriptions for fever or joint pain are usually not reimbursed unless the plan offers OPD benefits. [web:129][web:133][web:131][web:132]
</span><span>      low_cost_generic_access: >
</span><span>        Jan Aushadhi lists paracetamol 500 mg tablets and aspirin 150 mg tablets with very low MRPs, making them affordable even without insurance;
</span><span>        other analgesic molecules have comparable low-cost generics in the PMBJP price lists. [web:114][web:117]
</span><span>      questions_for_agent:
</span><span>        - "Are you covered by PM-JAY, CGHS, ESIC, or a private policy?"
</span><span>        - "Is the medicine being used for hospitalisation or only OPD/self-purchase?"
</span><span>        - "If private insurance: does your plan have OPD drug cover, or only hospitalisation?"
</span><span>
</span><span>    antibiotics:
</span><span>      drugs: ["Amoxicillin", "Amoxicillin + Clavulanic Acid", "Azithromycin", "Cefixime", "Ceftriaxone", "Cefuroxime", "Metronidazole", "Doxycycline", "Levofloxacin/Ciprofloxacin"]
</span><span>      public_schemes:
</span><span>        pmjay: >
</span><span>          For infections treated during PM-JAY-covered admissions (e.g., pneumonia, sepsis, surgery), antibiotic costs are bundled within the package rate and not billed separately to the patient. [web:130][web:127][web:121]
</span><span>        cghs: >
</span><span>          Widely used antibiotics such as amoxicillin, ceftriaxone, metronidazole and others are present in CGHS formulary and life-saving lists;
</span><span>          CGHS beneficiaries typically obtain them free from wellness centres when prescribed by CGHS/empanelled doctors. [web:122][web:128]
</span><span>        esic: >
</span><span>          ESIS hospitals stock common antibiotics from state/govt formularies; insured persons receive them without charge in-network,
</span><span>          while emergency care and antibiotics given in non-recognised hospitals can be reimbursed under ESIC emergency rules. [web:123][web:126]
</span><span>      private_insurance: >
</span><span>        In inpatient settings (e.g., IV ceftriaxone for sepsis, perioperative prophylaxis), antibiotics form part of the admissible treatment cost and are usually covered;
</span><span>        antibiotics prescribed purely as OPD (e.g., azithromycin for sore throat) are generally not reimbursed unless OPD cover exists. [web:133][web:131][web:129]
</span><span>      low_cost_generic_access: >
</span><span>        Jan Aushadhi price lists include numerous anti-infectives (e.g., ceftriaxone combinations, ciprofloxacin eye drops, etc.) with low MRPs,
</span><span>        which your agent can highlight as lower-cost sources when the user pays out of pocket. [web:114][web:117]
</span><span>      questions_for_agent:
</span><span>        - "Was the antibiotic part of a hospital admission or only outpatient therapy?"
</span><span>        - "Which scheme/insurer are you under, if any?"
</span><span>        - "Do you have access to a Jan Aushadhi Kendra nearby?"
</span><span>
</span><span>    diabetes:
</span><span>      drugs: ["Metformin", "Glimepiride", "Insulin (Regular/Human Mixtard)"]
</span><span>      public_schemes:
</span><span>        pmjay: >
</span><span>          Diabetes drugs given during hospitalisations (e.g., MI, stroke, decompensated HF) are included in the PM-JAY package cost;
</span><span>          PM-JAY does not currently fund long-term OPD diabetes prescriptions directly. [web:130][web:127]
</span><span>        cghs: >
</span><span>          Metformin, oral sulfonylureas, and human insulin preparations are standard items in CGHS formularies/lists;
</span><span>          CGHS beneficiaries typically receive monthly supplies via wellness centres, with special rules for those travelling abroad. [web:122][web:128]
</span><span>        esic: >
</span><span>          ESIS facilities supply essential oral antidiabetics and insulins as part of chronic disease management;
</span><span>          ongoing medication is provided through ESIS hospitals, and emergency non-network treatment can be reimbursed subject to ESIC rules. [web:123][web:126]
</span><span>      private_insurance: >
</span><span>        Most standard health insurance policies in India do not pay for chronic OPD diabetes medicines;
</span><span>        they may cover insulin and antidiabetic drugs given during admissions (e.g., for MI, CABG, diabetic ketoacidosis) as part of hospital charges.
</span><span>        For pre-existing diabetes, coverage usually starts only after serving a waiting period, now capped at 3 years under IRDAI norms. [web:137][web:140][web:133]
</span><span>      low_cost_generic_access: >
</span><span>        Jan Aushadhi lists multiple antidiabetic products, including metformin–pioglitazone combinations and biphasic isophane insulin injections, at controlled MRPs,
</span><span>        making them a key affordability pathway for patients lacking OPD drug coverage. [web:114][web:117]
</span><span>      questions_for_agent:
</span><span>        - "Is your query about long-term monthly medicines or about a recent/ongoing hospitalisation?"
</span><span>        - "Are you a CGHS/ESIC beneficiary (who get chronic diabetes drugs dispensed) or using private insurance?"
</span><span>        - "Are you open to switching to Jan Aushadhi generics to cut OPD costs?"
</span><span>
</span><span>    cardiovascular:
</span><span>      drugs: ["Amlodipine", "Losartan", "Telmisartan", "Atorvastatin", "Rosuvastatin", "Clopidogrel", "Aspirin + Clopidogrel"]
</span><span>      public_schemes:
</span><span>        pmjay: >
</span><span>          These drugs are essential components of secondary prevention and are used extensively during and after PM-JAY-covered admissions for cardiac events;
</span><span>          their in-hospital use is included in package payments (e.g., ACS, PCI, stroke packages). [web:130][web:127][web:121]
</span><span>        cghs: >
</span><span>          Antihypertensives, statins, and antiplatelets are central to CGHS chronic disease care; many of these agents (e.g., atorvastatin, losartan, clopidogrel) are supplied free from CGHS dispensaries as part of the formulary/life-saving lists. [web:122][web:128]
</span><span>        esic: >
</span><span>          ESIS manages hypertension, dyslipidaemia, and ischaemic heart disease within its facilities using generic statins, RAAS blockers, and antiplatelets;
</span><span>          in emergencies like heart attack treated outside ESIC hospitals, related drug expenditure may be reimbursed if the claim fits emergency criteria. [web:123][web:126]
</span><span>      private_insurance: >
</span><span>        Inpatient cardiac episodes (e.g., MI, stenting, CABG) require intensive use of antiplatelets, statins, ACEI/ARBs, and these medicine costs are part of the reimbursed hospital bill;
</span><span>        however, long-term OPD prescriptions for BP or cholesterol control are generally not covered unless the policy explicitly includes OPD drug benefits. [web:129][web:133][web:131]
</span><span>      low_cost_generic_access: >
</span><span>        Many cardiovascular generics (e.g., aspirin 150 mg, several statins, metoprolol) appear in government price lists and Jan Aushadhi portfolio with reduced MRPs,
</span><span>        which can dramatically lower out-of-pocket cost for chronic users without OPD coverage. [web:114][web:117]
</span><span>      questions_for_agent:
</span><span>        - "Are you asking about medicines used during a cardiac admission (stent/CABG) or ongoing home medication?"
</span><span>        - "Do you have CGHS/ESIC benefits (chronic drug supply) or only private insurance?"
</span><span>        - "Is your private plan only for hospitalisation or does it include OPD/medicine coverage?"
</span><span>
</span><span>    gastric_acid_reflux_and_antiemetic:
</span><span>      drugs: ["Pantoprazole", "Omeprazole/Rabeprazole", "Ondansetron"]
</span><span>      public_schemes:
</span><span>        pmjay: >
</span><span>          PPIs and antiemetics given during hospital stays (e.g., post‑surgery GI protection, chemotherapy-related nausea) are part of PM-JAY package tariff and not paid separately by the patient. [web:130][web:127][web:121]
</span><span>        cghs: >
</span><span>          Common PPIs (omeprazole, pantoprazole, etc.) and several antiemetics are present in CGHS medicine lists;
</span><span>          they are dispensed at wellness centres when prescribed, within the usual one‑month supply rules. [web:122][web:128]
</span><span>        esic: >
</span><span>          ESIS hospitals use PPIs and antiemetics from their state formularies; insured persons obtain them via ESIS systems,
</span><span>          with reimbursement possible if used during emergencies in non‑recognised hospitals according to ESIC reimbursement norms. [web:123][web:126]
</span><span>      private_insurance: >
</span><span>        When PPIs/ondansetron are part of hospitalised care (e.g., peri‑operative or chemotherapy admissions), they are included in the reimbursed hospital bill;
</span><span>        OPD prescriptions for gastritis or GERD are rarely reimbursed unless the plan has OPD medicine benefits. [web:133][web:131][web:129]
</span><span>      low_cost_generic_access: >
</span><span>        Jan Aushadhi portfolios include several PPIs and GI medicines at low MRPs, so your agent can recommend Jan Aushadhi channels for patients paying out of pocket. [web:114][web:117]
</span><span>      questions_for_agent:
</span><span>        - "Is this PPI/ondansetron for home OPD use or part of an admission?"
</span><span>        - "Are you covered under any government scheme or only private insurance?"
</span><span>        - "Would a cheaper generic from Jan Aushadhi be acceptable?"
</span><span>
</span><span>    respiratory:
</span><span>      drugs: ["Salbutamol", "Montelukast + Levocetirizine", "Budesonide (inhaler/respules)"]
</span><span>      public_schemes:
</span><span>        pmjay: >
</span><span>          These drugs, when used during PM-JAY-covered admissions (e.g., status asthmaticus, COPD exacerbation), are part of the package and not separately billed to the beneficiary. [web:130][web:127][web:121]
</span><span>        cghs: >
</span><span>          Inhalers (salbutamol, budesonide) and oral anti-allergic combinations are important in CGHS chronic respiratory care and appear in CGHS formularies/lists,
</span><span>          supplied free or subsidised via wellness centres. [web:122][web:128]
</span><span>        esic: >
</span><span>          ESIS facilities typically provide these respiratory medications for asthma/COPD management to insured workers as per their formulary; emergency external use can be reimbursed under ESIC emergency rules. [web:123][web:126]
</span><span>      private_insurance: >
</span><span>        Respiratory medicines used during an admission (e.g., nebulised salbutamol, IV steroids, inhaled budesonide) are generally covered as part of hospital costs;
</span><span>        chronic OPD inhaler prescriptions are seldom reimbursed unless a specific OPD/inhaler benefit is present in the policy. [web:133][web:131]
</span><span>      low_cost_generic_access: >
</span><span>        Government price lists include low‑cost respiratory generics (e.g., salbutamol, ciprofloxacin eye/nasal preparations) and similar products,
</span><span>        and PMBJP/Jan Aushadhi stocks many comparable low-cost options, although inhaler coverage may be more limited than tablets/injectables. [web:114][web:117]
</span><span>      questions_for_agent:
</span><span>        - "Is the user asking about emergency hospitalisation costs (e.g., asthma attack) or month-to-month inhaler expense?"
</span><span>        - "Do they have employer-based ESIC coverage or only retail private insurance?"
</span><span>        - "Is there a Jan Aushadhi Kendra or state generic pharmacy nearby that could reduce inhaler/tablet costs?"
</span><span>
</span><span></span></code></span></div></div></div></pre>

If you want, I can next help you:

* turn this into a JSON schema your backend can query, and
* design the prompt template for your “admin agent” so it uses this structure to answer questions like “Is my metformin covered under PM‑JAY or CGHS?” or “How can I get cheaper atorvastatin in Delhi?”.
