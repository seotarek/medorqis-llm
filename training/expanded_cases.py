"""
MedOrqis-LLM — Additional Curated Clinical Scenarios (Cases 21 - 50)
Authentic clinical decision scenarios across Nephrology, Cardiology, Pediatrics,
Emergency Medicine, Pharmacology, Evidence Verification, and Arabic Dialects.
Zero emojis in code or text (design-doctrine compliance).
"""

import json
from training.dataset_builder import CLINICAL_TOOLS_SCHEMA, SYSTEM_PROMPT

EXPANDED_CLINICAL_CASES = [
    # 21. Nephrology - KDIGO 2024 AKI Staging
    {
        "id": "medorqis-nephro-kdigo-aki-en-021",
        "language": "en",
        "domain": "nephrology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 55-year-old post-op patient has a baseline serum creatinine of 0.9 mg/dL. 48 hours post-surgery, serum creatinine has risen to 2.8 mg/dL and urine output has been 0.3 mL/kg/h for the past 14 hours. Stage his Acute Kidney Injury according to KDIGO 2024 criteria."},
            {"role": "assistant", "content": "I will evaluate the patient's renal function against KDIGO 2024 criteria for Acute Kidney Injury staging using the MedOrqis deterministic engine.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "kdigo_aki_staging", "parameters": {"baseline_creatinine": 0.9, "current_creatinine": 2.8, "urine_output_ml_kg_h": 0.3, "urine_duration_hours": 14}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "kdigo_aki_staging", "creatinine_fold_increase": 3.11, "aki_stage": 3, "criterion_met": "Creatinine >= 3.0x baseline (Stage 3) and Urine output < 0.5 mL/kg/h for >= 12h (Stage 2)", "recommendation": "Urgent nephrology consult, hold all nephrotoxins, optimize volume status, prepare for potential RRT."})},
            {"role": "assistant", "content": "Based on KDIGO 2024 criteria for Acute Kidney Injury:\n\n- AKI Stage: Stage 3 (Severe AKI).\n- Serum Creatinine: 2.8 mg/dL represents a 3.11-fold increase over baseline (Stage 3 threshold is >= 3.0x baseline or >= 4.0 mg/dL).\n- Urine Output: 0.3 mL/kg/h for 14 hours meets Stage 2 oliguria criteria.\n\nMandatory Management Protocol:\n1. Discontinue all nephrotoxic agents (NSAIDs, ACEi/ARBs, Aminoglycosides).\n2. Review fluid balance and hemodynamics; assess fluid responsiveness.\n3. Monitor serum potassium and bicarbonate closely (treat refractory hyperkalemia or acidemia).\n4. Request urgent nephrology consultation to assess readiness for renal replacement therapy (RRT)."}
        ]
    },
    # 22. Cardiology - TIMI Risk Score for UA/NSTEMI
    {
        "id": "medorqis-cardio-timi-en-022",
        "language": "en",
        "domain": "cardiology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 68-year-old male with hypertension, diabetes, and hyperlipidemia presents with 2 episodes of severe angina at rest within the last 24 hours. He has known 60% LAD stenosis, takes daily aspirin, and ECG shows 0.8 mm ST-depression in V4-V6. Cardiac troponin I is elevated at 0.12 ng/mL. Calculate his TIMI risk score for UA/NSTEMI."},
            {"role": "assistant", "content": "I will calculate the TIMI risk score for unstable angina/NSTEMI using MedOrqis deterministic risk engine.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "timi_ua_nstemi", "parameters": {"age_65_or_older": True, "three_or_more_cad_risk_factors": True, "known_cad_stenosis_50_pct": True, "aspirin_use_past_7_days": True, "severe_angina_past_24h": True, "st_deviation_0_5mm": True, "elevated_cardiac_markers": True}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "timi_ua_nstemi", "score": 7, "risk_category": "HIGH_RISK", "14_day_event_rate_percent": 40.9, "triage_recommendation": "Immediate invasive strategy (coronary angiography within 24 hours or emergent)."})},
            {"role": "assistant", "content": "Based on the deterministic TIMI Risk Score calculation:\n\n- TIMI Score: 7 / 7 (High Risk).\n- 14-Day Risk of All-Cause Mortality, New/Recurrent MI, or Severe Recurrent Ischemia: 40.9%.\n\nClinical Recommendations (ESC & ACC/AHA NSTEMI Guidelines):\n1. Immediate Invasive Strategy: Coronary angiography indicated within 24 hours (or immediate if hemodynamic instability/refractory pain develops).\n2. Antithrombotic Therapy: Dual antiplatelet therapy (Aspirin 300mg + Ticagrelor 180mg load) plus parenteral anticoagulation (Enoxaparin 1 mg/kg SC BID or unfractionated heparin).\n3. Continuous telemetry monitoring in a cardiac care unit (CCU)."}
        ]
    },
    # 23. Pediatrics - Acute Paracetamol Overdose Rumack-Matthew
    {
        "id": "medorqis-peds-apap-overdose-ar-023",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "طفل عمره 14 عاما وزنه 50 كغ تناول 20 قرص باراسيتامول 500 ملغ دفعة واحدة (10 غرامات) بهدف إيذاء النفس قبل 4 ساعات بالضبط. تركيز الباراسيتامول في الدم الآن 180 mcg/mL. كيف نقيم خطورة التسمم الكبدي وما هو العلاج الفوري؟"},
            {"role": "assistant", "content": "سأقوم بتقييم احتمالية التسمم الكبدي الحاد وفق مخطط روماك-ماثيو (Rumack-Matthew Nomogram) المعتمد دوليا لتحديد الحاجة إلى مضاد التسمم N-acetylcysteine.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "rumack_matthew_apap", "parameters": {"hours_post_ingestion": 4.0, "apap_concentration_mcg_ml": 180.0}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "rumack_matthew_apap", "treatment_line_threshold_at_4h": 150.0, "patient_level": 180.0, "result": "ABOVE_TREATMENT_LINE", "risk": "PROBABLE_HEPATOTOXICITY", "antidote_indicated": True})},
            {"role": "assistant", "content": "[CRITICAL ESCALATION] تقييم التسمم الحاد بالباراسيتامول (Rumack-Matthew Nomogram):\n\n1. تقييم الخطورة:\n- عند الساعة الرابعة بعد الابتلاع، الحد الحرج لبدء الترياق هو 150 ميكروغرام/مل.\n- تركيز الباراسيتامول لدى المريض (180 mcg/mL) يقع أعلى من خط العلاج (Probable Hepatic Toxicity Line)، مما ينذر بفشل كبدي حاد ناتج عن استنزاف الجلوتاثيون.\n\n2. خطة التدخل الإسعافي الفوري:\n- البدء فورا بترياق N-Acetylcysteine (NAC) عبر الوريد وفق بروتوكول 21 ساعة (جرعة تحميل 150 mg/kg خلال ساعة، ثم 50 mg/kg خلال 4 ساعات، ثم 100 mg/kg خلال 16 ساعة).\n- فحص وظائف الكبد (ALT, AST)، زمن البروثرومبين (INR)، الكرياتينين، والغازات بالدم.\n- إحالة المريض للتقييم النفسي بعد استقرار حالته السريرية."}
        ]
    },
    # 24. Pharmacology - Warfarin + Metronidazole Bleeding Risk
    {
        "id": "medorqis-pharm-ddi-warfarin-en-024",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 59-year-old woman stabilized on Warfarin 5 mg daily for deep vein thrombosis is diagnosed with trichomoniasis and prescribed oral Metronidazole 500 mg BID for 7 days. Screen for interactions and advise on management."},
            {"role": "assistant", "content": "I will screen for metabolic cytochrome P450 interactions between Warfarin and Metronidazole using MedOrqis interaction engine.",
             "tool_calls": [{"type": "function", "function": {"name": "check_drug_interactions", "arguments": {"medications": ["Warfarin", "Metronidazole"]}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": json.dumps({"status": "MAJOR_INTERACTION", "severity": "HIGH", "pair": ["Warfarin", "Metronidazole"], "mechanism": "Metronidazole selectively inhibits CYP2C9, the primary enzyme responsible for metabolizing the more potent S-enantiomer of warfarin, leading to dramatic INR elevation and severe bleeding risk.", "clinical_action": "Empirically reduce warfarin dose by 30-50% upon starting metronidazole, and monitor INR closely at day 3 and day 5."})},
            {"role": "assistant", "content": "[WARNING] Major Pharmacokinetic Interaction (CYP2C9 Inhibition & Bleeding Risk):\n\n1. Mechanism: Metronidazole strongly inhibits hepatic CYP2C9, the enzyme responsible for clearing the potent S-warfarin isomer. Unadjusted co-administration frequently results in supratherapeutic INR (> 5.0 to 10.0) with catastrophic gastrointestinal or intracranial hemorrhage.\n\n2. Clinical Management Protocol (CHEST Guidelines):\n- Anticipatory Dose Reduction: Empirically reduce the maintenance warfarin dose by 30% to 50% on the day metronidazole is initiated.\n- Close INR Monitoring: Recheck INR on Day 3 and Day 5 of antibiotic therapy.\n- Patient Counseling: Instruct the patient to report any spontaneous epistaxis, melena, hematuria, or extensive bruising immediately."}
        ]
    },
    # 25. Dialectal Arabic - Saudi Dialect Heart Failure Triage
    {
        "id": "medorqis-dialect-sa-chf-ar-025",
        "language": "ar",
        "domain": "dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سعودي يقول: 'يا دكتور أحس بضيقة بصدره لما أنسدح، لازم أحط مخدتين أو ثلاث عشان أتنفس، وريولي متورمة وما يدخل فيها النعال'. ترجم الحالة ونظمها للطبيب مع الفحوصات المقترحة."},
            {"role": "assistant", "content": "سأقوم بتطبيع الشكوى من اللهجة السعودية العامية إلى المصطلحات الطبية المعيارية (SNOMED-CT / ICD-10) لتقييم قصور القلب الاحتقاني.",
             "tool_calls": [{"type": "function", "function": {"name": "normalize_terminology", "arguments": {"query": "ضيقة بصدره لما أنسدح مخدتين أو ثلاث عشان أتنفس ريولي متورمة ما يدخل فيها النعال"}}}]},
            {"role": "tool", "name": "normalize_terminology", "content": json.dumps({"standard_terms": [{"colloquial": "ضيقة بصدره لما أنسدح", "clinical": "Orthopnea", "snomed": "70156005"}, {"colloquial": "لازم أحط مخدتين أو ثلاث عشان أتنفس", "clinical": "Three-Pillow Orthopnea / Severity Indicator", "snomed": "267036007"}, {"colloquial": "ريولي متورمة وما يدخل فيها النعال", "clinical": "Bilateral Peripheral Pitting Edema", "snomed": "267038008"}]})},
            {"role": "assistant", "content": "التقرير الطبي المنظم (Structured Clinical Triage):\n\n- الأعراض الرئيسية:\n  1. ضيق التنفس عند الاستلقاء (Orthopnea): يحتاج المريض 3 وسائد للنوم، وهو مؤشر قوي على ارتفاع ضغط امتلاء البطين الأيسر واحتقان الرئتين.\n  2. وذمة الأطراف السفلية الانطباعية (Bilateral Peripheral Pitting Edema): تورم القدمين الذي يعيق ارتداء الحذاء دلالة على احتباس السوائل الجهازي.\n\n- التشخيص السريري المرجح:\n  تفجر حاد لقصور القلب الاحتقاني (Acute Decompensated Heart Failure - ADHF).\n\n- الخطة الفورية:\n  1. فحص الببتيد الدماغي المدر للصوديوم (BNP أو NT-proBNP) وتخطيط القلب (ECG).\n  2. صورة أشعة سينية للصدر (CXR) لتقييم الاحتقان الرئوي (Pulmonary Congestion).\n  3. إيكو القلب (Echocardiogram) لتحديد الكسر القذفي (EF).\n  4. البدء بمدرات البول العروية (IV Furosemide) ومراقبة الوزن والشوارد."}
        ]
    },
    # 26. Emergency - Acute Aortic Dissection Red Flag
    {
        "id": "medorqis-er-aortic-dissection-en-026",
        "language": "en",
        "domain": "emergency",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 58-year-old male presents with sudden, catastrophic chest pain radiating between the shoulder blades described as 'tearing'. BP is 195/110 mmHg in the right arm and 145/80 mmHg in the left arm. Right radial pulse is bounding; left radial pulse is faint. Provide emergency assessment and next steps."},
            {"role": "assistant", "content": "I will evaluate the patient's catastrophic presentation using MedOrqis red flag escalation engine for acute aortic syndromes.",
             "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["sudden catastrophic chest pain", "tearing pain radiating between shoulder blades", "bp asymmetry greater than 20 mmHg", "pulse deficit"]}}}]},
            {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_SURGICAL_EMERGENCY", "suspected_condition": "Acute Aortic Dissection (Stanford Type A Suspected)", "action": "Immediate CT Angiography of Chest/Abdomen, IV beta-blockade target HR < 60 and SBP 100-120 mmHg, urgent cardiothoracic surgery consultation."})},
            {"role": "assistant", "content": "[CRITICAL EMERGENCY] Acute Aortic Dissection (Stanford Type A Suspected):\n\nThis presentation with sudden onset tearing chest/back pain, blood pressure differential > 20 mmHg between limbs, and pulse deficit is diagnostic of acute aortic dissection until proven otherwise.\n\nImmediate Life-Saving Protocol (ESC & AHA Guidelines):\n1. Diagnostic Confirmation: Emergent CT Aortogram (CTA of chest and abdomen) immediately if hemodynamically stable; Bedside Transthoracic/Transesophageal Echocardiogram (TEE) if unstable.\n2. Hemodynamic Control (Anti-Impulse Therapy):\n   - IV Beta-Blocker first line (Esmolol or Labetalol) titrated to heart rate < 60 bpm.\n   - Follow with IV Vasodilator (Nitroprusside or Nicardipine) only after HR is controlled, targeting systolic BP 100-120 mmHg to reduce aortic wall shear stress (dP/dt).\n3. Emergent Surgical Call: Immediate cardiothoracic surgical mobilization for definitive repair."}
        ]
    },
    # 27. Pharmacology - Brand to INN Normalization & DDI Screen
    {
        "id": "medorqis-pharm-brand-norm-ar-027",
        "language": "ar",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض في مصر يتناول أدوية مسجلة بالأسماء التجارية: كونكور 5 ملغ، وبلافيكس 75 ملغ، وفولتارين 50 ملغ عند اللزوم، وميباكاردي 80 ملغ. هل يوجد أي تضارب دوائي أو خطر على المعدة والقلب؟"},
            {"role": "assistant", "content": "سأقوم أولا بتحويل الأسماء التجارية المصرية إلى الأسماء العلمية الدولية (INN)، ثم فحص التفاعلات الدوائية والآثار الجانبية القلبية الكلوية.",
             "tool_calls": [{"type": "function", "function": {"name": "normalize_terminology", "arguments": {"query": "كونكور بلافيكس فولتارين ميباكاردي"}}}]},
            {"role": "tool", "name": "normalize_terminology", "content": json.dumps({"mappings": [{"brand": "كونكور", "inn": "Bisoprolol", "class": "Beta-1 Selective Blocker"}, {"brand": "بلافيكس", "inn": "Clopidogrel", "class": "P2Y12 Antiplatelet"}, {"brand": "فولتارين", "inn": "Diclofenac", "class": "NSAID"}, {"brand": "ميباكاردي", "inn": "Telmisartan", "class": "Angiotensin II Receptor Blocker (ARB)"}]})},
            {"role": "assistant", "content": "سأفحص الآن التفاعلات بين الأدوية بعد تطبيعها: Bisoprolol, Clopidogrel, Diclofenac, Telmisartan.",
             "tool_calls": [{"type": "function", "function": {"name": "check_drug_interactions", "arguments": {"medications": ["Bisoprolol", "Clopidogrel", "Diclofenac", "Telmisartan"]}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": json.dumps({"status": "SIGNIFICANT_INTERACTION", "pairs": [{"pair": ["Clopidogrel", "Diclofenac"], "risk": "Greatly increased gastrointestinal bleeding risk due to antiplatelet + ulcerogenic NSAID combination."}, {"pair": ["Diclofenac", "Telmisartan"], "risk": "NSAIDs blunt ARB antihypertensive effect and synergistically reduce glomerular filtration rate, risking acute kidney injury."}], "recommendation": "Discontinue Diclofenac. Substitute with Paracetamol for analgesia."})},
            {"role": "assistant", "content": "تقرير التحليل الدوائي السريري:\n\n1. تطبيع الأسماء التجارية إلى الأسماء العلمية الدولية (INN):\n- كونكور = Bisoprolol (مثبط مستقبلات بيتا)\n- بلافيكس = Clopidogrel (مانع تجلط الصفيحات)\n- فولتارين = Diclofenac (مضاد التهاب غير ستيرويدي NSAID)\n- ميباكاردي = Telmisartan (خافض ضغط من فئة ARBs)\n\n2. التفاعلات والمخاطر السريرية المكتشفة:\n- الجمع بين Clopidogrel و Diclofenac يرفع خطر النزيف المعدي المعوي الحاد أضعافا مضاعفة.\n- مسكن Diclofenac يعاكس فاعلية خافض الضغط Telmisartan ويسبب تضيق الشريان الوارد الكلوي، مما يهدد بحدوث قصور كلوي حاد واحتباس الصوديوم.\n\n3. التوصية العلاجية:\n- إيقاف الفولتارين (Diclofenac) فورا، واستبداله بمركب آمن مثل الباراسيتامول عند اللزوم، وإضافة واق للمعدة (PPI) مثل Omeprazole إذا دعت الحاجة."}
        ]
    },
    # 28. Evidence - ESC 2024 Guidelines Verification
    {
        "id": "medorqis-evidence-esc-af-en-028",
        "language": "en",
        "domain": "evidence",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Does the 2024 European Society of Cardiology (ESC) guideline recommend the CHA2DS2-VA score instead of CHA2DS2-VASc for anticoagulation decision-making in atrial fibrillation? Verify with formal evidence citation."},
            {"role": "assistant", "content": "I will verify the clinical claim against the 2024 ESC Atrial Fibrillation Guidelines using MedOrqis two-stage evidence engine.",
             "tool_calls": [{"type": "function", "function": {"name": "verify_evidence", "arguments": {"ref_id": "ESC_2024_AF", "claim": "ESC 2024 guidelines recommend CHA2DS2-VA score (omitting female sex as a standalone risk factor) for stroke risk stratification in AF."}}}]},
            {"role": "tool", "name": "verify_evidence", "content": json.dumps({"ref_id": "ESC_2024_AF", "guideline_title": "2024 ESC Guidelines for the management of atrial fibrillation", "doi": "10.1093/eurheartj/ehae178", "claim_entailment": "ENTAILED", "grade_recommendation": "Class I, Level A", "summary": "Female sex is a risk modifier rather than an independent risk factor for stroke in AF. ESC 2024 adopts CHA2DS2-VA (scores 0 to 6), simplifying oral anticoagulation indication to score >= 2 (recommended) or score = 1 (should be considered)."})},
            {"role": "assistant", "content": "Evidence Verification Confirmed (GRADE Class I, Level A):\n\n- Guideline Reference: 2024 ESC Guidelines for the management of atrial fibrillation (European Heart Journal, 2024, doi:10.1093/eurheartj/ehae178).\n\nKey Update in ESC 2024:\n1. Renamed to CHA2DS2-VA: Female sex (the 'Sc' category) has been removed as a standalone score component because female sex alone without other risk factors does not confer excess stroke risk.\n2. Decision Thresholds:\n   - CHA2DS2-VA >= 2: Oral Anticoagulation (OAC with DOAC) is strongly recommended (Class I, Level A).\n   - CHA2DS2-VA = 1: Oral Anticoagulation should be considered (Class IIa, Level B).\n   - CHA2DS2-VA = 0: No antithrombotic therapy recommended (Class III, Harm)."}
        ]
    },
    # 29. Critical Care - Sepsis-3 Quick SOFA (qSOFA) Bedside Triage
    {
        "id": "medorqis-er-qsofa-en-029",
        "language": "en",
        "domain": "critical_care",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 70-year-old female with suspected pyelonephritis has respiratory rate 24/min, Glasgow Coma Scale 14 (mildly confused compared to baseline), and systolic BP 94 mmHg. Calculate her qSOFA score and interpret mortality risk."},
            {"role": "assistant", "content": "I will calculate the Quick Sequential Organ Failure Assessment (qSOFA) score using the deterministic clinical calculator.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "qsofa_score", "parameters": {"respiratory_rate": 24, "altered_mental_status": True, "systolic_bp": 94}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "qsofa_score", "score": 3, "risk_category": "HIGH_MORTALITY_SEPSIS_ALERT", "criteria_met": ["RR >= 22", "Altered Mentation GCS < 15", "SBP <= 100 mmHg"], "action": "Immediate sepsis resuscitation, serum lactate, blood cultures, broad-spectrum IV antibiotics within 1 hour."})},
            {"role": "assistant", "content": "Based on the Sepsis-3 qSOFA calculation:\n\n- Total qSOFA Score: 3 / 3 (High Risk of Poor Outcome / Sepsis Alert).\n- Criteria Met:\n  1. Respiratory Rate >= 22/min (+1)\n  2. Altered Mental Status GCS < 15 (+1)\n  3. Systolic BP <= 100 mmHg (+1)\n\nImmediate Sepsis 3 Bundle Actions:\n1. Draw blood cultures before antibiotic administration.\n2. Measure serum lactate; repeat if initial lactate > 2 mmol/L.\n3. Administer broad-spectrum IV antimicrobials within 1 hour of recognition.\n4. Rapid administration of 30 mL/kg IV crystalloid for hypotension (MAP < 65 mmHg) or lactate >= 4 mmol/L."}
        ]
    },
    # 30. Neurology - Glasgow Coma Scale (GCS) Head Injury Triage
    {
        "id": "medorqis-neuro-gcs-ar-030",
        "language": "ar",
        "domain": "neurology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مصاب في حادث سير: يفتح عينيه عند التنبيه المؤلم فقط، يصدر أصواتا غير مفهومة (أنات وتأوهات)، ويثني ذراعه بشكل غير طبيعي (سحب تجنبي / ثني غير طبيعي للطرف). احسب مقياس غلاسكو للغيبوبة GCS وحدد خطورة إصابة الدماغ."},
            {"role": "assistant", "content": "سأحسب مقياس غلاسكو للغيبوبة (GCS) عبر المحرك الحتمي لتقييم درجة الوعي وتحديد الحاجة للتنبيب والطبقي المحوري.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "glasgow_coma_scale", "parameters": {"eye_opening": "PAIN", "verbal_response": "INCOMPREHENSIBLE_SOUNDS", "motor_response": "ABNORMAL_FLEXION"}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "glasgow_coma_scale", "eye_score": 2, "verbal_score": 2, "motor_score": 3, "total_gcs": 7, "tbi_severity": "SEVERE_TBI", "airway_action": "GCS <= 8 mandates immediate endotracheal intubation for airway protection."})},
            {"role": "assistant", "content": "[CRITICAL EMERGENCY] تقييم مقياس غلاسكو للغيبوبة (Glasgow Coma Scale - GCS):\n\n1. تفصيل الدرجات:\n- فتح العين (Eye Opening): استجابة للألم فقط = 2 / 4\n- الاستجابة اللفظية (Verbal): أصوات غير مفهومة = 2 / 5\n- الاستجابة الحركية (Motor): ثني غير طبيعي = 3 / 6\n- المجموع الإجمالي: E2V2M3 = 7 من 15.\n\n2. التصنيف والتدخل الحرج (ATLS Protocol):\n- إصابة دماغية رضية شديدة (Severe TBI: GCS <= 8).\n- القاعدة الذهبية: GCS <= 8 يتطلب تأمين مجرى التنفس والتنبيب الرغامي فورا (Immediate Endotracheal Intubation) لحماية الرئة ومنع نقص الأكسجة الدماغية.\n- طلب تصوير طبقي محوري للرأس (Non-contrast Head CT) واستدعاء جراحة الأعصاب فورا."}
        ]
    }
]

# Cases 31 to 50
ADDITIONAL_CLINICAL_CASES_31_TO_50 = [
    # 31. Nephrology - Cockcroft-Gault for Dabigatran Contraindication
    {
        "id": "medorqis-nephro-dabigatran-en-031",
        "language": "en",
        "domain": "nephrology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "An 81-year-old female weighing 48 kg with non-valvular AF has serum creatinine 1.7 mg/dL. Her physician wants to start Dabigatran 150 mg BID. Calculate her Cockcroft-Gault CrCl and evaluate safety."},
            {"role": "assistant", "content": "I will calculate Cockcroft-Gault CrCl using the deterministic calculator to assess Dabigatran contraindication threshold.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "cockcroft_gault_crcl", "parameters": {"age_years": 81, "weight_kg": 48, "serum_creatinine_mg_dl": 1.7, "sex": "female"}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "cockcroft_gault_crcl", "crcl_ml_min": 19.6, "status": "SEVERE_RENAL_IMPAIRMENT", "contraindication": "Dabigatran is CONTRAINDICATED when CrCl < 30 mL/min (FDA/EMA)."})},
            {"role": "assistant", "content": "[CRITICAL WARNING] Dabigatran is Strictly Contraindicated:\n\n1. Deterministic CrCl: 19.6 mL/min (Severe renal impairment: CrCl < 30 mL/min).\n2. Pharmacokinetic Risk: Dabigatran is 80% eliminated unchanged by the kidneys. In severe renal impairment, accumulation occurs rapidly, leading to fatal uncontrollable hemorrhage.\n3. Clinical Recommendation: Switch to Apixaban (with close monitoring) or dose-adjusted Rivaroxaban/Edoxaban, or consider low-dose Warfarin with careful INR titration."}
        ]
    },
    # 32. Cardiology - HAS-BLED Bleeding Risk in Anticoagulation
    {
        "id": "medorqis-cardio-hasbled-en-032",
        "language": "en",
        "domain": "cardiology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 77-year-old male on Warfarin has BP 172/98 mmHg, history of ischemic stroke 3 years ago, liver cirrhosis (cirrhotic coagulopathy), and drinks 3 glasses of whiskey daily. Calculate his HAS-BLED bleeding risk score."},
            {"role": "assistant", "content": "I will calculate the HAS-BLED score using MedOrqis deterministic risk engine.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "has_bled_score", "parameters": {"hypertension_uncontrolled": True, "abnormal_renal_function": False, "abnormal_liver_function": True, "stroke_history": True, "bleeding_history": False, "labile_inr": False, "elderly_age_over_65": True, "drugs_antiplatelet_nsaid": False, "alcohol_excess": True}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "has_bled_score", "score": 5, "risk_category": "VERY_HIGH_BLEEDING_RISK", "annual_bleeding_risk_percent": 9.1})},
            {"role": "assistant", "content": "Based on the deterministic HAS-BLED calculation:\n\n- HAS-BLED Score: 5 / 9 (Very High Bleeding Risk, ~9.1% annual major bleed rate).\n- Components: Hypertension (1) + Liver disease (1) + Prior Stroke (1) + Age > 65 (1) + Alcohol excess (1).\n\nClinical Guidance:\n1. Address Modifiable Factors: Treat blood pressure aggressively (target < 130/80 mmHg) and provide alcohol cessation intervention.\n2. Do NOT stop anticoagulation solely based on high HAS-BLED; rather, establish high-frequency clinical follow-up and consider switching from Warfarin to DOAC if liver cirrhosis is Child-Pugh A."}
        ]
    },
    # 33. Cardiology - ESC 2024 HFrEF Guideline-Directed Medical Therapy
    {
        "id": "medorqis-cardio-hfref-quad-ar-033",
        "language": "ar",
        "domain": "cardiology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض عمره 60 عاما تم تشخيصه بقصور قلب مع كسر قذفي منخفض (HFrEF, EF 28%). الكرياتينين 1.1 mg/dL والبوتاسيوم 4.4 mmol/L وضغط الدم 125/80. ما هي الأركان الأربعة للعلاج الدوائي الموجه بالدلائل السريرية وفق ESC 2024؟"},
            {"role": "assistant", "content": "سأقوم بالتحقق من البروتوكول الرباعي المعتمد من الجمعية الأوروبية لأمراض القلب (ESC 2024) لقصور القلب منخفض الكسر القذفي عبر محرك الأدلة السريرية.",
             "tool_calls": [{"type": "function", "function": {"name": "verify_evidence", "arguments": {"ref_id": "ESC_2024_HF", "claim": "Guideline-directed medical therapy for HFrEF mandates four foundational pill classes: ARNI/ACEi, Beta-blocker, MRA, and SGLT2 inhibitor."}}}]},
            {"role": "tool", "name": "verify_evidence", "content": json.dumps({"ref_id": "ESC_2024_HF", "claim_entailment": "ENTAILED", "grade_recommendation": "Class I, Level A", "pillars": ["ARNI (Sacubitril/Valsartan) or ACEi", "Evidence-based Beta-blocker (Bisoprolol/Carvedilol/Metoprolol succinate)", "Mineralocorticoid Receptor Antagonist (Spironolactone/Eplerenone)", "SGLT2 inhibitor (Dapagliflozin/Empagliflozin)"]})},
            {"role": "assistant", "content": "الأركان الأربعة الإلزامية لعلاج قصور القلب HFrEF (توصية من الدرجة الأولى Class I, Level A):\n\n1. حاصر مستقبلات الأنجيوتنسين والنيبريليسين (ARNI):\n- Sacubitril/Valsartan (بدء بجرعة 24/26 ملغ مرتين يوميا والتدرج).\n\n2. حاصرات بيتا المعتمدة مثبتة خفض الوفيات:\n- Bisoprolol أو Carvedilol أو Metoprolol succinate.\n\n3. مضادات مستقبلات القشرانيات المعدنية (MRA):\n- Spironolactone (25 ملغ يوميا مع مراقبة البوتاسيوم ووظائف الكلى).\n\n4. مثبطات ناقل الصوديوم والجلوكوز-2 (SGLT2i):\n- Dapagliflozin 10 mg أو Empagliflozin 10 mg يوميا (تخفض الوفيات والاستشفاء بغض النظر عن وجود داء السكري).\n\nملاحظة سريرية: البوتاسيوم 4.4 والكرياتينين 1.1 يتيحان البدء الآمن بالفئات الأربع كاملة."}
        ]
    },
    # 34. Pediatrics - High-Dose Amoxicillin for Acute Otitis Media
    {
        "id": "medorqis-peds-amox-aom-en-034",
        "language": "en",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 3-year-old child weighing 14 kg is diagnosed with severe acute otitis media. Guidelines recommend high-dose amoxicillin at 90 mg/kg/day divided into 2 doses (every 12 hours). Adult max single dose is 1000 mg. Calculate each dose."},
            {"role": "assistant", "content": "I will calculate the pediatric weight-based dose for Amoxicillin with adult ceiling enforcement via MedOrqis deterministic dosing engine.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_pediatric_weight_dose", "arguments": {"age_years": 3, "weight_kg": 14, "dose_per_kg": 45, "max_single_adult_dose_mg": 1000, "dose_unit": "mg"}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": json.dumps({"age_years": 3, "weight_kg": 14, "calculated_dose_mg": 630, "max_single_adult_dose_mg": 1000, "final_safe_dose_mg": 630, "dose_capped": False})},
            {"role": "assistant", "content": "Deterministic Pediatric Dosing Calculation (AAP Guidelines):\n\n- Patient Weight: 14 kg\n- Total Daily Target: 14 kg × 90 mg/kg/day = 1260 mg/day\n- Individual Dose (BID): 1260 ÷ 2 = 630 mg orally every 12 hours\n- Adult Maximum Single Ceiling: 1000 mg (630 mg is well within safe bounds)\n\nPractical Dispensing Advice:\n- Using Amoxicillin 400 mg/5 mL oral suspension: 630 mg corresponds to ~7.9 mL orally twice daily with food for 10 days."}
        ]
    },
    # 35. Pediatrics - Ibuprofen Weight-Based Dosing with Adult Cap
    {
        "id": "medorqis-peds-ibuprofen-cap-ar-035",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "طفل عمره 11 سنة وزنه 48 كغ يعاني من ألم حاد بعد التواء الكاحل. الجرعة الموصوفة من إيبوبروفين هي 10 mg/kg، وسقف الجرعة الواحدة للبالغين هو 400 mg. احسب الجرعة الصحيحة."},
            {"role": "assistant", "content": "سأحسب الجرعة باستخدام محرك MedOrqis مع تطبيق سقف الأمان الصارم للبالغين لمنع التسمم الكلوي.",
             "tool_calls": [{"type": "function", "function": {"name": "calculate_pediatric_weight_dose", "arguments": {"age_years": 11, "weight_kg": 48, "dose_per_kg": 10, "max_single_adult_dose_mg": 400, "dose_unit": "mg"}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": json.dumps({"age_years": 11, "weight_kg": 48, "calculated_dose_mg": 480, "max_single_adult_dose_mg": 400, "final_safe_dose_mg": 400, "dose_capped": True, "policy": "Zero Overdose Policy - Capped at adult ceiling."})},
            {"role": "assistant", "content": "حساب الجرعة السريرية الآمنة وفق سياسة Zero Overdose:\n\n- الحساب النظري: 48 كغ × 10 ملغ/كغ = 480 ملغ.\n- تطبيق سقف الأمان: الحد الأقصى للجرعة الواحدة هو 400 ملغ.\n- الجرعة المعتمدة للطفل: 400 ملغ فقط (تم تقييد الجرعة لتفادي السمية المعدية والكلوية).\n- الإعطاء: تؤخذ مع أو بعد الوجبات كل 8 ساعات عند اللزوم."}
        ]
    },
    # 36. Emergency - Tension Pneumothorax Red Flag Escalation
    {
        "id": "medorqis-er-tension-pneumo-en-036",
        "language": "en",
        "domain": "emergency",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 24-year-old trauma victim has acute severe respiratory distress, cyanosis, tracheal deviation to the right side, hyperresonance to percussion on the left hemithorax, and absent breath sounds on the left. Blood pressure is 74/40 mmHg, HR 135 bpm. What is the immediate life-saving action?"},
            {"role": "assistant", "content": "I will evaluate this catastrophic respiratory presentation using MedOrqis red flag emergency engine.",
             "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["severe respiratory distress", "tracheal deviation to right", "hyperresonance left hemithorax", "absent left breath sounds", "severe hypotension"]}}}]},
            {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_SURGICAL_EMERGENCY", "suspected_condition": "Left-sided Tension Pneumothorax", "action": "IMMEDIATE NEEDLE DECOMPRESSION. DO NOT DELAY FOR CHEST X-RAY."})},
            {"role": "assistant", "content": "[CRITICAL SURGICAL EMERGENCY] Left-Sided Tension Pneumothorax:\n\nThis is a clinical diagnosis of immediate death risk caused by one-way valve air accumulation compressing the vena cava and arresting venous return to the heart.\n\nMandatory ATLS Life-Saving Action:\n1. Immediate Needle Thoracostomy: Insert a large-bore cannula (14-16 Gauge) into the second intercostal space at the midclavicular line (or fifth intercostal space anterior axillary line) on the left side.\n2. DO NOT WAIT FOR CHEST X-RAY: Ordering imaging before decompression is medical malpractice in tension pneumothorax.\n3. Follow immediately with formal tube thoracostomy (Chest Tube / Intercostal Drain 28-32 Fr) connected to underwater seal."}
        ]
    },
    # 37. Emergency - Acute Anaphylactic Shock Escalation
    {
        "id": "medorqis-er-anaphylaxis-ar-037",
        "language": "ar",
        "domain": "emergency",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريضة تبلغ 28 عاما بدأت تشكو من تورم مفاجئ في الشفتين واللسان، صعوبة شديدة في التنفس مع صرير حنجري (Stridor)، وطفح جلدي حطاطي حاك مع هبوط الضغط إلى 80/50 بعد 10 دقائق من تناول دواء أموكسيسيلين. ما هو التصرف الإسعافي الفوري من الدرجة الأولى؟"},
            {"role": "assistant", "content": "سأفحص الحالة فورا عبر محرك العلامات الحمراء للطوارئ لتقييم صدمة الحساسية المفرطة الحادة.",
             "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["sudden lip and tongue swelling", "stridor", "dyspnea", "generalized urticaria", "hypotension 80/50", "drug trigger"]}}}]},
            {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_ANAPHYLAXIS", "action": "IMMEDIATE INTRAMUSCULAR EPINEPHRINE 1:1000 (0.5 mg) into anterolateral mid-thigh. Oxygen, IV crystalloid resuscitation, airway preparation."})},
            {"role": "assistant", "content": "[CRITICAL RESUSCITATION] صدمة الحساسية المفرطة الحادة (Anaphylactic Shock):\n\nهذه حالة طوارئ مهددة للحياة فوريا بسبب انسداد مجرى التنفس والانهيار الوعائي.\n\nخطوات التدخل الفوري (Resuscitation Council / WAO Guidelines):\n1. الإبينفرين / الأدرينالين هو حجر الزاوية وخط العلاج الأول دون أي تأخير:\n- حقن 0.5 ملغ من الأدرينالين بتركيز 1:1000 في العضل (IM) في الجزء الأوسط الوحشي من الفخذ (Anterolateral Thigh).\n- تكرار الجرعة بعد 5 إلى 15 دقيقة إذا لم تستجب الأعراض.\n\n2. التدابير الداعمة المتزامنة:\n- استلقاء المريض ورفع الساقين (Trendelenburg position) لمنع متلازمة القلب الفارغ.\n- أكسجين عالي التدفق (15 L/min عبر قناع ذو خزان).\n- فتح خطين وريديين واسعين وإعطاء بلعة سوائل ملحية دافئة (1000-2000 mL Normal Saline IV).\n- إعطاء مضادات الهيستامين والكورتيكوستيرويدات كعلاج متمم ثانوي بعد استقرار الحالة."}
        ]
    },
    # 38. Pharmacology - Serotonin Syndrome (SSRI + Linezolid)
    {
        "id": "medorqis-pharm-serotonin-syn-en-038",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 42-year-old female on daily Sertraline 100 mg for depression is admitted with severe MRSA soft tissue infection. The resident intends to start IV Linezolid 600 mg BID. Is this combination safe?"},
            {"role": "assistant", "content": "I will screen for severe pharmacodynamic interactions between Sertraline and Linezolid using MedOrqis interaction engine.",
             "tool_calls": [{"type": "function", "function": {"name": "check_drug_interactions", "arguments": {"medications": ["Sertraline", "Linezolid"]}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": json.dumps({"status": "CONTRAINDICATED", "severity": "FATAL", "pair": ["Sertraline", "Linezolid"], "mechanism": "Linezolid is a reversible, non-selective monoamine oxidase inhibitor (MAOI). Co-administration with SSRIs like sertraline triggers life-threatening Serotonin Syndrome.", "clinical_action": "Contraindicated. Do not start linezolid without stopping sertraline (washout required), or use an alternative anti-MRSA agent such as Vancomycin or Daptomycin."})},
            {"role": "assistant", "content": "[CRITICAL WARNING] Life-Threatening Serotonin Syndrome Risk (Contraindicated):\n\n1. Mechanism: Linezolid possesses potent, reversible monoamine oxidase-A (MAO-A) inhibitory activity. Combining it with an SSRI (Sertraline) blocks both serotonin reuptake and metabolism, causing massive central and peripheral serotonin toxicity.\n2. Manifestations: Inducible and spontaneous clonus, hyperthermia (> 40 C), hyperreflexia, autonomic instability, seizures, and death.\n3. Clinical Recommendation: Do NOT administer Linezolid. Switch to alternative anti-MRSA antibiotics that have zero serotonergic activity, such as IV Vancomycin, Daptomycin, or Ceftaroline."}
        ]
    },
    # 39. Pharmacology - Digoxin + Amiodarone Toxicity
    {
        "id": "medorqis-pharm-digoxin-amio-ar-039",
        "language": "ar",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض عمره 74 عاما يتناول دواء الديجوكسين (Digoxin 0.25 mg) لقصور القلب والرجفان الأذيني. تقرر إضافة عقار أميودارون (Amiodarone 200 mg) لضبط نظم القلب. ما هو التحذير الصيدلاني المطلوب؟"},
            {"role": "assistant", "content": "سأفحص التفاعل الدوائي الحركي بين الديجوكسين والأميودارون عبر محرك السلامة الدوائية.",
                 "tool_calls": [{"type": "function", "function": {"name": "check_drug_interactions", "arguments": {"medications": ["Digoxin", "Amiodarone"]}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": json.dumps({"status": "MAJOR_INTERACTION", "pair": ["Digoxin", "Amiodarone"], "mechanism": "Amiodarone inhibits P-glycoprotein (P-gp) and decreases renal and non-renal clearance of digoxin, doubling serum digoxin concentrations within 3 to 7 days.", "clinical_action": "Empirically reduce digoxin dose by 50% immediately upon starting amiodarone, and monitor serum digoxin levels and ECG closely."})},
            {"role": "assistant", "content": "[WARNING] تفاعل دوائي حرج (مخاطر التسمم بالديجوكسين):\n\n1. آلية التفاعل:\n- عقار الأميودارون يثبط بروتين النقل P-glycoprotein ويقلل الإفراز الكلوي والصفراوي للديجوكسين، مما يرفع تركيز الديجوكسين في مصل الدم بمقدار الضعف (100% زيادة) خلال أيام قليلة.\n\n2. أعراض التسمم المتوقعة إن لم تُخفض الجرعة:\n- بطء قلب شديد أو إحصار أذيني بطيني (AV Block)، غثيان وقياء، اضطراب الرؤية الصفراء (Xanthopsia)، واضطرابات نظم بطينية خطيرة.\n\n3. التدبير السريري الإلزامي:\n- تخفيض جرعة الديجوكسين بنسبة 50% فورا (من 0.25 ملغ إلى 0.125 ملغ يوميا أو يوما بعد يوم).\n- فحص تركيز الديجوكسين في الدم بعد أسبوع من البدء ومراقبة البوتاسيوم ورسم القلب (ECG)."}
        ]
    },
    # 40. Pharmacology - Triple Hyperkalemia Synergy (Spironolactone + Lisinopril + Bactrim)
    {
        "id": "medorqis-pharm-triple-hyperkalemia-en-040",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 66-year-old male with heart failure takes Lisinopril 20 mg and Spironolactone 25 mg daily. He presents with uncomplicated cellulitis and is prescribed Trimethoprim-Sulfamethoxazole (Bactrim DS) 1 tablet BID. Screen for lethal biochemical synergies."},
            {"role": "assistant", "content": "I will screen for severe additive hyperkalemia risk across these three medications using MedOrqis interaction engine.",
             "tool_calls": [{"type": "function", "function": {"name": "check_drug_interactions", "arguments": {"medications": ["Lisinopril", "Spironolactone", "Trimethoprim-Sulfamethoxazole"]}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": json.dumps({"status": "HIGH_FATALITY_RISK", "severity": "SEVERE", "triad": ["Lisinopril", "Spironolactone", "Trimethoprim"], "mechanism": "Trimethoprim acts like amiloride by blocking the apical sodium channel (ENaC) in the distal nephron. Combined with aldosterone antagonism (Spironolactone) and ACE inhibition (Lisinopril), it induces catastrophic hyperkalemic cardiac arrest.", "clinical_action": "Avoid trimethoprim. Choose an alternative antibiotic with zero renal potassium-sparing effect (e.g. Doxycycline, Cephalexin)."})},
            {"role": "assistant", "content": "[CRITICAL WARNING] Fatal Hyperkalemia Synergy (Distal Nephron Blockade Triad):\n\n1. Mechanism: Trimethoprim structurally mimics the potassium-sparing diuretic amiloride, blocking epithelial sodium channels (ENaC) in the distal nephron. Combined with Lisinopril (decreased aldosterone production) and Spironolactone (aldosterone receptor blockade), renal potassium excretion is almost completely abolished.\n2. Clinical Consequences: Rapid onset of severe hyperkalemia (K > 6.5 - 7.5 mmol/L), leading to peaked T waves, QRS widening, sine-wave formation, and asystolic cardiac arrest.\n3. Clinical Recommendation: Substitute Bactrim with an alternative antimicrobial for cellulitis that has zero potassium impact, such as Doxycycline, Cephalexin, or Clindamycin."}
        ]
    },
    # 41. Dialectal Arabic - Levantine Atypical Angina / Dissection Triage
    {
        "id": "medorqis-dialect-levantine-ar-041",
        "language": "ar",
        "domain": "dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سوري في عيادة الطوارئ يقول: 'عم يوجعني صدري وعم بنخز بضهري وحاسس بنار متل الشطة ببلعومي، وعم دوق دوخة وما عم ارتاح'. ترجم الشكوى سريريا ونظم التشخيص التفريقي."},
            {"role": "assistant", "content": "سأقوم بتطبيع الشكوى من اللهجة الشامية إلى المصطلحات الطبية المعتمدة (SNOMED-CT / ICD-10).",
             "tool_calls": [{"type": "function", "function": {"name": "normalize_terminology", "arguments": {"query": "عم يوجعني صدري بنخز بضهري نار متل الشطة ببلعومي عم دوق دوخة"}}}]},
            {"role": "tool", "name": "normalize_terminology", "content": json.dumps({"standard_terms": [{"colloquial": "عم يوجعني صدري وعم بنخز بضهري", "clinical": "Retrosternal Chest Pain with Interscapular Radiation", "snomed": "29857009"}, {"colloquial": "نار متل الشطة ببلعومي", "clinical": "Severe Pyrosis / Esophageal Burning", "snomed": "69870006"}, {"colloquial": "عم دوق دوخة", "clinical": "Presyncope / Dizziness", "snomed": "271594007"}]})},
            {"role": "assistant", "content": "التقرير الطبي المنظم (Structured Triage Summary):\n\n- الشكوى السريرية المعيارية:\n  1. ألم صدري خلف عظمة القص ممتد إلى منطقة ما بين لوحي الكتف (Interscapular Pain).\n  2. إحساس حارق شديد في المريء والبلعوم (Severe Pyrosis).\n  3. دوار وإشراف على الإغماء (Presyncope).\n\n- التشخيص التفريقي الإلزامي:\n  1. متلازمة الشريان التاجي الحادة (ACS) أو تسلخ الشريان الأبهر (Aortic Dissection) بسبب الامتداد الظهري والدوار.\n  2. تشنج المريء الحاد أو ارتجاع مريئي حاد (GERD).\n\n- التدخل الفوري:\n  - تخطيط قلب كهربائي 12-lead ECG فورا.\n  - قياس ضغط الدم في كلا الذراعين لاستبعاد تفاوت الضغط (Aortic Dissection sign).\n  - فحص التروبونين عالي الحساسية وإنزيمات القلب."}
        ]
    },
    # 42. Dialectal Arabic - Maghrebi Hemoptysis / TB Triage
    {
        "id": "medorqis-dialect-maghreb-ar-042",
        "language": "ar",
        "domain": "dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض مغربي يقول: 'عندي سخانة قوية وكنكحب بالدم وصدري كيضرني بزاف، وعرقان بالليل وضعافيت بـ 7 كيلو فـ شهر'. ترجم الحالة سريريا وحدد الفحوصات العاجلة."},
            {"role": "assistant", "content": "سأقوم بتطبيع الشكوى من الدارجة المغربية إلى المصطلحات الطبية المعيارية لتقييم الأمراض الصدرية المعدية.",
             "tool_calls": [{"type": "function", "function": {"name": "normalize_terminology", "arguments": {"query": "سخانة قوية كنكحب بالدم صدري كيضرني بزاف عرقان بالليل ضعافيت 7 كيلو"}}}]},
            {"role": "tool", "name": "normalize_terminology", "content": json.dumps({"standard_terms": [{"colloquial": "سخانة قوية", "clinical": "High-Grade Pyrexia / Fever", "snomed": "386661006"}, {"colloquial": "كنكحب بالدم", "clinical": "Hemoptysis", "snomed": "66857006"}, {"colloquial": "صدري كيضرني بزاف", "clinical": "Pleuritic Chest Pain", "snomed": "43924001"}, {"colloquial": "عرقان بالليل", "clinical": "Drenching Night Sweats", "snomed": "42984000"}, {"colloquial": "ضعافيت 7 كيلو فـ شهر", "clinical": "Significant Unintentional Weight Loss (B-symptoms)", "snomed": "89362005"}]})},
            {"role": "assistant", "content": "التقرير السريري المنظم (Infectious Disease Triage):\n\n- الأعراض السريرية المعيارية:\n  1. بصاق مدمم (Hemoptysis).\n  2. حمى مرتفعة مترافقة مع تعرق ليلي غزير (Drenching Night Sweats).\n  3. ألم صدري جنبي (Pleuritic Pain).\n  4. فقدان وزن غير مقصود وسريع (7 كغ خلال شهر - أعراض B الكلاسيكية).\n\n- الاشتباه السريري ذو الأولوية:\n  التدرن الرئوي النشط (Active Pulmonary Tuberculosis) حتى يثبت العكس، أو خراج رئوي / ورم قصبي.\n\n- الإجراءات الوقائية والتشخيصية الفورية:\n  1. عزل المريض فورا في غرفة ضغط سلبي (Airborne Infection Isolation) مع ارتداء قناع N95.\n  2. صورة أشعة سينية للصدر (Chest Radiograph) للبحث عن تكهفات في الفص العلوي (Apical Cavitations).\n  3. فحص اللطاخة المباشرة وتحليل GeneXpert PCR لبلغم الصباح لثلاث عينات متتالية للكشف عن عصيات كوخ ومقاومة الريفامبيسين."}
        ]
    },
    # 43. Dialectal Arabic - Egyptian Nephrotic / Fluid Overload Triage
    {
        "id": "medorqis-dialect-eg-nephro-ar-043",
        "language": "ar",
        "domain": "dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريضة في مصر تقول: 'رجليا منفوخة ومعلمة فيها صوابعي، والبول قليل أوي ولونه زي الشاي، وعيني مورمة أول ما بصحى من النوم'. ترجم الحالة سريريا واقترح الفحوصات."},
            {"role": "assistant", "content": "سأقوم بتطبيع الشكوى من اللهجة المصرية إلى المصطلحات السريرية الدقيقة لتقييم المتلازمة الكلوية أو القصور الكلوي الحاد.",
             "tool_calls": [{"type": "function", "function": {"name": "normalize_terminology", "arguments": {"query": "رجليا منفوخة ومعلمة فيها صوابعي البول قليل لونه زي الشاي عيني مورمة أول ما بصحى"}}}]},
            {"role": "tool", "name": "normalize_terminology", "content": json.dumps({"standard_terms": [{"colloquial": "رجليا منفوخة ومعلمة فيها صوابعي", "clinical": "Bilateral Lower Limb Pitting Edema", "snomed": "267038008"}, {"colloquial": "البول قليل", "clinical": "Oliguria", "snomed": "28651003"}, {"colloquial": "لونه زي الشاي", "clinical": "Tea-Colored Urine / Gross Hematuria", "snomed": "34436003"}, {"colloquial": "عيني مورمة أول ما بصحى", "clinical": "Periorbital Morning Edema", "snomed": "271809000"}]})},
            {"role": "assistant", "content": "التقرير الطبي المنظم (Nephrology Triage Summary):\n\n- الأعراض السريرية المعيارية:\n  1. وذمة انطباعية ثنائية الجانب في الأطراف السفلية (Pitting Edema).\n  2. شح البول (Oliguria).\n  3. بول بلون الشاي يشير إلى بيلة دموية كبيبية (Glomerular Hematuria / Tea-Colored Urine).\n  4. وذمة حول الحجاج صباحية (Periorbital Edema) وهي علامة مميزة لفقدان البروتين أو متلازمة كبيبية.\n\n- التشخيص السريري المرجح:\n  متلازمة كلوية حادة (Nephritic Syndrome / Glomerulonephritis) أو متلازمة كلوية نفروتية متقدمة.\n\n- الفحوصات المخبرية العاجلة:\n  1. تحليل بول كامل مع فحص الراسب المجهري (Urinalysis + Microscopy) للبحث عن الأسطوانات الدموية (RBC casts).\n  2. فحص وظائف الكلى (الكرياتينين واليوريا) ونسبة البروتين إلى الكرياتينين في البول (Urine Protein/Creatinine Ratio).\n  3. قياس الألبومين بالدم ومستوى المتممة (C3, C4) وضغط الدم."}
        ]
    },
    # 44. Evidence - KDIGO 2024 SGLT2i Indication in CKD
    {
        "id": "medorqis-evidence-kdigo-sglt2-en-044",
        "language": "en",
        "domain": "evidence",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Does KDIGO 2024 clinical practice guideline recommend SGLT2 inhibitors for CKD patients with eGFR >= 20 mL/min/1.73m2 regardless of diabetes status? Verify with evidence citation."},
            {"role": "assistant", "content": "I will verify the clinical claim against the KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease.",
             "tool_calls": [{"type": "function", "function": {"name": "verify_evidence", "arguments": {"ref_id": "KDIGO_2024_CKD", "claim": "KDIGO 2024 recommends treating adults with CKD and eGFR >= 20 mL/min/1.73 m2 with an SGLT2 inhibitor, irrespective of diabetic status or albuminuria level."}}}]},
            {"role": "tool", "name": "verify_evidence", "content": json.dumps({"ref_id": "KDIGO_2024_CKD", "guideline_title": "KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease", "doi": "10.1016/j.kint.2023.10.018", "claim_entailment": "ENTAILED", "grade_recommendation": "Level 1A", "summary": "KDIGO 2024 provides a strong Level 1A recommendation to initiate an SGLT2 inhibitor in adults with CKD who have eGFR >= 20 mL/min/1.73 m2 (with urine ACR >= 200 mg/g or heart failure) regardless of whether type 2 diabetes is present."})},
            {"role": "assistant", "content": "Evidence Verification Confirmed (GRADE Level 1A):\n\n- Guideline Reference: KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease (Kidney International, 2024, doi:10.1016/j.kint.2023.10.018).\n\nKey Takeaways from KDIGO 2024:\n1. Broadened eGFR Threshold: SGLT2 inhibitors (Dapagliflozin or Empagliflozin) can now be safely initiated down to an eGFR threshold of 20 mL/min/1.73 m2 (previously 25-30 mL/min).\n2. Continuation Policy: Once initiated at eGFR >= 20 mL/min/1.73 m2, the SGLT2 inhibitor should be continued until dialysis or kidney transplantation, even if eGFR falls below 20 mL/min, unless not tolerated.\n3. Independent of Diabetes: Cardiovascular and nephroprotective mortality benefits are proven both in diabetic and non-diabetic CKD etiologies."}
        ]
    },
    # 45. Evidence - GOLD 2024 COPD Triple Therapy
    {
        "id": "medorqis-evidence-gold-copd-en-045",
        "language": "en",
        "domain": "evidence",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "What is the blood eosinophil count threshold in the GOLD 2024 report that favors adding an Inhaled Corticosteroid (ICS) to LABA/LAMA in COPD patients experiencing frequent exacerbations? Verify."},
            {"role": "assistant", "content": "I will verify the biomarker threshold against the GOLD 2024 Report for the diagnosis, management, and prevention of COPD.",
             "tool_calls": [{"type": "function", "function": {"name": "verify_evidence", "arguments": {"ref_id": "GOLD_2024_COPD", "claim": "GOLD 2024 recommends escalating to triple therapy (LABA+LAMA+ICS) when blood eosinophils are >= 300 cells/mcL or in patients with >= 2 moderate exacerbations or 1 hospitalization and eosinophils >= 100 cells/mcL."}}}]},
            {"role": "tool", "name": "verify_evidence", "content": json.dumps({"ref_id": "GOLD_2024_COPD", "guideline_title": "Global Initiative for Chronic Obstructive Lung Disease (GOLD) 2024 Report", "claim_entailment": "ENTAILED", "thresholds": {"strong_support": "Blood eosinophils >= 300 cells/mcL", "moderate_support": "Blood eosinophils 100-299 cells/mcL with >= 2 moderate exacerbations or >= 1 hospitalization", "against_use": "Blood eosinophils < 100 cells/mcL or repeated pneumonia episodes"}})},
            {"role": "assistant", "content": "Evidence Verification Confirmed (GOLD 2024 Report):\n\n- Blood Eosinophil Thresholds for ICS Addition:\n  1. Blood Eosinophils >= 300 cells/mcL: Strongly supports initial or escalated ICS addition to LABA/LAMA (Single-inhaler triple therapy reduces mortality and severe exacerbations).\n  2. Blood Eosinophils 100 to 299 cells/mcL: Favors ICS addition if the patient has had >= 2 moderate exacerbations or >= 1 severe exacerbation resulting in hospitalization per year.\n  3. Blood Eosinophils < 100 cells/mcL: Strongly contraindicates ICS use due to lack of efficacy and elevated risk of bacterial pneumonia."}
        ]
    },
    # 46. Toxicology - Carbon Monoxide Poisoning Triage
    {
        "id": "medorqis-tox-co-poisoning-en-046",
        "language": "en",
        "domain": "toxicology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A family of three was found in an apartment with a faulty gas water heater. A 35-year-old female presents with severe throbbing headache, confusion, and nausea. Standard pulse oximeter shows SpO2 99% on room air. Explain why pulse oximetry is misleading and determine immediate management."},
            {"role": "assistant", "content": "I will evaluate the toxicity mechanisms and diagnostic traps of acute carbon monoxide exposure.",
             "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["gas heater exposure", "throbbing headache", "altered mental status", "normal pulse oximetry despite hypoxia"]}}}]},
            {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_TOXICOLOGY", "suspected_condition": "Acute Carbon Monoxide (CO) Poisoning", "trap": "Standard dual-wavelength pulse oximeters cannot distinguish carboxyhemoglobin from oxyhemoglobin, falsely reading normal SpO2.", "action": "Immediate 100% normobaric oxygen via non-rebreather mask, send arterial/venous blood gas for CO-oximetry carboxyhemoglobin (COHb), evaluate for hyperbaric oxygen (HBO) therapy."})},
            {"role": "assistant", "content": "[CRITICAL TOXICOLOGY ALERT] Acute Carbon Monoxide Poisoning:\n\n1. The Pulse Oximetry Trap:\n- Standard pulse oximeters measure absorbance at 660 nm and 940 nm. Carboxyhemoglobin (COHb) has identical light absorption to oxyhemoglobin at 660 nm, causing standard monitors to report a falsely reassuring SpO2 of 99-100% while cellular tissue is suffocating.\n\n2. Mandatory Diagnostic Confirmation:\n- Draw venous or arterial blood gas and request CO-Oximetry to measure actual carboxyhemoglobin (COHb) percentage (normal < 3% in non-smokers, < 10% in heavy smokers).\n\n3. Immediate Emergency Protocol:\n- Administer 100% High-Flow Normobaric Oxygen immediately via a tight-fitting non-rebreather mask (reduces CO half-life from 320 minutes on room air to ~80 minutes).\n- Indications for Hyperbaric Oxygen Therapy (HBO): COHb > 25% (or > 15% in pregnancy), any loss of consciousness, neurological deficits, severe metabolic acidosis, or ischemic ECG changes."}
        ]
    },
    # 47. Neurology - Subarachnoid Hemorrhage (Thunderclap Headache)
    {
        "id": "medorqis-neuro-sah-redflag-ar-047",
        "language": "ar",
        "domain": "neurology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريضة عمرها 49 عاما تصف صداعا مفاجئا بأنه 'أسوأ صداع في حياتها' بلغ ذروته خلال 30 ثانية أثناء رفع أثقال، مترافق مع قيء وتيبس بالرقبة (Neck stiffness) ورهاب الضوء. ما هو التشخيص الإسعافي وخوارزمية الفحص؟"},
            {"role": "assistant", "content": "سأفحص الأعراض فورا عبر محرك العلامات الحمراء للطوارئ لتقييم النزف تحت العنكبوتية الحاد.",
             "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["thunderclap headache peak under 1 minute", "worst headache of life", "meningismus / neck stiffness", "photophobia", "vomiting"]}}}]},
            {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_NEUROSURGICAL_EMERGENCY", "suspected_condition": "Aneurysmal Subarachnoid Hemorrhage (SAH)", "action": "Non-contrast Head CT within 6 hours. If CT negative and high suspicion remains, perform Lumbar Puncture for xanthochromia."})},
            {"role": "assistant", "content": "[CRITICAL NEUROSURGICAL EMERGENCY] نزف تحت العنكبوتية (Subarachnoid Hemorrhage - SAH):\n\nالصداع الرعدي المفاجئ (Thunderclap Headache) الذي يبلغ ذروته في أقل من دقيقة مع تيبس الرقبة هو نزف تحت عنكبوتية ناتج عن تمزق أم دم شريانية دماغية حتى يثبت العكس.\n\nالخوارزمية التشخيصية الإلزامية:\n1. التصوير الطبقي المحوري للرأس دون صبغة (Non-contrast Head CT):\n- يجب إجراؤه فورا. حساسيته تصل إلى 98-100% إذا أُجري خلال أول 6 ساعات من بدء الصداع.\n\n2. البزل القطني (Lumbar Puncture):\n- إذا كانت نتيجة الأشعة المقطعية سلبية أو أُجريت بعد 6 ساعات وظل الشك السريري قائما، فالبزل القطني إلزامي لفحص وجود اصفرار السائل الدماغي الشوكي (Xanthochromia) وضغط الفتح.\n\n3. التدابير العاجلة:\n- ضبط ضغط الدم (SBP < 140 mmHg) لمنع عودة النزف، وإعطاء Nimodipine 60 mg كل 4 ساعات لمنع تشنج الأوعية الدماغية ونقص التروية المتأخر، واستدعاء جراحة الأعصاب."}
        ]
    },
    # 48. Surgery - Cauda Equina Syndrome Emergency
    {
        "id": "medorqis-surg-cauda-equina-en-048",
        "language": "en",
        "domain": "surgery",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 45-year-old male with chronic lumbar disc herniation presents with acute bilateral leg weakness, numbness in the groin and perineal area ('saddle distribution'), and new urinary retention with painless overflow dribbling. Provide triage and urgency classification."},
            {"role": "assistant", "content": "I will evaluate the patient's neurological presentation for spinal surgical emergencies.",
             "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["bilateral sciatica", "saddle anesthesia", "urinary retention with overflow incontinence", "lax anal sphincter tone"]}}}]},
            {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_SPINAL_SURGICAL_EMERGENCY", "suspected_condition": "Acute Cauda Equina Syndrome", "action": "Emergent Lumbar Spine MRI within 4 hours, immediate neurosurgical decompression within 24-48 hours to prevent permanent bladder/bowel incontinence and paraplegia."})},
            {"role": "assistant", "content": "[CRITICAL SURGICAL EMERGENCY] Cauda Equina Syndrome:\n\nThis constellation of bilateral lower extremity weakness, saddle anesthesia, and urinary retention with overflow is a spinal cord surgical emergency caused by central canal herniation compressing lumbosacral nerve roots.\n\nImmediate Actions Required:\n1. Urgent Whole-Spine/Lumbar MRI: Perform emergent MRI scan within 4 hours to confirm compression level.\n2. Emergent Surgical Call: Immediate spine/neurosurgical decompression (discectomy/laminectomy). Surgical decompression within 24-48 hours of symptom onset is vital to prevent irreversible urinary incontinence, fecal incontinence, and permanent sexual dysfunction.\n3. Nursing Action: Insert Foley catheter to decompress bladder and measure post-void residual volume."}
        ]
    },
    # 49. Pediatrics - Acute Epiglottitis Pediatric Emergency
    {
        "id": "medorqis-peds-epiglottitis-ar-049",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "طفل عمره 4 سنوات يصل لقسم الطوارئ بحمى 39.8، يسيل لعابه (Drooling)، يجلس منحنيا للأمام في وضعية القائمتين (Tripod position)، ويعاني من صرير شهيقي حاد مع غياب كامل للسعال. كيف يتعامل الطبيب فورا وما هو الإجراء الممنوع قطعا؟"},
            {"role": "assistant", "content": "سأفحص الأعراض فورا عبر محرك العلامات الحمراء للطوارئ لتقييم التهاب لسان المزمار الحاد لدى الأطفال.",
             "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["acute stridor in child", "drooling", "tripod positioning", "high fever", "absence of cough"]}}}]},
            {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_AIRWAY_EMERGENCY", "suspected_condition": "Acute Pediatric Epiglottitis", "forbidden_action": "DO NOT EXAMINE THE PHARYNX WITH A TONGUE DEPRESSOR. DO NOT AGITATE THE CHILD.", "action": "Mobilize ENT and Senior Anesthesiologist for controlled operating room intubation, humidified oxygen, IV ceftriaxone."})},
            {"role": "assistant", "content": "[CRITICAL AIRWAY EMERGENCY] التهاب لسان المزمار الحاد (Acute Pediatric Epiglottitis):\n\nتجمع أعراض الصرير الشهيقي، وسيلان اللعاب، ووضعية القائمتين الثلاثية (Tripod)، وغياب السعال يمثل التهابا حادا مهددا للحياة في لسان المزمار.\n\n1. التحذير المحظور قطعا (Absolute Contraindication):\n- يمنع منعا باتا فحص الحلق باستخدام خافض اللسان (Tongue Depressor) أو محاولة فتح الفم بالقوة، لأن ذلك قد يثير تشنجا حنجريا فوريا وتوقفا كاملا للتنفس.\n- تجنب إزعاج الطفل أو إجباره على الاستلقاء أو سحب دم وريدي قبل تأمين مجرى الهواء.\n\n2. البروتوكول العلاجي العاجل:\n- استدعاء استشاري التخدير وجراح الأنف والأذن والحنجرة فورا إلى غرفة العمليات.\n- تأمين مجرى التنفس عن طريق التنبيب الرغامي في بيئة غرفة العمليات المتحكم بها.\n- بعد تأمين مجرى الهواء، البدء بالمضادات الحيوية الوريدية (Ceftriaxone + Vancomycin)."}]
    },
    # 50. Evidence - KDIGO 2024 Blood Pressure Target in CKD
    {
        "id": "medorqis-evidence-kdigo-bp-en-050",
        "language": "en",
        "domain": "evidence",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "What is the systolic blood pressure target recommended by the KDIGO 2024 Clinical Practice Guideline for patients with chronic kidney disease? Verify with formal evidence citation."},
            {"role": "assistant", "content": "I will verify the blood pressure target against the KDIGO 2024 Clinical Practice Guideline for CKD.",
             "tool_calls": [{"type": "function", "function": {"name": "verify_evidence", "arguments": {"ref_id": "KDIGO_2024_BP", "claim": "KDIGO 2024 recommends targeting a systolic blood pressure of < 120 mmHg, when tolerated, using standardized office BP measurement in adults with CKD."}}}]},
            {"role": "tool", "name": "verify_evidence", "content": json.dumps({"ref_id": "KDIGO_2024_BP", "guideline_title": "KDIGO 2024 Clinical Practice Guideline for the Management of Blood Pressure in Chronic Kidney Disease", "claim_entailment": "ENTAILED", "grade_recommendation": "Level 1B", "target_sbp_mmhg": "< 120", "measurement_standard": "Standardized office blood pressure measurement"})},
            {"role": "assistant", "content": "Evidence Verification Confirmed (GRADE Level 1B):\n\n- Guideline Reference: KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease (Kidney International, 2024).\n\nKey Recommendation:\n1. Intensive SBP Target: Target a systolic blood pressure of < 120 mmHg, when tolerated, in adult CKD patients (with or without diabetes and across all levels of albuminuria).\n2. Standardized Measurement Prerequisite: This target applies strictly when blood pressure is measured using standardized office BP protocols (rested for 5 minutes, proper cuff size, back supported, uncrossed legs, automated oscillatory device).\n3. Clinical Rationale: Based on the SPRINT trial and CKD sub-analyses, intensive control (< 120 mmHg) significantly reduces all-cause mortality and major adverse cardiovascular events compared to standard control (< 140 mmHg)."}
        ]
    }
]

EXPANDED_CLINICAL_CASES.extend(ADDITIONAL_CLINICAL_CASES_31_TO_50)
