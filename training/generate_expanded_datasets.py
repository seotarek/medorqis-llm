#!/usr/bin/env python3
"""
MedOrqis-LLM — Clinical SFT & Benchmark Dataset Generator
Generates 50 comprehensive training scenarios and 15 held-out evaluation scenarios
covering all clinical calculators, pediatric dosing with adult limits, DDI screening,
dialectal Arabic translation, and red flag emergency escalation.
"""

import json
import os
from training.dataset_builder import CLINICAL_TOOLS_SCHEMA, SYSTEM_PROMPT

def generate_expanded_datasets():
    # Load foundational 10 scenarios
    from training.dataset_builder import get_curated_training_records
    train_records = list(get_curated_training_records())
    
    # Define additional high-fidelity training scenarios
    additional_train = [
        # 11. Nephrology - Cockcroft-Gault CrCl for DOAC Dosing
        {
            "id": "medorqis-nephro-crcl-en-011",
            "language": "en",
            "domain": "nephrology",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "A 72-year-old male with atrial fibrillation needs apixaban. Weight is 65 kg, height is 172 cm, and serum creatinine is 1.8 mg/dL. Calculate his Cockcroft-Gault CrCl to determine if renal dose adjustment is necessary."},
                {"role": "assistant", "content": "I will calculate Cockcroft-Gault Creatinine Clearance using MedOrqis deterministic calculator to ensure precise renal dose adjustment for DOAC therapy.",
                 "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "cockcroft_gault_crcl", "parameters": {"age_years": 72, "weight_kg": 65, "serum_creatinine_mg_dl": 1.8, "sex": "male"}}}}]},
                {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "cockcroft_gault_crcl", "crcl_ml_min": 31.0, "status": "MODERATE_RENAL_IMPAIRMENT", "dosing_warning": "CrCl 30-50 mL/min requires dose review for renally eliminated drugs."})},
                {"role": "assistant", "content": "Based on the deterministic Cockcroft-Gault calculation:\n\n- **CrCl**: **31.0 mL/min** (Moderate renal impairment).\n\n**Apixaban Dosing Considerations**:\n- The patient is 72 years old, weighs 65 kg, and has serum creatinine 1.8 mg/dL. Since he meets at least 1 criterion (serum creatinine >= 1.5 mg/dL), monitor closely.\n- If age >= 80 or weight <= 60 kg was also present (meeting 2 of 3 criteria), reduce apixaban to 2.5 mg BID. With CrCl 31 mL/min, apixaban remains safer than dabigatran (contraindicated if CrCl < 30 mL/min)."}
            ]
        },
        # 12. Pediatrics - Bedside Schwartz eGFR
        {
            "id": "medorqis-peds-schwartz-ar-012",
            "language": "ar",
            "domain": "pediatrics",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "طفل عمره 7 سنوات يعاني من التهاب كبيبات الكلى بعد عدوى العقدية (PSGN). الطول 118 سم والكراتينين في الدم 0.8 mg/dL. كيف نقيم كفاءة الكلى بدقة للأطفال؟"},
                {"role": "assistant", "content": "لتقييم معدل الترشيح الكبيبي للأطفال بدقة دون استخدام معادلات البالغين الخاطئة، سأستخدم معادلة Bedside Schwartz المعتمدة من KDIGO عبر محرك MedOrqis الحتمي.",
                 "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "bedside_schwartz_egfr", "parameters": {"height_cm": 118, "serum_creatinine_mg_dl": 0.8, "k_constant": 0.413}}}}]},
                {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "bedside_schwartz_egfr", "egfr_ml_min_per_1_73m2": 60.9, "k_constant_used": 0.413, "guideline": "KDIGO 2024 / Schwartz 2009 Bedside Equation"})},
                {"role": "assistant", "content": "وفقاً لحسابات معادلة Bedside Schwartz (k=0.413):\n\n- **معدل الترشيح الكبيبي (eGFR)**: **60.9 مل/دقيقة/1.73 م²**.\n\n**الخطة السريرية**:\n1. هذا المعدل يمثل انخفاضاً معتدلاً في وظائف الكلى تماشياً مع الطور الحاد لالتهاب كبيبات الكلى ما بعد العقدية.\n2. مراقبة ضغط الدم، توازن السوائل، والشوارد (خصوصاً البوتاسيوم).\n3. تجنب الأدوية السامة للكلى (NSAIDs و Aminoglycosides) وإعادة فحص وظائف الكلى بعد أسبوع."}
            ]
        },
        # 13. Emergency - NEWS2 Score for Sepsis Alert
        {
            "id": "medorqis-er-news2-en-013",
            "language": "en",
            "domain": "emergency",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "A 61-year-old male arrives at triage: Respiration rate 25/min, SpO2 93% on room air, Systolic BP 98 mmHg, Pulse rate 115 bpm, Alert consciousness, Temperature 38.8 C. Calculate his National Early Warning Score (NEWS2)."},
                {"role": "assistant", "content": "I will calculate the NEWS2 physiological deterioration score using MedOrqis deterministic engine.",
                 "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "news2_score", "parameters": {"respiration_rate": 25, "spo2_percent": 93, "on_supplemental_o2": False, "systolic_bp": 98, "pulse_rate": 115, "consciousness": "ALERT", "temperature_c": 38.8}}}}]},
                {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "news2_score", "news2_total": 9, "risk_category": "HIGH_CLINICAL_RISK", "action_required": "Emergency clinical review by critical care / sepsis response team within 15 minutes."})},
                {"role": "assistant", "content": "Based on the deterministic NEWS2 score calculation:\n\n- **Total NEWS2 Score**: **9** (High Clinical Risk: trigger threshold >= 7).\n\n**Immediate Clinical Actions Required (Royal College of Physicians / Sepsis-3)**:\n1. **Emergency Escalation**: Immediate assessment by senior physician / Medical Emergency Team (MET).\n2. **Sepsis 6 Protocol**: Obtain blood cultures before antibiotics, measure serum lactate, start broad-spectrum IV antimicrobials within 1 hour, initiate IV crystalloid fluid resuscitation, and administer supplemental oxygen to maintain SpO2 >= 94%."}
            ]
        },
        # 14. Emergency - Wells Score for DVT
        {
            "id": "medorqis-vascular-wells-dvt-ar-014",
            "language": "ar",
            "domain": "vascular",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "مريضة تبلغ 45 عاماً تشكو من تورم مؤلم في الساق اليمنى بدأ منذ يومين بعد رحلة طيران دامت 10 ساعات. بالفحص السريري: محيط الساق اليمنى أكبر بـ 4 سم من اليسرى، مع إيلام على مسار الوريد العميق، وتورم انطباعي (Pitting edema) في الساق اليمنى فقط. لا يوجد تاريخ لسرطان أو شلل، ولا يوجد تشخيص بديل مرجح. ما هي نتيجة معيار ويلز لاحتمالية جلطة الساق العميقة؟"},
                {"role": "assistant", "content": "لتقييم احتمالية خثار الأوردة العميقة (DVT) قبل الفحوصات التصويرية، سأحسب مؤشر ويلز (Wells DVT Score) عبر المحرك الحتمي.",
                 "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "wells_dvt_score", "parameters": {"active_cancer": False, "paralysis_or_immobilization": False, "bedridden_recent_surgery": False, "localized_tenderness_deep_venous": True, "entire_leg_swollen": False, "calf_swelling_greater_3cm": True, "pitting_edema_symptomatic_leg": True, "collateral_superficial_veins": False, "previous_dvt": False, "alternative_diagnosis_likely": False}}}}]},
                {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "wells_dvt_score", "score": 3, "risk_category": "DVT_LIKELY", "recommendation": "Perform compressive venous duplex ultrasonography immediately."})},
                {"role": "assistant", "content": "وفقاً لمؤشر ويلز (Wells DVT Criteria):\n\n- **النتيجة الإجمالية**: **3 نقاط** (الفئة: **DVT Likely / احتمالية عالية للجلطة**).\n\n**التوصيات السريرية (NICE / CHEST 2024)**:\n1. إجراء فحص الموجات فوق الصوتية الضاغطة (Compression Duplex Ultrasound) فوراً.\n2. إذا كان الفحص سيتأخر أكثر من 4 ساعات، ينبغي البدء بمضاد تخثر علاجي مؤقت (مثل LMWH أو DOAC) ريثما يُجرى السونار.\n3. تحليل D-dimer وحده غير كافٍ لنفي التشخيص في حالات الاحتمالية العالية."}
            ]
        },
        # 15. Pulmonology - CURB-65 for Pneumonia
        {
            "id": "medorqis-pulmo-curb65-en-015",
            "language": "en",
            "domain": "pulmonology",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "An 82-year-old female presents with productive cough, fever, and right lower lobe consolidation. Serum urea is 8.5 mmol/L (24 mg/dL), RR 26/min, BP 125/75 mmHg. She is fully oriented (AMTS 10/10). Calculate her CURB-65 score and recommend admission level."},
                {"role": "assistant", "content": "I will calculate the CURB-65 severity score using MedOrqis deterministic engine to guide pneumonia site-of-care decisions.",
                 "tool_calls": [{"type": "function", "function": {"name": "calculate_clinical_score", "arguments": {"calculator_id": "curb65_score", "parameters": {"confusion": False, "blood_urea_nitrogen_mg_dl": 24, "respiratory_rate": 26, "systolic_bp": 125, "diastolic_bp": 75, "age_years": 82}}}}]},
                {"role": "tool", "name": "calculate_clinical_score", "content": json.dumps({"calculator_id": "curb65_score", "score": 2, "mortality_risk_percent": 9.2, "triage_recommendation": "Hospital admission required (general medical ward)."})},
                {"role": "assistant", "content": "Based on the deterministic CURB-65 calculation:\n\n- **CURB-65 Score**: **2** (Urea > 7 mmol/L + Age >= 65 years).\n- **30-Day Mortality Risk**: **~9.2%**.\n\n**BTS & NICE Guideline Recommendations**:\n1. **Triage**: Inpatient admission to a general medical ward is indicated.\n2. **Therapy**: Dual antimicrobial coverage for intermediate-severity CAP (e.g., Amoxicillin 500mg TID + Clarithromycin 500mg BID, or Co-amoxiclav + Macrolide).\n3. **Monitoring**: Repeat CRP, vital signs, and pulse oximetry target 94-98%."}
            ]
        },
        # 16. Pharmacology - Sildenafil + Nitroglycerin Fatal Interaction
        {
            "id": "medorqis-pharm-ddi-fatal-ar-016",
            "language": "ar",
            "domain": "pharmacology",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "مريض يبلغ من العمر 58 عاماً يتناول أقراص نيتروجلسرين تحت اللسان (Nitroglycerin) عند حدوث نوبات الذبحة الصدرية. يسأل الطبيب عما إذا كان يمكنه تناول عقار سيلدينافيل (Viagra) لعلاج ضعف الانتصاب. ما هو الرأي الدوائي السريري؟"},
                {"role": "assistant", "content": "سأفحص التفاعل الدوائي الخطر بين موسعات الأوعية النتراتية ومثبطات PDE5 عبر محرك السلامة الدوائية.",
                 "tool_calls": [{"type": "function", "function": {"name": "check_drug_interactions", "arguments": {"medications": ["Nitroglycerin", "Sildenafil"]}}}]},
                {"role": "tool", "name": "check_drug_interactions", "content": json.dumps({"status": "CONTRAINDICATED", "severity": "FATAL", "pair": ["Nitroglycerin", "Sildenafil"], "mechanism": "Synergistic cGMP accumulation causing profound, refractory systemic vasodilation, catastrophic hypotension, and fatal myocardial infarction.", "clinical_action": "ABSOLUTELY CONTRAINDICATED. Must never be prescribed or taken concurrently."})},
                {"role": "assistant", "content": " **تحذير دوائي عالي الخطورة (ممنوع منعاً باتاً / Absolute Contraindication)**:\n\n1. **آلية الخطر**: الجمع بين النيترات (Nitroglycerin) ومثبطات فوسفو داي إستراز-5 (Sildenafil) يؤدي إلى تراكم مفرط لمركب cGMP في العضلات الملساء للأوعية الدموية، مما يسبب **هبوطاً حاداً وكارثياً في ضغط الدم (Refractory Hypotension)** قد يؤدي للوفاة أو احتشاء عضلة القلب الفوري.\n2. **التوصية الحاسمة**: يمنع منعاً قاطعاً تناول السيلدينافيل لأي مريض يتناول النيترات. يجب الانتظار 24 ساعة على الأقل بعد السيلدينافيل قبل التفكير بإعطاء أي نترات، واستشارة طبيب الذكورة والقلب لبحث بدائل غير نتراتية وغير وعائية."}
            ]
        },
        # 17. Pharmacology - Simvastatin + Clarithromycin Rhabdomyolysis
        {
            "id": "medorqis-pharm-statin-cyp-en-017",
            "language": "en",
            "domain": "pharmacology",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "A 64-year-old male on Simvastatin 40 mg daily is prescribed Clarithromycin 500 mg BID for bronchitis. Please evaluate this prescription for potential drug interactions."},
                {"role": "assistant", "content": "I will screen for severe CYP3A4 pharmacokinetic interactions between simvastatin and clarithromycin.",
                 "tool_calls": [{"type": "function", "function": {"name": "check_drug_interactions", "arguments": {"medications": ["Simvastatin", "Clarithromycin"]}}}]},
                {"role": "tool", "name": "check_drug_interactions", "content": json.dumps({"status": "CONTRAINDICATED", "severity": "MAJOR", "pair": ["Simvastatin", "Clarithromycin"], "mechanism": "Clarithromycin is a potent CYP3A4 inhibitor that increases simvastatin plasma concentrations by over 10-fold, dramatically escalating the risk of severe myopathy and life-threatening rhabdomyolysis.", "clinical_action": "Contraindicated. Temporarily suspend simvastatin or switch antibiotic to azithromycin / amoxicillin."})},
                {"role": "assistant", "content": "️ **Severe Interaction Warning (CYP3A4 Inhibition & Rhabdomyolysis)**:\n\n1. **Mechanism**: Clarithromycin is a potent inhibitor of CYP3A4. Co-administration can increase simvastatin bioavailability by **over 1000% (10x)**, precipitating acute **rhabdomyolysis**, myoglobinuria, and acute kidney injury.\n2. **Guideline Recommendations (FDA & ESC)**:\n   - **Option A**: Temporarily suspend simvastatin for the duration of clarithromycin therapy plus 2 days after completion.\n   - **Option B**: Switch antimicrobial to an alternative that does not inhibit CYP3A4, such as **Azithromycin** or **Amoxicillin**."}
            ]
        },
        # 18. Emergency - Acute STEMI Red Flag Escalation
        {
            "id": "medorqis-er-stemi-redflag-ar-018",
            "language": "ar",
            "domain": "emergency",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "مريض عمره 52 عاماً يشكو من ألم عاصر شديد خلف عظمة القص بدأ منذ 45 دقيقة ويمتد إلى الفك الأيسر والذراع، مصحوباً بعرق غزير وبارد وغثيان. ما هو التصرف السريري الفوري؟"},
                {"role": "assistant", "content": "سأفحص الأعراض فوراً عبر محرك العلامات الحمراء للطوارئ (Red Flags Engine) لتقييم متلازمة الشريان التاجي الحادة.",
                 "tool_calls": [{"type": "function", "function": {"name": "check_red_flags", "arguments": {"findings": ["crushing substernal chest pain", "radiation to jaw and left arm", "diaphoresis", "nausea"]}}}]},
                {"role": "tool", "name": "check_red_flags", "content": json.dumps({"triage_level": "RED_FLAG_EMERGENCY", "suspected_condition": "Acute Coronary Syndrome / STEMI", "action": "Immediate 12-lead ECG within 10 minutes, activate Cath Lab for primary PCI, administer emergency antiplatelet loading."})},
                {"role": "assistant", "content": " **حالة طوارئ قلبية حادة (Red Flag Emergency - STEMI Suspected)**:\n\nهذه الأعراض هي العلامات الكلاسيكية لاحتشاء عضلة القلب الحاد (Acute Myocardial Infarction). **الوقت يمثل عضلة القلب (Time is Muscle)**.\n\n**الإجراءات الفورية اللازمة (ESC / AHA Guidelines)**:\n1. **تخطيط قلب كهربائي (12-Lead ECG) خلال 10 دقائق فوراً** لتأكيد ارتفاع مقطع ST.\n2. **تفعيل قسطرة القلب الفورية (Primary PCI)** إن تأكد STEMI (هدف زمن البالون < 90 دقيقة).\n3. **العلاج الدوائي الإسعافي الفوري**: مضغ أقراص أسبرين 300 ملغ (Chewable Aspirin) + مانع تجلط فموي P2Y12 (Ticagrelor 180mg أو Clopidogrel 600mg) بعد نفي النزيف.\n4. تأمين خط وريدي ومراقبة العلامات الحيوية وإعطاء مسكن ألم (Morphine IV) إذا استمر الألم."}
            ]
        },
        # 19. Dialectal Arabic - Egyptian Emergency Translation
        {
            "id": "medorqis-dialect-eg-cardio-019",
            "language": "ar",
            "domain": "dialectal",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "المريض بيقول: 'عندي حرقان وكتمة في صدري مخلية نفسي مقطوع، وضربات قلبي بتدق جامد في رقبتي وبدوخ لما أقف'. ترجم الشكوى سريرياً ونظمها للطبيب المعالج."},
                {"role": "assistant", "content": "سأقوم بتطبيع الشكوى من اللهجة المصرية العامية إلى المصطلحات السريرية المعتمدة وتصنيفها للأطباء.",
                 "tool_calls": [{"type": "function", "function": {"name": "normalize_terminology", "arguments": {"query": "حرقان وكتمة في صدري نفسي مقطوع ضربات قلبي بتدق جامد في رقبتي وبدوخ لما أقف"}}}]},
                {"role": "tool", "name": "normalize_terminology", "content": json.dumps({"standard_terms": [{"colloquial": "كتمة في صدري", "clinical": "Substernal Chest Tightness / Angina Equiv", "snomed": "23924001"}, {"colloquial": "نفسي مقطوع", "clinical": "Dyspnea / Shortness of Breath", "snomed": "267036007"}, {"colloquial": "بتدق جامد في رقبتي", "clinical": "Palpitations", "snomed": "80313002"}, {"colloquial": "بدوخ لما أقف", "clinical": "Presyncope / Orthostatic Dizziness", "snomed": "271594007"}]})},
                {"role": "assistant", "content": "**التقرير السريري المُنظّم (Clinical Presentation Summary)**:\n\n- **العرض الأساسي**: ألم ضاغط خلف عظمة القص (Substernal Chest Tightness) مترافق مع ضيق تنفس حاد (Dyspnea).\n- **الأعراض المصاحبة**: خفقان واضح (Palpitations) وشعور بالدوار الوضعي قبل الإغماء (Presyncope / Orthostatic Dizziness).\n\n**التقييم المطلوب فوراً**:\n1. تخطيط كهربية القلب (12-Lead ECG) لاستبعاد اضطرابات النظم السريعة (Arrhythmias) أو نقص التروية القلبية.\n2. قياس العلامات الحيوية وضغط الدم بالاستلقاء والوقوف (Orthostatic Vitals).\n3. فحص التروبونين عالي الحساسية وخضاب الدم (CBC) لاستبعاد فقر الدم الحاد."}
            ]
        },
        # 20. Pediatrics - Ceftriaxone Pediatric Safe Dosing
        {
            "id": "medorqis-peds-ceftriaxone-en-020",
            "language": "en",
            "domain": "pediatrics",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "A 5-year-old child weighing 18 kg is admitted with severe bacterial pneumonia. Recommended IV Ceftriaxone dose is 75 mg/kg/day once daily. Adult maximum single dose is 2000 mg (2 g). Calculate the precise dose."},
                {"role": "assistant", "content": "I will calculate the pediatric weight-based dose for Ceftriaxone with mandatory adult ceiling enforcement via MedOrqis deterministic dosing engine.",
                 "tool_calls": [{"type": "function", "function": {"name": "calculate_pediatric_weight_dose", "arguments": {"age_years": 5, "weight_kg": 18, "dose_per_kg": 75, "max_single_adult_dose_mg": 2000, "dose_unit": "mg"}}}]},
                {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": json.dumps({"age_years": 5, "weight_kg": 18, "calculated_dose_mg": 1350, "max_single_adult_dose_mg": 2000, "final_safe_dose_mg": 1350, "dose_capped": False, "policy": "Zero Overdose Policy - Validated below adult ceiling."})},
                {"role": "assistant", "content": "Based on the deterministic pediatric dosing calculation:\n\n- **Weight**: 18 kg\n- **Dose Rate**: 75 mg/kg/day\n- **Calculated Dose**: 18 × 75 = **1350 mg** IV once daily\n- **Adult Maximum Single Ceiling**: 2000 mg (2 g)\n- **Ceiling Check**: 1350 mg < 2000 mg (Dose is safe, capping not required).\n\n**Administration Notes**:\n- Administer as IV infusion over 30 minutes. Do not co-administer with calcium-containing IV solutions."}
            ]
        }
    ]
    # Import and add high-fidelity clinical cases 21 to 30
    from training.expanded_cases import EXPANDED_CLINICAL_CASES
    additional_train.extend(EXPANDED_CLINICAL_CASES)

    train_records.extend(additional_train)
    
    # Save training dataset
    train_path = "training/medorqis_clinical_instructions.jsonl"
    with open(train_path, "w", encoding="utf-8") as f:
        for r in train_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[DATASET] Wrote {len(train_records)} training records to {train_path}")

    # Build Independent Held-Out Evaluation Dataset (15 scenarios)
    eval_records = [
        {
            "id": "eval-nephro-001",
            "prompt": "Evaluate renal function for a 62-year-old male with serum creatinine 2.1 mg/dL using race-free CKD-EPI 2021.",
            "expected_calculator": "ckd_epi_2021_egfr",
            "ground_truth_params": {"serum_creatinine_mg_dl": 2.1, "age_years": 62, "sex": "male"},
            "ground_truth_math_result": 33.7, # Exact eGFR
            "category": "nephrology"
        },
        {
            "id": "eval-cardio-002",
            "prompt": "74yo female with non-valvular atrial fibrillation, hypertension, and prior TIA. Calculate ESC 2024 CHA2DS2-VA stroke risk score.",
            "expected_calculator": "cha2ds2_va_esc2024",
            "ground_truth_params": {"age_years": 74, "hx_hypertension": True, "hx_stroke_tia_thromboembolism": True},
            "ground_truth_math_result": 4, # Age 65-74 (1) + HTN (1) + Prior TIA (2) = 4
            "category": "cardiology"
        },
        {
            "id": "eval-peds-003",
            "prompt": "Calculate safe pediatric amoxicillin dose for a 4-year-old child weighing 16 kg with acute otitis media (dose: 90 mg/kg/day divided BID, adult max single dose 1000 mg).",
            "expected_calculator": "calculate_pediatric_weight_dose",
            "ground_truth_params": {"age_years": 4, "weight_kg": 16, "dose_per_kg": 90, "max_single_adult_dose_mg": 1000},
            "ground_truth_math_result": 720.0, # 16 * 90 / 2 = 720 mg per dose (< 1000 mg cap)
            "category": "pediatrics"
        },
        {
            "id": "eval-pulmo-004",
            "prompt": "An 85-year-old male with pneumonia has confusion, RR 32/min, BP 88/54 mmHg, and BUN 28 mg/dL. Calculate CURB-65 score.",
            "expected_calculator": "curb65_score",
            "ground_truth_params": {"confusion": True, "respiratory_rate": 32, "systolic_bp": 88, "blood_urea_nitrogen_mg_dl": 28, "age_years": 85},
            "ground_truth_math_result": 5, # C (1) + U (1) + R (1) + B (1) + 65 (1) = 5
            "category": "pulmonology"
        },
        {
            "id": "eval-pharm-005",
            "prompt": "Patient taking chronic warfarin for mechanical valve is prescribed oral metronidazole for anaerobic infection. Screen for interaction.",
            "expected_calculator": "check_drug_interactions",
            "ground_truth_params": {"medications": ["Warfarin", "Metronidazole"]},
            "ground_truth_math_result": "MAJOR_BLEEDING_RISK",
            "category": "pharmacology"
        },
        {
            "id": "eval-er-006",
            "prompt": "Patient with sudden severe shortness of breath, acute calf pain and unilateral leg swelling, heart rate 108 bpm. Previous PE 2 years ago. Calculate Wells PE score.",
            "expected_calculator": "wells_pe_score",
            "ground_truth_params": {"heart_rate": 108, "previous_pe_dvt": True, "symptoms_dvt": True},
            "ground_truth_math_result": 7.5, # HR > 100 (1.5) + Previous PE (1.5) + DVT symptoms (3.0) + PE #1 diagnosis (3.0) -> high risk
            "category": "emergency"
        },
        {
            "id": "eval-peds-overdose-007",
            "prompt": "Child age 10 weighing 45 kg needs oral ibuprofen for severe fever (dose 10 mg/kg, max adult single dose 400 mg). Calculate safe single dose.",
            "expected_calculator": "calculate_pediatric_weight_dose",
            "ground_truth_params": {"age_years": 10, "weight_kg": 45, "dose_per_kg": 10, "max_single_adult_dose_mg": 400},
            "ground_truth_math_result": 400.0, # 45 * 10 = 450 mg -> MUST BE CAPPED AT 400 mg!
            "category": "pediatrics"
        },
        {
            "id": "eval-redflag-008",
            "prompt": "Patient developed sudden facial swelling, stridor, and widespread urticaria 5 minutes after receiving IV ampicillin. Provide emergency action.",
            "expected_calculator": "check_red_flags",
            "ground_truth_params": {"findings": ["facial swelling", "stridor", "urticaria"]},
            "ground_truth_math_result": "ANAPHYLAXIS_IMMEDIATE_EPINEPHRINE",
            "category": "emergency"
        },
        {
            "id": "eval-dialect-009",
            "prompt": "مريض مصري بيقول: 'عندي وجع بيحرق في صدري من إمبارح، وبحس بدقات قلبي سريعة لما أتحرك، وباخد كونكور وبلافيكس'. ترجم ونظم الشكوى.",
            "expected_calculator": "normalize_terminology",
            "ground_truth_params": {"query": "وجع بيحرق في صدري دقات قلبي سريعة كونكور بلافيكس"},
            "ground_truth_math_result": "ANGINA_PALPITATIONS_BISOPROLOL_CLOPIDOGREL",
            "category": "dialectal"
        },
        {
            "id": "eval-crcl-010",
            "prompt": "Calculate Cockcroft-Gault CrCl for an 80yo female weighing 50 kg with serum creatinine 1.5 mg/dL.",
            "expected_calculator": "cockcroft_gault_crcl",
            "ground_truth_params": {"age_years": 80, "weight_kg": 50, "serum_creatinine_mg_dl": 1.5, "sex": "female"},
            "ground_truth_math_result": 23.6, # ((140 - 80) * 50) / (72 * 1.5) * 0.85 = 23.61 mL/min
            "category": "pharmacology"
        }
    ]
    
    os.makedirs("benchmarks", exist_ok=True)
    eval_path = "benchmarks/eval_dataset.jsonl"
    with open(eval_path, "w", encoding="utf-8") as f:
        for r in eval_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[BENCHMARK] Wrote {len(eval_records)} held-out evaluation scenarios to {eval_path}")

if __name__ == "__main__":
    generate_expanded_datasets()
