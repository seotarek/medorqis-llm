"""
MedOrqis-LLM — Clinical Instruction Expansion (Cases 51 - 100)
Curated clinical scenarios addressing published Medical AI failure modes:
- Unit conversion order-of-magnitude errors
- Renal dose adjustments (KDIGO 2024 / FDA)
- Pediatric dose ceiling capping & frequency protections
- Critical DDI & Triple Whammy
- Dialectal clinical ambiguity & anti-sycophancy guardrails
Zero emojis in code or text (design-doctrine compliance).
"""

import json
from training.dataset_builder import CLINICAL_TOOLS_SCHEMA, SYSTEM_PROMPT

EXPANDED_CLINICAL_CASES_PART2 = [
    {
        "id": "medorqis-unit-cr-umol-en-051",
        "language": "en",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 65-year-old male in the ICU has a reported serum creatinine of 176.8 umol/L. Convert this to mg/dL before evaluating his eGFR under US guideline formulas."},
            {"role": "assistant", "content": "I will perform a deterministic unit conversion from umol/L to mg/dL using the MedOrqis clinical conversion engine.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 176.8, 'from_unit': 'umol/L', 'to_unit': 'mg/dL', 'analyte': 'creatinine'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 2.0, \"from_unit\": \"umol/L\", \"to_unit\": \"mg/dL\", \"analyte\": \"creatinine\", \"formula\": \"val / 88.42\"}"},
            {"role": "assistant", "content": "Based on deterministic clinical unit conversion:\n\n- Serum Creatinine: 176.8 umol/L is exactly 2.00 mg/dL (conversion factor: 1 mg/dL = 88.42 umol/L).\n\nClinical Impact:\nPlugging 176.8 directly into mg/dL-based formulas (like CKD-EPI or Cockcroft-Gault) would erroneously calculate profound end-stage kidney failure. The validated baseline of 2.00 mg/dL must be used for all subsequent eGFR calculations and renal dosing adjustments."}
        ]
    },
    {
        "id": "medorqis-unit-cr-umol-ar-052",
        "language": "ar",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سكري عمره 60 سنة أجرى تحليلاً في مختبر يعتمد النظام الدولي وجاءت نتيجة الكرياتينين 265.3 ميكرومول/لتر (umol/L). كم تعادل هذه القيمة بوحدة mg/dL لتقييم قصوره الكلوي؟"},
            {"role": "assistant", "content": "سأقوم بتحويل وحدة قياس الكرياتينين بدقة حتمية من ميكرومول/لتر إلى ملغ/ديسيلتر عبر محرك MedOrqis.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 265.3, 'from_unit': 'umol/L', 'to_unit': 'mg/dL', 'analyte': 'creatinine'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 3.0, \"from_unit\": \"umol/L\", \"to_unit\": \"mg/dL\", \"analyte\": \"creatinine\", \"formula\": \"val / 88.42\"}"},
            {"role": "assistant", "content": "بناءً على التحويل المخبري السريري الحتمي:\n\n- الكرياتينين في المصل: 265.3 ميكرومول/لتر يعادل تماماً 3.00 ملغ/ديسيلتر (معامل التحويل: 1 ملغ/ديسيلتر = 88.42 ميكرومول/لتر).\n\nالتوجيه السريري:\nهذه القيمة تمثل ارتفاعاً شديداً ينذر بقصور كلوي متقدم (المرحلة 4 أو 5 بحسب العمر والجنس). يجب استخدام القيمة 3.00 mg/dL لحساب معدل الترشيح الكبيبي الحقيقي وتجنب الخطأ الشائع بإدخال 265 مباشرة في المعادلات الرياضية."}
        ]
    },
    {
        "id": "medorqis-unit-weight-lbs-en-053",
        "language": "en",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 5-year-old child's parent reports the child weighs 44 lbs. Convert this weight to kilograms to allow accurate pediatric dosing calculation."},
            {"role": "assistant", "content": "I will convert the patient's weight from pounds (lbs) to kilograms (kg) using deterministic conversion.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 44.0, 'from_unit': 'lbs', 'to_unit': 'kg', 'analyte': 'weight'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 20.0, \"from_unit\": \"lbs\", \"to_unit\": \"kg\", \"analyte\": \"weight\", \"formula\": \"val * 0.45359237\"}"},
            {"role": "assistant", "content": "Based on deterministic physiological unit conversion:\n\n- Patient Weight: 44.0 lbs converts exactly to 20.0 kg (conversion factor: 1 lb = 0.45359 kg).\n\nSafety Alert:\nNever divide roughly by 2.0 in pediatric intensive care or critical drug dosing. The verified metric weight of 20.0 kg is the sole standard for all mg/kg drug calculations (e.g. Paracetamol 15 mg/kg = 300 mg; Amoxicillin 45 mg/kg/day = 900 mg/day)."}
        ]
    },
    {
        "id": "medorqis-unit-weight-lbs-ar-054",
        "language": "ar",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "أم تسأل: وزنت طفلي بميزان منزلي أمريكي وطلع 66 باوند (lbs). كم وزنه بالكيلوغرام لحساب جرعة المضاد الحيوي أوجمنتين؟"},
            {"role": "assistant", "content": "سأقوم بتحويل وزن الطفل بدقة من الرطل (باوند) إلى الكيلوغرام عبر محرك MedOrqis لمنع أخطاء الجرعات.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 66.0, 'from_unit': 'lbs', 'to_unit': 'kg', 'analyte': 'weight'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 29.94, \"from_unit\": \"lbs\", \"to_unit\": \"kg\", \"analyte\": \"weight\", \"formula\": \"val * 0.45359237\"}"},
            {"role": "assistant", "content": "بناءً على التحويل السريري الدقيق:\n\n- وزن الطفل: 66.0 رطلاً (باوند) يعادل 29.94 كغ (قرابة 30 كغ).\n\nتنبيه دوائي للأطفال:\nيجب دائماً الاعتماد على الوزن بالكيلوغرام (30 كغ) عند حساب جرعات المضادات الحيوية (مثل أموكسيسيلين/كلافولانات 45 ملغ/كغ/يوم = 1350 ملغ/يوم مقسمة على جرعتين، أي 675 ملغ كل 12 ساعة) لمنع نقص أو زيادة الجرعة."}
        ]
    },
    {
        "id": "medorqis-unit-digoxin-mcg-en-055",
        "language": "en",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A prescription reads Digoxin 125 mcg orally once daily for heart failure. The hospital pharmacy dispenses scored tablets in milligrams. Convert 125 mcg to mg."},
            {"role": "assistant", "content": "I will convert the microgram dose to milligrams using the MedOrqis unit conversion engine to eliminate 1000-fold dosing hazards.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 125.0, 'from_unit': 'mcg', 'to_unit': 'mg', 'analyte': 'mass'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 0.125, \"from_unit\": \"mcg\", \"to_unit\": \"mg\", \"analyte\": \"mass\", \"formula\": \"val / 1000.0\"}"},
            {"role": "assistant", "content": "[HIGH-ALERT MEDICATION SAFETY]\nBased on deterministic unit conversion:\n\n- Digoxin Dose: 125 mcg = 0.125 mg.\n\nCritical Pharmacology Guardrail:\nDigoxin has a very narrow therapeutic index (target serum concentration: 0.5 - 0.9 ng/mL). A 1,000-fold decimal error (confusing mcg with mg) represents a fatal overdose. Verify that the dispensed tablet is labeled 0.125 mg (or half of a 0.25 mg scored tablet) and monitor renal function and electrolytes."}
        ]
    },
    {
        "id": "medorqis-unit-levo-mcg-ar-056",
        "language": "ar",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريضة قصور درق تتناول إيوثيروكس (Levothyroxine) بجرعة 75 ميكروجرام (mcg). ترغب في معرفة ما يعادلها بوحدة المليجرام (mg) للتأكد من نشرة الدواء."},
            {"role": "assistant", "content": "سأقوم بتحويل الجرعة بدقة من الميكروجرام إلى المليجرام لحماية المريضة من مخاطر التسمم الدرقي.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 75.0, 'from_unit': 'mcg', 'to_unit': 'mg', 'analyte': 'mass'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 0.075, \"from_unit\": \"mcg\", \"to_unit\": \"mg\", \"analyte\": \"mass\", \"formula\": \"val / 1000.0\"}"},
            {"role": "assistant", "content": "بناءً على التحويل الصيدلاني الحتمي:\n\n- جرعة الليفوثيروكسين: 75 ميكروجرام تعادل تماماً 0.075 ملغ.\n\nتوجيه سريري للسلامة:\nأدوية هرمون الغدة الدرقية دقيقة جداً؛ تأكدي من تناول القرص صباحاً على معدة فارغة قبل الإفطار بنصف ساعة إلى ساعة مع كوب ماء كامل، وتجنب تناوله مع مكملات الكالسيوم أو الحديد خلال 4 ساعات لتفادي ضعف الامتصاص."}
        ]
    },
    {
        "id": "medorqis-unit-glucose-mmol-en-057",
        "language": "en",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A diabetic patient visiting from the UK measures blood glucose on his portable glucometer as 15.0 mmol/L. Convert this to mg/dL for clinical evaluation."},
            {"role": "assistant", "content": "I will convert blood glucose from mmol/L to mg/dL using deterministic biochemical conversion factor.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 15.0, 'from_unit': 'mmol/L', 'to_unit': 'mg/dL', 'analyte': 'glucose'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 270.27, \"from_unit\": \"mmol/L\", \"to_unit\": \"mg/dL\", \"analyte\": \"glucose\", \"formula\": \"val * 18.0182\"}"},
            {"role": "assistant", "content": "Based on deterministic biochemical conversion:\n\n- Blood Glucose: 15.0 mmol/L converts to 270.3 mg/dL (conversion factor: 1 mmol/L = 18.0182 mg/dL).\n\nClinical Assessment:\nThis indicates marked hyperglycemia (>250 mg/dL). Clinicians must screen for Diabetic Ketoacidosis (DKA) or Hyperosmolar Hyperglycemic State (HHS) by evaluating serum/urine ketones, blood gases, and hydration status."}
        ]
    },
    {
        "id": "medorqis-unit-glucose-mmol-ar-058",
        "language": "ar",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سكري من النوع الأول أحضر جهاز قياس بريطاني وسجل قراءة 18.5 مليمول/لتر (mmol/L) ويعاني من غثيان وعطش شديد. كم تساوي بالملغ/ديسيلتر وما خطورتها؟"},
            {"role": "assistant", "content": "سأقوم بتحويل قراءة السكر من مليمول/لتر إلى ملغ/ديسيلتر وتقييم علامات الحماض الكيتوني السكري.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 18.5, 'from_unit': 'mmol/L', 'to_unit': 'mg/dL', 'analyte': 'glucose'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 333.34, \"from_unit\": \"mmol/L\", \"to_unit\": \"mg/dL\", \"analyte\": \"glucose\", \"formula\": \"val * 18.0182\"}"},
            {"role": "assistant", "content": "[EMERGENCY ESCALATION]\nبناءً على التحويل البيوكيميائي الحتمي:\n\n- سكر الدم: 18.5 مليمول/لتر يعادل 333.3 ملغ/ديسيلتر.\n\nالتقييم السريري العاجل:\nهذه القراءة المرتفعة جداً (>300 mg/dL) المصحوبة بالغثيان والعطش الشديد لدى مريض سكري من النوع الأول تثير اشتباهاً قوياً بحماض كيتوني سكري (DKA). يجب التوجه فوراً لقسم الطوارئ لفحص الأجسام الكيتونية بالدم والبول، وقياس غازات الدم والشوارد، والبدء بالإماهة الوريدية والإنسولين المنتظم."}
        ]
    },
    {
        "id": "medorqis-unit-fentanyl-mcg-en-059",
        "language": "en",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "An ICU orders an intravenous fentanyl bolus of 50 mcg for procedural analgesia. Convert this dose to milligrams to confirm against the medication ampoule."},
            {"role": "assistant", "content": "I will convert intravenous fentanyl dose from micrograms to milligrams using the MedOrqis conversion tool.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 50.0, 'from_unit': 'mcg', 'to_unit': 'mg', 'analyte': 'mass'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 0.05, \"from_unit\": \"mcg\", \"to_unit\": \"mg\", \"analyte\": \"mass\", \"formula\": \"val / 1000.0\"}"},
            {"role": "assistant", "content": "[OPIOID INTENSIVE CARE SAFETY]\nBased on deterministic unit conversion:\n\n- Fentanyl Dose: 50 mcg is exactly 0.05 mg (50 micrograms).\n\nCritical Practice Rule:\nStandard fentanyl ampoules contain 100 mcg / 2 mL (50 mcg/mL). Therefore, 50 mcg corresponds to exactly 1.0 mL of the standard solution. Confusing milligrams and micrograms with synthetic opioids causes fatal respiratory arrest. Verify volume and concentration independently with two certified nurses."}
        ]
    },
    {
        "id": "medorqis-unit-infant-lbs-ar-060",
        "language": "ar",
        "domain": "unit_conversion",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "رضيع عمره 8 أشهر وزنه 15.4 باوند (lbs) ولديه حمى 39 درجة مئوية. حول وزنه إلى كيلوغرام لتحديد جرعة الإيبوبروفين الصحيحة."},
            {"role": "assistant", "content": "سأقوم بتحويل وزن الرضيع بدقة من الرطل إلى الكيلوغرام لضمان سلامة الجرعة.", "tool_calls": [{'type': 'function', 'function': {'name': 'convert_clinical_units', 'arguments': {'value': 15.4, 'from_unit': 'lbs', 'to_unit': 'kg', 'analyte': 'weight'}}}]},
            {"role": "tool", "name": "convert_clinical_units", "content": "{\"converted_value\": 6.99, \"from_unit\": \"lbs\", \"to_unit\": \"kg\", \"analyte\": \"weight\", \"formula\": \"val * 0.45359237\"}"},
            {"role": "assistant", "content": "بناءً على التحويل السريري الدقيق:\n\n- وزن الرضيع: 15.4 رطلاً (باوند) يعادل 7.00 كغ تماماً.\n\nحساب جرعة خافض الحرارة (إيبوبروفين للأطفال فوق 6 أشهر):\n- الجرعة المعيارية: 10 ملغ/كغ كل 6 إلى 8 ساعات عند اللزوم.\n- الجرعة للرضيع: 7.0 كغ * 10 ملغ/كغ = 70 ملغ للجرعة الواحدة.\n- لا يجوز إعطاء الإيبوبروفين للرضع أقل من 6 أشهر، ويجب ضمان إماهة الرضيع جيداً."}
        ]
    },
    {
        "id": "medorqis-renal-enoxaparin-en-061",
        "language": "en",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 72-year-old female weighing 60 kg is admitted with acute DVT. Her calculated Cockcroft-Gault CrCl is 22 mL/min. Adjust her therapeutic enoxaparin dose according to clinical guidelines."},
            {"role": "assistant", "content": "I will evaluate therapeutic enoxaparin dosing against KDIGO and FDA renal guidelines using deterministic renal dose adjustment.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'enoxaparin', 'standard_dose': '1 mg/kg SC q12h', 'crcl_or_egfr': 22.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"enoxaparin\", \"crcl_or_egfr\": 22.0, \"recommendation\": \"Dose reduction to 1 mg/kg SC once every 24 hours (50% reduction)\", \"anti_xa_monitoring\": true, \"risk\": \"Accumulation and major retroperitoneal/GI hemorrhage\"}"},
            {"role": "assistant", "content": "[HIGH-RISK RENAL PHARMACOLOGY]\nBased on KDIGO 2024 and FDA Renal Adjustment Guidelines for Enoxaparin:\n\n- Standard Therapeutic Regimen: 1 mg/kg subcutaneously every 12 hours (60 mg q12h).\n- Patient CrCl: 22 mL/min (<30 mL/min represents severe renal impairment).\n- Adjusted Guideline Regimen: 1 mg/kg subcutaneously ONCE DAILY (60 mg q24h) - exactly a 50% dose reduction.\n\nClinical Monitoring Protocol:\n1. Low-molecular-weight heparins depend on renal elimination. In severe renal insufficiency, failure to reduce frequency leads to drug accumulation and catastrophic bleeding.\n2. Consider monitoring peak anti-Factor Xa levels (target: 0.5 - 1.0 IU/mL measured 4 hours post-dose) or switching to unfractionated heparin with aPTT monitoring."}
        ]
    },
    {
        "id": "medorqis-renal-enoxaparin-ar-062",
        "language": "ar",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريضة عمرها 68 سنة وزنها 55 كغ تم تشخيصها بجلطة رئوية حادة. تصفية الكرياتينين المحسوبة لديها 25 مل/دقيقة. كيف نعدل جرعة كليكسان (Enoxaparin) العلاجية بأمان؟"},
            {"role": "assistant", "content": "سأقوم بتعديل جرعة الإنوكسابارين العلاجية وفق إرشادات القصور الكلوي الحاد لتجنب النزيف القاتل.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'enoxaparin', 'standard_dose': '1 mg/kg SC q12h', 'crcl_or_egfr': 25.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"enoxaparin\", \"crcl_or_egfr\": 25.0, \"recommendation\": \"Dose reduction to 1 mg/kg SC once every 24 hours (50% reduction)\", \"anti_xa_monitoring\": true, \"risk\": \"Accumulation and fatal hemorrhage\"}"},
            {"role": "assistant", "content": "تعديل جرعة كليكسان (Enoxaparin) العلاجية وفق الإرشادات السريرية الدولية (KDIGO 2024):\n\n1. تقييم التصفية الكلوية:\n- تصفية الكرياتينين (25 مل/دقيقة) تقع ضمن نطاق القصور الكلوي الشديد (<30 مل/دقيقة).\n\n2. الجرعة المعدلة بأمان:\n- الجرعة المعتادة: 55 ملغ تحت الجلد كل 12 ساعة.\n- الجرعة المعدلة إلزامياً: 55 ملغ تحت الجلد مرة واحدة فقط كل 24 ساعة (تخفيض بنسبة 50%).\n\nتحذير سريري صارم:\nيطرح الإنوكسابارين كلوياً؛ عدم خفض وتيرة الجرعة يؤدي إلى تراكم الدواء وحدوث نزيف باطني أو دماغي مهدد للحياة. يفضل قياس مستوى مضاد العامل العاشر (Anti-Xa) بعد 4 ساعات من الحقن أو التفكير في التحويل إلى الهيبارين غير المجزأ (UFH)."}
        ]
    },
    {
        "id": "medorqis-renal-metformin-stage4-en-063",
        "language": "en",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 63-year-old male with type 2 diabetes takes metformin 1000 mg twice daily. Recent labs show serum creatinine 2.4 mg/dL with eGFR 24 mL/min/1.73m2. What is the mandatory action regarding his metformin?"},
            {"role": "assistant", "content": "I will evaluate metformin safety against KDIGO 2024 and ADA/EASD guidelines for advanced chronic kidney disease.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'metformin', 'standard_dose': '1000 mg BID', 'crcl_or_egfr': 24.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"metformin\", \"crcl_or_egfr\": 24.0, \"contraindicated\": true, \"action\": \"DISCONTINUE_IMMEDIATELY\", \"risk\": \"Fatal Metformin-Associated Lactic Acidosis (MALA)\", \"mortality_rate\": \"30-50%\"}"},
            {"role": "assistant", "content": "[BLACK BOX WARNING: METFORMIN IN SEVERE CKD]\nBased on KDIGO 2024 and ADA/EASD Clinical Guidelines:\n\n- Patient eGFR: 24 mL/min/1.73m2 (CKD Stage 4, severe impairment).\n- Guideline Verdict: METFORMIN IS ABSOLUTELY CONTRAINDICATED.\n\nMandatory Actions:\n1. Discontinue metformin immediately. Metformin is eliminated by tubular secretion; when eGFR falls below 30 mL/min/1.73m2, toxic accumulation triggers Metformin-Associated Lactic Acidosis (MALA), carrying a 30-50% mortality rate.\n2. Screen for lactic acidosis (check venous/arterial lactate, serum bicarbonate, and anion gap).\n3. Transition glycemic management to renal-safe alternatives: DPP-4 inhibitor with dose adjustment (e.g. Linagliptin 5 mg daily without renal adjustment, or adjusted Sitagliptin 25 mg daily) or basal insulin."}
        ]
    },
    {
        "id": "medorqis-renal-metformin-stage4-ar-064",
        "language": "ar",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سكري عمره 66 سنة يتناول جلوكوفاج 1000 ملغ مرتين يومياً. أظهر التحليل تدهور وظائف الكلى وانخفاض معدل الترشيح الكبيبي (eGFR) إلى 22 مل/دقيقة/1.73م2. هل يستمر على الدواء؟"},
            {"role": "assistant", "content": "سأقوم بفحص معايير أمان الميتفورمين وفق إرشادات KDIGO 2024 للقصور الكلوي المتقدم.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'metformin', 'standard_dose': '1000 mg BID', 'crcl_or_egfr': 22.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"metformin\", \"crcl_or_egfr\": 22.0, \"contraindicated\": true, \"action\": \"DISCONTINUE_IMMEDIATELY\", \"risk\": \"Fatal Metformin-Associated Lactic Acidosis (MALA)\"}"},
            {"role": "assistant", "content": "[تحذير دوائي عاجل: إيقاف فوري للجلوكوفاج]\nوفقاً للإرشادات العالمية لأمراض الكلى والسكري (KDIGO 2024 & ADA):\n\n1. التقييم السريري:\n- معدل الترشيح الكبيبي للمريض (22 مل/دقيقة) يمثل قصوراً كلوياً شديداً من المرحلة الرابعة (CKD Stage 4).\n\n2. القرار الطبي الإلزامي:\n- إيقاف الجلوكوفاج (Metformin) فوراً وبشكل قاطع.\n- الدواء محظور تماماً وممنوع إذا كان معدل الترشيح أقل من 30 مل/دقيقة، لأن تراكمه يسبب الحماض اللبني المميت (Metformin-Associated Lactic Acidosis) الذي تصل نسبة الوفاة فيه إلى 50%.\n\n3. البدائل العلاجية الآمنة كلوياً:\n- التحويل إلى أدوية آمنة كلوياً لا تحتاج تعديل جرعة مثل لينامجلبتين (Linagliptin 5 mg) أو بدء الإنسولين القاعدي بجرعات محسوبة بدقة مع متابعة السكر."}
        ]
    },
    {
        "id": "medorqis-renal-metformin-stage3b-en-065",
        "language": "en",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 58-year-old diabetic female has an eGFR of 38 mL/min/1.73m2. She currently takes metformin 850 mg three times daily (2550 mg/day). What dose reduction is mandated under KDIGO 2024?"},
            {"role": "assistant", "content": "I will determine the maximum permissible metformin ceiling for CKD Stage 3b using deterministic renal dose adjustment.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'metformin', 'standard_dose': '2550 mg/day', 'crcl_or_egfr': 38.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"metformin\", \"crcl_or_egfr\": 38.0, \"max_safe_dose_mg_day\": 1000, \"recommendation\": \"Reduce dose to maximum 1000 mg/day (e.g. 500 mg BID)\", \"monitoring_interval_months\": 3}"},
            {"role": "assistant", "content": "Based on KDIGO 2024 and FDA Renal Safety Criteria for Metformin:\n\n- Patient eGFR: 38 mL/min/1.73m2 (CKD Stage 3b, 30-44 mL/min/1.73m2).\n- Current Dose: 2550 mg/day exceeds safe limits and creates dangerous accumulation risk.\n\nMandated Adjustments:\n1. Cap Maximum Dose at 1000 mg/day (e.g., 500 mg orally twice daily with meals).\n2. Do NOT initiate metformin if eGFR is between 30-44 mL/min; if already taking it, continuation at <=1000 mg/day is permissible under close surveillance.\n3. Re-evaluate renal function (eGFR and electrolytes) every 3 months. If eGFR drops below 30 mL/min/1.73m2, discontinue immediately."}
        ]
    },
    {
        "id": "medorqis-renal-metformin-stage3b-ar-066",
        "language": "ar",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سكري يتناول ميتفورمين 1000 ملغ مرتين يومياً (2000 ملغ باليوم). تحليل الكلى أظهر معدل ترشيح كبيبي eGFR يساوي 35 مل/دقيقة. كيف يجب ضبط الجرعة؟"},
            {"role": "assistant", "content": "سأقوم بحساب السقف الآمن لجرعة الميتفورمين للمرحلة 3b من القصور الكلوي عبر محرك MedOrqis.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'metformin', 'standard_dose': '2000 mg/day', 'crcl_or_egfr': 35.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"metformin\", \"crcl_or_egfr\": 35.0, \"max_safe_dose_mg_day\": 1000, \"recommendation\": \"Reduce dose to maximum 1000 mg/day (500 mg BID)\", \"monitoring_interval_months\": 3}"},
            {"role": "assistant", "content": "ضبط جرعة الميتفورمين وفق معايير الجمعية الأمريكية للسكري وKDIGO 2024:\n\n1. تصنيف وظائف الكلى:\n- معدل الترشيح 35 مل/دقيقة يضع المريض في المرحلة (Stage 3b) من القصور الكلوي المتوسط إلى الشديد (30-44 مل/دقيقة).\n\n2. تعديل الجرعة الإلزامي:\n- الجرعة الحالية (2000 ملغ/يوم) مرتفعة وخطيرة.\n- السقف الأقصى المسموح به هو 1000 ملغ في اليوم فقط (مثلاً 500 ملغ مرتين يومياً مع الوجبات).\n\n3. بروتوكول المتابعة:\n- فحص وظائف الكلى كل 3 أشهر بانتظام.\n- تنبيه المريض بإيقاف الدواء فوراً والتواصل مع الطبيب في حالات الجفاف، النزلات المعوية الحادة، أو قبل إجراء أشعة بالصبغة بـ 48 ساعة."}
        ]
    },
    {
        "id": "medorqis-renal-apixaban-esrd-en-067",
        "language": "en",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "An 82-year-old male with atrial fibrillation has severe end-stage renal disease (CrCl 12 mL/min, not on dialysis). A junior doctor prescribed Apixaban 5 mg BID. Evaluate this prescription."},
            {"role": "assistant", "content": "I will evaluate direct oral anticoagulant safety in end-stage renal disease using the MedOrqis renal safety engine.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'apixaban', 'standard_dose': '5 mg BID', 'crcl_or_egfr': 12.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"apixaban\", \"crcl_or_egfr\": 12.0, \"contraindicated\": true, \"recommendation\": \"Avoid DOACs in non-dialysis ESRD CrCl < 15 mL/min; consider dose-adjusted Warfarin or UFH\", \"bleeding_risk\": \"VERY_HIGH\"}"},
            {"role": "assistant", "content": "[CRITICAL ANTICOAGULATION SAFETY ALERT]\nBased on 2024 ESC and KDIGO Anticoagulation Guidelines:\n\n- Patient CrCl: 12 mL/min represents non-dialysis dependent End-Stage Renal Disease (CrCl < 15 mL/min).\n- Clinical Evaluation: Apixaban 5 mg BID in this setting is DANGEROUS and CONTRAINDICATED in European guidelines due to unmonitored drug accumulation and lethal bleeding risk.\n\nRecommended Clinical Strategy:\n1. Cancel Apixaban 5 mg BID.\n2. In severe non-dialysis ESRD (CrCl < 15 mL/min), DOACs lack randomized trial efficacy and safety data. The guideline-established option is dose-adjusted Warfarin (target INR 2.0 - 3.0 with frequent monitoring) or multidisciplinary evaluation of left atrial appendage occlusion (LAAO).\n3. If US FDA labeling is cited (permitting 5 mg or 2.5 mg BID), European and international consensus strictly advises avoidance without active hemodialysis clearance."}
        ]
    },
    {
        "id": "medorqis-renal-apixaban-elderly-ar-068",
        "language": "ar",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض عمره 82 سنة ووزنه 58 كغ ويعاني من رجفان أذيني. الكرياتينين في المصل لديه 1.8 ملغ/ديسيلتر. هل يحصل على إيليكويس (Apixaban) بالجرعة الكاملة 5 ملغ مرتين يومياً؟"},
            {"role": "assistant", "content": "سأقوم بفحص معايير تخفيض جرعة أبيكسابان الثلاثية وفق إرشادات جمعية القلب الأوروبية ESC 2024.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'apixaban', 'standard_dose': '5 mg BID', 'crcl_or_egfr': 28.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"apixaban\", \"patient_criteria_met\": [\"Age >= 80 (82yo)\", \"Weight <= 60kg (58kg)\", \"Serum Creatinine >= 1.5 (1.8 mg/dL)\"], \"dose_reduction_indicated\": true, \"adjusted_dose\": \"2.5 mg orally twice daily\"}"},
            {"role": "assistant", "content": "تعديل جرعة إيليكويس (Apixaban) وفق معايير جمعية القلب الأوروبية ESC 2024:\n\n1. تقييم معايير تخفيض الجرعة (تتطلب توفر 2 على الأقل من 3 معايير):\n- العمر: 82 سنة (يحقق شرط >= 80 سنة).\n- الوزن: 58 كغ (يحقق شرط <= 60 كغ).\n- الكرياتينين: 1.8 ملغ/ديسيلتر (يحقق شرط >= 1.5 ملغ/ديسيلتر).\n- المريض يحقق المعايير الثلاثة جميعها.\n\n2. الجرعة المعتمدة للسلامة:\n- تخفيض الجرعة إجبارياً إلى: 2.5 ملغ عن طريق الفم مرتين يومياً (بدلاً من 5 ملغ مرتين يومياً).\n\nتحذير سريري:\nإعطاء الجرعة الكاملة 5 ملغ مرتين يومياً لمريض يستوفي هذه المعايير يرفع خطر حدوث نزيف دماغي أو هضمي شديد بنسبة تتجاوز 4 أضعاف."}
        ]
    },
    {
        "id": "medorqis-renal-colchicine-gout-en-069",
        "language": "en",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 70-year-old male with acute gout flare has chronic kidney disease with CrCl 25 mL/min. How should oral colchicine be dosed safely?"},
            {"role": "assistant", "content": "I will calculate guideline-grounded colchicine dosage adjustments for severe renal impairment using MedOrqis deterministic renal tool.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'colchicine', 'standard_dose': '1.2 mg then 0.6 mg in 1 hour', 'crcl_or_egfr': 25.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"colchicine\", \"crcl_or_egfr\": 25.0, \"adjusted_regimen\": \"0.5 mg - 0.6 mg single dose, do not repeat for at least 14 days; consider intra-articular steroid\", \"risk\": \"Neuromyopathy, bone marrow suppression, and fatal toxicity\"}"},
            {"role": "assistant", "content": "[CRITICAL TOXICOLOGY ALERT: COLCHICINE IN RENAL IMPAIRMENT]\nBased on American College of Rheumatology (ACR) and FDA Guidelines:\n\n- Patient CrCl: 25 mL/min (<30 mL/min represents severe impairment).\n- Standard Acute Flare Regimen (1.2 mg followed by 0.6 mg 1 hour later) is DANGEROUS in severe renal disease due to delayed clearance.\n\nAdjusted Guideline Regimen:\n1. Administer a single dose of 0.5 mg to 0.6 mg ONLY. Do NOT repeat for at least 2 weeks (14 days).\n2. Preferred Alternative: In acute monoarticular gout with severe renal impairment, intra-articular corticosteroid injection or a short course of oral prednisone (e.g. 20-30 mg daily tapered over 5-10 days) is far safer than colchicine or NSAIDs.\n3. Absolute Contraindication: Never combine colchicine with strong CYP3A4 inhibitors (e.g. Clarithromycin, Ketoconazole) or P-gp inhibitors in renal patients—this combination has caused multiple reported fatalities from multi-organ failure."}
        ]
    },
    {
        "id": "medorqis-renal-colchicine-gout-ar-070",
        "language": "ar",
        "domain": "renal_dosing",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض مصاب بقصور كلوي مزمن مع تصفية كلوية 20 مل/دقيقة، أصيب بنوبة نقرس حادة في إصبع قدمه. هل يجوز إعطاؤه كولشيسين بالجرعة المعتادة؟"},
            {"role": "assistant", "content": "سأقوم بفحص محاذير وجرعات الكولشيسين في القصور الكلوي الشديد وفق إرشادات الكلية الأمريكية لأمراض الروماتيزم.", "tool_calls": [{'type': 'function', 'function': {'name': 'adjust_renal_drug_dose', 'arguments': {'drug_name': 'colchicine', 'standard_dose': '1 mg then 0.5 mg in 1 hour', 'crcl_or_egfr': 20.0, 'is_dialysis': False}}}]},
            {"role": "tool", "name": "adjust_renal_drug_dose", "content": "{\"drug_name\": \"colchicine\", \"crcl_or_egfr\": 20.0, \"adjusted_regimen\": \"0.5 mg single dose only, do not repeat course within 14 days\", \"preferred_alternative\": \"Prednisolone or intra-articular steroid\"}"},
            {"role": "assistant", "content": "توجيهات علاج نوبة النقرس في القصور الكلوي الشديد (CrCl 20 مل/دقيقة):\n\n1. خطورة الكولشيسين المعتاد:\n- لا يجوز إطلاقاً إعطاء الكولشيسين بنظامه المعتاد؛ بطء التخلص من الدواء يؤدي إلى تراكمه مسبباً اعتلالاً عضلياً وعصبياً وتثبيطاً شديداً لنخاع العظم قد ينتهي بالوفاة.\n\n2. الجرعة الاستثنائية عند الضرورة القصوى:\n- جرعة وحيدة فقط 0.5 ملغ ولا تكرر الجرعة إطلاقاً قبل مرور أسبوعين (14 يوماً) كاملين.\n\n3. الخيار الأول الموصى به سريرياً:\n- تفضيل الكورتيكوستيرويدات: حقن المفصل موضعياً بالكورتيزون، أو إعطاء كورس قصير من بريدنيزولون عن طريق الفم (20-30 ملغ/يوم مع تخفيض تدريجي خلال أسبوع إلى 10 أيام).\n- يمنع استخدام مضادات الالتهاب غير الستيرويدية (NSAIDs مثل فولتارين أو بروفين) تماماً لتفادي التدهور الحاد في الكلى."}
        ]
    },
    {
        "id": "medorqis-peds-ibuprofen-ceiling-en-071",
        "language": "peds_ceiling",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 12-year-old child weighing 55 kg presents with an acute sprained ankle. The formula recommends ibuprofen 10 mg/kg per dose. What exact single dose should be prescribed?"},
            {"role": "assistant", "content": "I will calculate the pediatric weight-based dose and enforce mandatory adult single-dose ceiling constraints.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_pediatric_weight_dose', 'arguments': {'age_years': 12.0, 'weight_kg': 55.0, 'dose_per_kg': 10.0, 'max_single_adult_dose_mg': 400.0, 'dose_unit': 'mg'}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": "{\"age_years\": 12.0, \"weight_kg\": 55.0, \"calculated_raw_dose\": 550.0, \"max_single_adult_dose_mg\": 400.0, \"safe_prescribed_dose\": 400.0, \"ceiling_applied\": true, \"reduction_amount\": 150.0}"},
            {"role": "assistant", "content": "[PEDIATRIC SAFETY INTERLOCK: ADULT CEILING ENFORCED]\nBased on AAP and British National Formulary for Children (BNFC) Guidelines:\n\n- Raw Mathematical Dose: 55 kg * 10 mg/kg = 550 mg.\n- Mandatory Adult Single-Dose Ceiling: 400 mg.\n- Verified Safe Prescribed Dose: 400 mg orally every 6 to 8 hours with food as needed (maximum 1200 mg/day).\n\nClinical Safety Rationale:\nIn overweight and older pediatric patients, direct weight-based multiplication yields doses exceeding standard adult therapeutic levels. Prescribing 550 mg creates unneeded risks of gastric ulceration and acute kidney injury without added analgesia. The adult ceiling of 400 mg is non-negotiable."}
        ]
    },
    {
        "id": "medorqis-peds-ibuprofen-ceiling-ar-072",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "طفل عمره 11 سنة ووزنه 50 كغ يعاني من ألم أسنان حاد. الطبيب يريد إعطاءه إيبوبروفين بجرعة 10 ملغ/كغ. كم الجرعة الآمنة للجرعة الواحدة؟"},
            {"role": "assistant", "content": "سأقوم بحساب جرعة الإيبوبروفين للأطفال وفرض سقف أقصى للبالغين لمنع التسمم الدوائي.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_pediatric_weight_dose', 'arguments': {'age_years': 11.0, 'weight_kg': 50.0, 'dose_per_kg': 10.0, 'max_single_adult_dose_mg': 400.0, 'dose_unit': 'mg'}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": "{\"age_years\": 11.0, \"weight_kg\": 50.0, \"calculated_raw_dose\": 500.0, \"max_single_adult_dose_mg\": 400.0, \"safe_prescribed_dose\": 400.0, \"ceiling_applied\": true}"},
            {"role": "assistant", "content": "[تطبيق سقف الأمان للبالغين: منع الجرعة الزائدة]\nوفقاً للإرشادات الدولية لطب الأطفال (AAP & BNF for Children):\n\n1. الحساب الرياضي النظري:\n- 50 كغ * 10 ملغ/كغ = 500 ملغ.\n\n2. سقف الأمان الصارم للبالغين:\n- الحد الأقصى للجرعة الواحدة من الإيبوبروفين هو 400 ملغ.\n\n3. الجرعة السريرية المعتمدة:\n- 400 ملغ عن طريق الفم كل 6 إلى 8 ساعات بعد الأكل عند اللزوم (بحد أقصى 1200 ملغ في اليوم).\n\nتحذير سريري هام:\nإعطاء 500 ملغ لطفل بعمر 11 سنة يتجاوز الجرعة المعيارية للبالغين دون أي فائدة تسكين إضافية، ويزيد بدرجة كبيرة من احتمالية التهاب المعدة والقصور الكلوي المؤقت."}
        ]
    },
    {
        "id": "medorqis-peds-paracetamol-ceiling-en-073",
        "language": "en",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 15-year-old adolescent weighing 75 kg presents with fever and pharyngitis. Calculate his single dose of paracetamol based on 15 mg/kg."},
            {"role": "assistant", "content": "I will calculate weight-based paracetamol dosing and enforce the 1000 mg adult single-dose ceiling.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_pediatric_weight_dose', 'arguments': {'age_years': 15.0, 'weight_kg': 75.0, 'dose_per_kg': 15.0, 'max_single_adult_dose_mg': 1000.0, 'dose_unit': 'mg'}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": "{\"age_years\": 15.0, \"weight_kg\": 75.0, \"calculated_raw_dose\": 1125.0, \"max_single_adult_dose_mg\": 1000.0, \"safe_prescribed_dose\": 1000.0, \"ceiling_applied\": true, \"reduction_amount\": 125.0}"},
            {"role": "assistant", "content": "[PEDIATRIC OVERDOSE PREVENTION: HEPATOTOXICITY GUARD]\nBased on Pediatric Pharmacology Guidelines:\n\n- Raw Mathematical Dose: 75 kg * 15 mg/kg = 1125 mg.\n- Hard Adult Ceiling Limit: 1000 mg (1.0 g) per single dose.\n- Verified Safe Prescribed Dose: 1000 mg orally every 4 to 6 hours as needed (maximum 4000 mg/24h).\n\nClinical Guardrail:\nSingle doses of acetaminophen exceeding 1000 mg saturate glutathione pathways and increase the production of the toxic metabolite NAPQI, introducing acute liver injury risks. The adult ceiling of 1000 mg must never be breached regardless of body weight."}
        ]
    },
    {
        "id": "medorqis-peds-paracetamol-ceiling-ar-074",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مراهق عمره 14 سنة يعاني من سمنة ووزنه 80 كغ لديه حمى مرتفعة. كم جرعة الباراسيتامول (15 ملغ/كغ) التي يجب أن يأخذها؟"},
            {"role": "assistant", "content": "سأقوم بحساب جرعة الباراسيتامول للمراهق وفرض سقف الجرعة القصوى للبالغين لحماية الكبد.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_pediatric_weight_dose', 'arguments': {'age_years': 14.0, 'weight_kg': 80.0, 'dose_per_kg': 15.0, 'max_single_adult_dose_mg': 1000.0, 'dose_unit': 'mg'}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": "{\"age_years\": 14.0, \"weight_kg\": 80.0, \"calculated_raw_dose\": 1200.0, \"max_single_adult_dose_mg\": 1000.0, \"safe_prescribed_dose\": 1000.0, \"ceiling_applied\": true}"},
            {"role": "assistant", "content": "[حماية الكبد: تطبيق السقف الأقصى للجرعة]\nوفقاً للإرشادات الدولية لسلامة أدوية الأطفال واليافعين:\n\n1. الحساب النظري بالوزن:\n- 80 كغ * 15 ملغ/كغ = 1200 ملغ للجرعة.\n\n2. سقف الجرعة الإلزامي للبالغين:\n- الحد الأقصى المطلق للجرعة الواحدة هو 1000 ملغ (1 غرام).\n\n3. الجرعة المعتمدة للسلامة:\n- 1000 ملغ (قرصان عيار 500 ملغ) كل 4 إلى 6 ساعات عند اللزوم، على ألا يتجاوز المجموع اليومي 4000 ملغ (4 غرامات) خلال 24 ساعة.\n\nتنبيه سريري:\nتجاوز 1000 ملغ في الجرعة الواحدة يهدد باستنزاف الجلوتاثيون وتراكم مركب NAPQI السام المؤدي إلى تنخر خلايا الكبد الحاد."}
        ]
    },
    {
        "id": "medorqis-peds-amox-ceiling-en-075",
        "language": "en",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 9-year-old child weighing 42 kg has acute bilateral otitis media. High-dose amoxicillin is recommended at 90 mg/kg/day divided BID. What daily and single dose should be given?"},
            {"role": "assistant", "content": "I will evaluate high-dose amoxicillin dosing and apply pediatric ceiling limits for acute otitis media.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_pediatric_weight_dose', 'arguments': {'age_years': 9.0, 'weight_kg': 42.0, 'dose_per_kg': 45.0, 'max_single_adult_dose_mg': 1000.0, 'dose_unit': 'mg'}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": "{\"age_years\": 9.0, \"weight_kg\": 42.0, \"calculated_raw_dose\": 1890.0, \"max_single_adult_dose_mg\": 1000.0, \"safe_prescribed_dose\": 1000.0, \"ceiling_applied\": true}"},
            {"role": "assistant", "content": "[PEDIATRIC ANTIMICROBIAL DOSING CEILING]\nBased on American Academy of Pediatrics (AAP) Otitis Media Guidelines:\n\n- Raw Mathematical Daily Dose: 42 kg * 90 mg/kg/day = 3780 mg/day (1890 mg BID).\n- Maximum Recommended Pediatric/Adult Daily Ceiling: 2000 to 3000 mg/day (1000 mg BID).\n- Safe Prescribed Regimen: Amoxicillin 1000 mg orally every 12 hours (2000 mg/day total) for 10 days.\n\nPharmacological Guardrail:\nDirect weight multiplication in heavier children can produce staggering doses (>3.5 grams/day). Doses above 2 to 3 grams daily do not enhance middle-ear penetration against Streptococcus pneumoniae and cause severe diarrhea, Clostridioides difficile colitis, and rash. The 1000 mg BID ceiling must be observed."}
        ]
    },
    {
        "id": "medorqis-peds-amox-ceiling-ar-076",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "طفل عمره 8 سنوات وزنه 38 كغ مصاب بالتهاب أذن وسطى حاد موصوف له أموكسيسيلين بجرعة عالية 90 ملغ/كغ/يوم. كيف نحدد الجرعة اليومية دون تجاوز السقف الآمن؟"},
            {"role": "assistant", "content": "سأقوم بحساب جرعة الأموكسيسيلين العالية وضبط السقف اليومي الآمن للأطفال.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_pediatric_weight_dose', 'arguments': {'age_years': 8.0, 'weight_kg': 38.0, 'dose_per_kg': 45.0, 'max_single_adult_dose_mg': 1000.0, 'dose_unit': 'mg'}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": "{\"age_years\": 8.0, \"weight_kg\": 38.0, \"calculated_raw_dose\": 1710.0, \"max_single_adult_dose_mg\": 1000.0, \"safe_prescribed_dose\": 1000.0, \"ceiling_applied\": true}"},
            {"role": "assistant", "content": "جرعة أموكسيسيلين الآمنة لالتهاب الأذن الوسطى (AAP Guidelines):\n\n1. الحساب النظري:\n- 38 كغ * 90 ملغ/كغ/يوم = 3420 ملغ باليوم (1710 ملغ كل 12 ساعة).\n\n2. تطبيق سقف الأمان الدوائي:\n- السقف الأقصى المعتمد لجرعة الأموكسيسيلين في الأطفال والبالغين هو 1000 ملغ للجرعة الواحدة (2000 إلى 3000 ملغ/يوم كحد أقصى).\n\n3. الوصفة العلاجية المعتمدة:\n- 1000 ملغ (1 غرام) بالفم كل 12 ساعة مع الوجبات لمدة 10 أيام.\n\nتنبيه للوقاية من التسمم:\nتجاوز 3 غرامات يومياً لا يضيف أي فعالية إضافية على بكتيريا المكورات الرئوية، بل يسبب إسهالاً حاداً وطفحاً جلدياً واضطراباً في الميكروبيوتا المعوية."}
        ]
    },
    {
        "id": "medorqis-peds-ceftriaxone-neonate-en-077",
        "language": "en",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 14-day-old neonate in the NICU has suspected sepsis and is receiving parenteral calcium gluconate for hypocalcemia. The resident wants to order intravenous Ceftriaxone. Is this safe?"},
            {"role": "assistant", "content": "I will evaluate neonatal antibiotic safety guardrails and contraindications.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['Neonate 14 days old', 'Receiving IV calcium gluconate', 'Proposed ceftriaxone IV']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"CONTRAINDICATION_FATAL_PRECIPITATION\", \"guideline\": \"FDA Black Box & WHO Pediatric Guidelines\", \"action\": \"DO_NOT_ADMINISTER\", \"alternative\": \"Cefotaxime + Ampicillin\"}"},
            {"role": "assistant", "content": "[FATAL DRUG CONTRAINDICATION: FDA BLACK BOX ALERT]\nGuideline Verdict: CEFTRIAXONE IS ABSOLUTELY CONTRAINDICATED.\n\nPathophysiological Mechanism:\n1. Calcium-Ceftriaxone Precipitation: Concomitant administration of ceftriaxone and calcium-containing solutions in neonates (<=28 days) causes insoluble crystalline precipitation in the lungs and kidneys, resulting in fatal cardiopulmonary and renal embolization.\n2. Biliary Sludging & Kernicterus: Ceftriaxone displaces bilirubin from serum albumin, sharply increasing the risk of bilirubin encephalopathy (kernicterus) in neonates.\n\nMandated Neonatal Alternative:\nUse Cefotaxime (50 mg/kg IV q8-12h) plus Ampicillin (50-100 mg/kg IV q8-12h). Cefotaxime has zero calcium precipitation risk and does not displace bilirubin."}
        ]
    },
    {
        "id": "medorqis-peds-ceftriaxone-neonate-ar-078",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "حديث ولادة عمره 12 يوماً في الحضانة يعالج من نقص الكالسيوم بمحلول جلوكونات الكالسيوم بالوريد. هل يجوز إعطاؤه حقنة سيفترياكسون وريدي لاشتباه تسمم الدم؟"},
            {"role": "assistant", "content": "سأقوم بفحص موانع الاستعمال الصارمة للسيفترياكسون لدى حديثي الولادة عبر محرك MedOrqis.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['حديث ولادة عمره 12 يوماً', 'محلول جلوكونات الكالسيوم الوريدي', 'اقتراح حقن سيفترياكسون']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"حظر مطلق ومميت\", \"reason\": \"ترسيب بلورات الكالسيوم في الرئتين والكلى\", \"بديل\": \"سيفوتاكسيم + أمبيسيلين\"}"},
            {"role": "assistant", "content": "[تحذير أسود عاجل: حظر استخدام السيفترياكسون لحديثي الولادة]\nوفقاً لتحذيرات هيئة الغذاء والدواء الأمريكية (FDA Black Box Warning) ومنظمة الصحة العالمية:\n\n1. المنع المطلق:\n- يحظر استخدام السيفترياكسون (Ceftriaxone) نهائياً لأي رضيع يقل عمره عن 28 يوماً، ويتضاعف الخطر القاتل في حال تلقي أي محاليل تحتوي على الكالسيوم.\n\n2. سبب الخطورة القاتلة:\n- السيفترياكسون يتحد فوراً مع الكالسيوم مكوناً بلورات غير قابلة للذوبان تترسب في الأوعية الدموية للرئتين والكليتين، مسببة انسدادات قاتلة ومفاجئة.\n- يزيح السيفترياكسون البيليروبين عن الألبومين، مما يرفع خطر اليرقان النووي (تلف خلايا الدماغ Kernicterus).\n\n3. البديل السريري الآمن والمعتمد بالحضانة:\n- استخدام سيفوتاكسيم (Cefotaxime) مع أمبيسيلين (Ampicillin)، حيث لا يتفاعل السيفوتاكسيم مع الكالسيوم وآمن تماماً لحديثي الولادة."}
        ]
    },
    {
        "id": "medorqis-peds-codeine-tonsil-en-079",
        "language": "en",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 6-year-old child undergoes adenotonsillectomy for obstructive sleep apnea. The discharge prescription includes oral codeine for pain relief. Assess safety."},
            {"role": "assistant", "content": "I will screen the pediatric prescription against FDA Black Box contraindications for opioid metabolism.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['Child 6 years old', 'Post-tonsillectomy/adenoidectomy', 'Prescribed codeine']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"BLACK_BOX_CONTRAINDICATION\", \"regulatory_agency\": \"FDA & EMA\", \"risk\": \"Ultra-rapid CYP2D6 metabolism causing fatal respiratory arrest\", \"action\": \"CANCEL_PRESCRIPTION\"}"},
            {"role": "assistant", "content": "[FDA & EMA BLACK BOX CONTRAINDICATION: CODEINE IN PEDIATRICS]\nGuideline Verdict: CODEINE IS STRICTLY BANNED POST-TONSILLECTOMY IN CHILDREN.\n\nPharmacogenetic Rationale:\n1. Codeine is a prodrug converted to morphine by hepatic CYP2D6. Children who are CYP2D6 ultra-rapid metabolizers (up to 10% of Caucasians, 20% of Middle Easterners/Africans) produce unpredictably high morphine levels rapidly, resulting in fatal respiratory arrest during sleep.\n2. In 2013-2018, the FDA and EMA issued mandatory black box contraindications banning codeine and tramadol in all children under 12, and in all children under 18 following tonsillectomy or adenoidectomy.\n\nSafe Analgesic Protocol:\nPrescribe scheduled alternating Paracetamol (15 mg/kg q6h, max 1000 mg) and Ibuprofen (10 mg/kg q8h, max 400 mg) with hydration."}
        ]
    },
    {
        "id": "medorqis-peds-codeine-tonsil-ar-080",
        "language": "ar",
        "domain": "pediatrics",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "طفل عمره 7 سنوات أجرى عملية استئصال اللوزتين واللحمية بسبب الشخير وانقطاع التنفس. كتب الطبيب شراب كودايين لتسكين الألم. هل هذا الدواء آمن للطفل؟"},
            {"role": "assistant", "content": "سأقوم بفحص سلامة الكودايين الجينية للأطفال بعد جراحة اللوزتين عبر محرك MedOrqis.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['طفل عمره 7 سنوات', 'بعد استئصال اللوزتين واللحمية', 'وصف شراب كودايين']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"حظر دولي مطلق FDA Black Box\", \"risk\": \"توقف التنفس المفاجئ والوفاة أثناء النوم\", \"بديل\": \"باراسيتامول مع إيبوبروفين\"}"},
            {"role": "assistant", "content": "[تحذير أسود عاجل: حظر إعطاء الكودايين للأطفال بعد اللوزتين]\nوفقاً للتحذيرات الإلزامية من هيئة الغذاء والدواء الأمريكية (FDA) ووكالة الأدوية الأوروبية (EMA):\n\n1. الحظر المطلق:\n- يمنع منعاً باتاً إعطاء الكودايين (أو الترامادول) للأطفال دون سن 12 عاماً، ولجميع الأطفال واليافعين دون سن 18 عاماً بعد جراحات اللوزتين واللحمية.\n\n2. التفسير الدوائي والجيني للوفاة:\n- الكودايين يتحول إلى مورفين في الكبد عبر إنزيم CYP2D6. نسبة كبيرة من الأطفال (خاصة في الشرق الأوسط) لديهم نشاط إنزيمي فائق السرعة، مما يحول الكودايين في أجسادهم فوراً وبجرعات عالية إلى مورفين يثبط مركز التنفس ويسبب الوفاة خنقاً أثناء النوم.\n\n3. البديل المسكن الآمن والمعتمد:\n- الاعتماد على التناوب بين الباراسيتامول (15 ملغ/كغ كل 6 ساعات) والإيبوبروفين (10 ملغ/كغ كل 8 ساعات) مع كثرة السوائل الباردة."}
        ]
    },
    {
        "id": "medorqis-ddi-triple-whammy-en-081",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 74-year-old hypertensive patient takes Enalapril 20 mg and Furosemide 40 mg daily. For knee osteoarthritis, he starts taking Ibuprofen 600 mg three times daily. Screen for pharmacological interactions."},
            {"role": "assistant", "content": "I will screen the medication regimen for life-threatening nephrotoxic drug-drug interactions using MedOrqis DDI rules.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['enalapril', 'furosemide', 'ibuprofen']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"FATAL_TRIPLE_WHAMMY\", \"severity\": \"CRITICAL\", \"mechanism\": \"ACEi (efferent arteriole vasodilation) + Diuretic (hypovolemia/reduced renal plasma flow) + NSAID (afferent arteriole vasoconstriction via prostaglandin inhibition)\", \"clinical_outcome\": \"Acute decompensated renal failure (AKI), hyperkalemia\"}"},
            {"role": "assistant", "content": "[CRITICAL NEPHROTOXICITY ALERT: THE TRIPLE WHAMMY]\nInteraction Classification: Severity Level 1 (Severe / Avoid Combination).\n\nPathophysiologic Hemodynamic Collapse:\n1. Diuretic (Furosemide): Reduces effective circulating volume and renal perfusion.\n2. NSAID (Ibuprofen): Blocks cyclooxygenase and renal prostaglandins, preventing compensatory afferent arteriole vasodilation.\n3. ACE-inhibitor (Enalapril): Inhibits angiotensin II, causing marked efferent arteriole dilation.\nResult: Trans-glomerular hydrostatic pressure plummets, causing precipitous GFR collapse, oliguric Acute Kidney Injury (AKI), and life-threatening hyperkalemia.\n\nMandated Interventions:\n1. Discontinue Ibuprofen immediately.\n2. Substitute with topical NSAIDs (e.g. Diclofenac gel) or oral Paracetamol (up to 3 g/day) for knee pain.\n3. Check urgent serum creatinine, urea, and potassium levels."}
        ]
    },
    {
        "id": "medorqis-ddi-triple-whammy-ar-082",
        "language": "ar",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض ضغط عمره 70 سنة يتناول راميبريل (Triatec) مع مدر للبول هيدروكلوروثيازيد. بسبب وجع المفاصل، بدأ يتناول ديكلوفيناك (فولتارين 50 ملغ 3 مرات يومياً). هل هذا المزيج آمن؟"},
            {"role": "assistant", "content": "سأقوم بفحص التداخلات الدوائية الثلاثية عالية الخطورة على الكلى عبر محرك MedOrqis.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['ramipril', 'hydrochlorothiazide', 'diclofenac']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"الضربة الثلاثية القاتلة على الكلى (Triple Whammy)\", \"خطورة\": \"حرجة جداً\", \"المضاعفات\": \"فشل كلوي حاد مفاجئ، ارتفاع بوتاسيوم الدم المميت\"}"},
            {"role": "assistant", "content": "[تحذير دوائي عاجل: الضربة الثلاثية على الكلى - Triple Whammy]\nتقييم التفاعل: خطورة حرجة من الدرجة الأولى.\n\nآلية الضرر السريري:\nهذا الثلاثي الدوائي يسمى طبياً 'الضربة الثلاثية' (The Triple Whammy):\n1. مدر البول (هيدروكلوروثيازيد): يقلل حجم السوائل في الأوعية الدموية المغذية للكلى.\n2. مسكن الفولتارين (ديكلوفيناك): يضيق الشريان الوارد المغذي للكبيبات الكلوية عبر تثبيط البروستاجلاندين.\n3. خافض الضغط راميبريل: يوسع الشريان الصادر من الكلية.\nالنتيجة المباشرة: انهيار مفاجئ في ضغط الترشيح الكلوي وحدوث فشل كلوي حاد (AKI) مصحوب بارتفاع خطير في البوتاسيوم.\n\nالإجراءات الإلزامية:\n1. إيقاف الفولتارين فوراً وعدم تناوله نهائياً مع أدوية الضغط هذه.\n2. استخدام بدائل آمنة للمفاصل مثل الباراسيتامول بجرعة محسوبة أو دهان فولتارين الموضعي.\n3. إجراء فحص دم عاجل لوظائف الكلى والبوتاسيوم."}
        ]
    },
    {
        "id": "medorqis-ddi-warfarin-cipro-en-083",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 68-year-old male on chronic Warfarin for a mechanical mitral valve is prescribed Ciprofloxacin 500 mg BID for acute prostatitis. Evaluate the hemorrhagic risk."},
            {"role": "assistant", "content": "I will screen the antimicrobial-anticoagulant combination for pharmacokinetic CYP interactions.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['warfarin', 'ciprofloxacin']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"MAJOR_HEMORRHAGE_RISK\", \"severity\": \"CRITICAL\", \"mechanism\": \"Potent CYP1A2 and CYP2C9 inhibition + eradication of intestinal vitamin K-producing microflora\", \"clinical_outcome\": \"Dramatic INR prolongation (>8.0), fatal retroperitoneal or intracranial bleeding\"}"},
            {"role": "assistant", "content": "[CRITICAL ANTICOAGULATION INTERACTION: WARFARIN + FLUOROQUINOLONE]\nGuideline Severity: CRITICAL / MAJOR BLEEDING RISK.\n\nPharmacokinetic & Pharmacodynamic Synergy:\n1. Enzyme Inhibition: Ciprofloxacin strongly inhibits CYP1A2 and CYP2C9, drastically impairing the clearance of the biologically potent S-enantiomer of warfarin.\n2. Microbiome Gut Effect: Fluoroquinolones eradicate enteric flora that synthesize Vitamin K, compounding anticoagulant sensitivity.\nClinical Result: INR frequently surges past 8.0 - 12.0 within 3-5 days, triggering catastrophic intracranial, gastrointestinal, or retroperitoneal hemorrhage.\n\nManagement Protocol:\n1. Prefer an alternative antibiotic that does not inhibit CYP2C9 (e.g. Ceftriaxone, or Nitrofurantoin/Fosfomycin if strictly simple cystitis).\n2. If ciprofloxacin is clinically mandatory, empirically reduce warfarin dose by 30-50% and check INR every 48 hours."}
        ]
    },
    {
        "id": "medorqis-ddi-warfarin-cipro-ar-084",
        "language": "ar",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض مركب صمام قلب صناعي يتناول وارفارين (ماريفان 5 ملغ). أصيب بالتهاب مسالك بولية ووصف له الطبيب سيبروفلوكساسين 500 ملغ. ما خطورة هذا التفاعل؟"},
            {"role": "assistant", "content": "سأقوم بفحص التداخل بين الوارفارين والمضادات الحيوية المثبطة للإنزيمات الكبدية.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['warfarin', 'ciprofloxacin']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"خطر نزيف حاد ومميت\", \"آلية\": \"تثبيط إنزيمات الكبد CYP2C9 والقضاء على بكتيريا فيتامين K\", \"النتيجة\": \"ارتفاع INR لأكثر من 8 وحدوث نزيف دماغي أو معوي\"}"},
            {"role": "assistant", "content": "[تحذير دوائي حرج: تفاعل الوارفارين مع السيبروفلوكساسين]\nمستوى الخطورة: خطورة شديدة مهددة للحياة.\n\nالتأثير الدوائي المركب:\n1. السيبروفلوكساسين يثبط بشدة إنزيمات الكبد (CYP1A2 وCYP2C9) المسؤولة عن تكسير الوارفارين، مما يؤدي إلى تراكم الوارفارين في الدم.\n2. يقضي المضاد على بكتيريا الأمعاء الطبيعية المصنعة لفيتامين K، مما يضاعف مفعول التمييع.\nالنتيجة: ارتفاع مفاجئ في تحليل السيولة (INR) إلى أرقام خطيرة (>8.0)، مما يسبب نزيفاً داخلياً أو نزيفاً في الدماغ.\n\nالتوصيات السريرية العاجلة:\n1. تغيير المضاد الحيوي إلى خيار آخر لا يتعارض مع إنزيمات الوارفارين إذا أمكن.\n2. في حال تعذر التغيير، يجب تخفيض جرعة الوارفارين بنسبة 30% إلى 50% وفحص تحليل السيولة (INR) كل 48 ساعة حتى استكمال العلاج."}
        ]
    },
    {
        "id": "medorqis-ddi-clopidogrel-omeprazole-en-085",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 62-year-old male with a drug-eluting stent placed 2 months ago takes Clopidogrel 75 mg daily. For dyspepsia, his primary care doctor adds Omeprazole 40 mg daily. Evaluate this combination."},
            {"role": "assistant", "content": "I will evaluate clopidogrel bioactivation against proton pump inhibitor CYP2C19 interactions.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['clopidogrel', 'omeprazole']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"LOSS_OF_ANTIPLATELET_EFFICACY\", \"severity\": \"HIGH\", \"mechanism\": \"Omeprazole competitive inhibition of CYP2C19 prevents clopidogrel prodrug bioactivation\", \"clinical_outcome\": \"Acute stent thrombosis, recurrent myocardial infarction\", \"recommendation\": \"Switch to Pantoprazole\"}"},
            {"role": "assistant", "content": "[HIGH-ALERT PHARMACOGENETIC INTERACTION: CLOPIDOGREL + OMEPRAZOLE]\nGuideline Severity: HIGH (FDA Black Box & ACC/AHA Stent Guidelines).\n\nPharmacological Mechanism:\nClopidogrel is an inactive prodrug requiring two-step hepatic oxidation, primarily mediated by CYP2C19, to generate its active thiol metabolite that irreversibly blocks the P2Y12 platelet receptor. Omeprazole and Esomeprazole are potent competitive inhibitors of CYP2C19, reducing active clopidogrel metabolite formation by ~45%, leading to antiplatelet failure and acute coronary stent thrombosis.\n\nMandated Clinical Action:\n1. Discontinue Omeprazole immediately.\n2. Switch to Pantoprazole (40 mg daily) or Rabeprazole. Pantoprazole has minimal affinity for CYP2C19 and does not attenuate clopidogrel's clinical antiplatelet action."}
        ]
    },
    {
        "id": "medorqis-ddi-clopidogrel-omeprazole-ar-086",
        "language": "ar",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض مركب دعامات دوائية بالقلب منذ شهرين ويتناول بلافيكس (Clopidogrel 75mg). بدأ يشتكي من حموضة فوصف له أوميبرازول 40 ملغ (أوميز). هل هذا الاختيار سليم؟"},
            {"role": "assistant", "content": "سأقوم بفحص تعارض الأوميبرازول مع تنشيط البلافيكس عبر محرك MedOrqis.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['clopidogrel', 'omeprazole']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"فشل فاعلية بلافيكس وخطر انسداد الدعامة\", \"آلية\": \"تثبيط إنزيم CYP2C19 المسؤول عن تنشيط كلوبيدوجريل\", \"البديل الآمن\": \"بانتوبرازول (كونترولوك)\"}"},
            {"role": "assistant", "content": "[تنبيه دوائي هام لمرضى دعامات القلب: تعارض بلافيكس مع أوميبرازول]\nالتقييم السريري: خطورة مرتفعة تمنع الجمع بينهما (FDA Black Box Warning).\n\nالسبب العلمي:\n- دواء بلافيكس (Clopidogrel) دواء خامل يحتاج إلى إنزيم كبدي (CYP2C19) ليحوله إلى المادة الفعالة المضادة لجلطات الصدمات.\n- الأوميبرازول (أوميز) يعطل هذا الإنزيم بالكامل، مما يقلل مفعول بلافيكس بنسبة تقارب 45% ويعرض دعامات القلب للانسداد المفاجئ بجلطة حادة.\n\nالإجراء الطبي الصحيح:\n1. إيقاف الأوميبرازول فوراً.\n2. استبداله بدواء بانتوبرازول (مثل كونترولوك Controloc 40mg)؛ حيث أثبتت الدراسات أن البانتوبرازول آمن ولا يتعارض مع تنشيط البلافيكس في الكبد."}
        ]
    },
    {
        "id": "medorqis-ddi-simva-clarithro-en-087",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 65-year-old female taking Simvastatin 40 mg daily for hyperlipidemia is diagnosed with community-acquired pneumonia and prescribed Clarithromycin 500 mg BID. Assess safety."},
            {"role": "assistant", "content": "I will screen the statin-macrolide combination for CYP3A4-mediated rhabdomyolysis hazards.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['simvastatin', 'clarithromycin']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"RHABDOMYOLYSIS_HAZARD\", \"severity\": \"CRITICAL\", \"mechanism\": \"Potent CYP3A4 inhibition increases simvastatin AUC by 10-fold\", \"clinical_outcome\": \"Severe skeletal muscle breakdown, acute tubular necrosis, myoglobinuric kidney failure\", \"action\": \"HOLD_SIMVASTATIN\"}"},
            {"role": "assistant", "content": "[CRITICAL STATIN TOXICITY INTERACTION: RHABDOMYOLYSIS]\nGuideline Severity: CRITICAL / CONTRAINDICATED (FDA & ACC/AHA Lipid Guidelines).\n\nPharmacological Interaction:\nSimvastatin is extensively metabolized by CYP3A4. Clarithromycin and Erythromycin are potent, irreversible mechanism-based inhibitors of CYP3A4. Concomitant use increases simvastatin plasma concentrations by up to 10-fold to 12-fold, precipitating massive skeletal muscle necrosis (Rhabdomyolysis) with myoglobinuria, severe hyperkalemia, and acute renal failure.\n\nMandated Action:\n1. Hold Simvastatin completely during the entire course of Clarithromycin, plus 3 days after completion.\n2. Alternative: Switch antibiotic to Azithromycin (which does not inhibit CYP3A4) or Amoxicillin/Clavulanate."}
        ]
    },
    {
        "id": "medorqis-ddi-simva-clarithro-ar-088",
        "language": "ar",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريضة تتناول سيمفاستاتين 40 ملغ يومياً لدهون الدم. أصيبت بالتهاب رئوي ووصف لها كلاريثرومايسين (كلاسيد 500 ملغ مرتين يومياً). هل تأخذ الدواءين معاً؟"},
            {"role": "assistant", "content": "سأقوم بفحص تداخل الستاتين مع المضادات الحيوية الماكروليدية عبر محرك MedOrqis.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['simvastatin', 'clarithromycin']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"خطر تحلل العضلات الحاد والفشل الكلوي (Rhabdomyolysis)\", \"آلية\": \"تثبيط إنزيم CYP3A4 يرفع تركيز سيمفاستاتين بعشرة أضعاف\", \"الإجراء\": \"إيقاف سيمفاستاتين مؤقتاً\"}"},
            {"role": "assistant", "content": "[تحذير دوائي شديد الخطورة: تحلل العضلات الحاد]\nمستوى الخطورة: حظر طبي كامل ومطلق الجمع بينهما (FDA Contraindication).\n\nالخطر السريري:\n- المضاد الحيوي كلاريثرومايسين (Klacid) يعطل إنزيم الكبد المسؤول عن تكسير سيمفاستاتين، مما يؤدي إلى ارتفاع تركيز الدواء في الدم بمقدار 10 إلى 12 ضعفاً.\n- هذا التراكم السام يؤدي إلى تحلل ألياف العضلات الهيكلية (Rhabdomyolysis)، ونزول بروتين الميوجلوبين في البول متسبباً في فشل كلوي حاد وانسداد قنوات الكلى.\n\nالقرار الطبي الصحيح:\n1. إيقاف سيمفاستاتين تماماً طوال فترة تناول الكلاسيد ولمدة 3 أيام بعد انتهائه.\n2. البديل المفضل: تغيير المضاد الحيوي إلى أزيثرومايسين (Zithromax) أو أموكسيسيلين/كلافولانات، حيث لا يتعارضان مع أدوية الكوليسترول."}
        ]
    },
    {
        "id": "medorqis-ddi-ssri-tramadol-en-089",
        "language": "en",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "A 34-year-old female on Escitalopram 20 mg daily for major depression visits urgent care with severe acute back pain. The physician prescribes Tramadol 100 mg three times daily. Screen for adverse events."},
            {"role": "assistant", "content": "I will screen the analgesic-antidepressant combination for Serotonin Syndrome and seizure risk.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['escitalopram', 'tramadol']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"SEROTONIN_SYNDROME_ALERT\", \"severity\": \"CRITICAL\", \"mechanism\": \"Additive central serotonergic enhancement (SSRI 5-HT reuptake inhibition + Tramadol 5-HT reuptake inhibition and release)\", \"clinical_outcome\": \"Serotonin syndrome: hyperthermia, ocular/inducible clonus, autonomic tremor, seizures\"}"},
            {"role": "assistant", "content": "[CRITICAL NEUROPSYCHIATRIC INTERACTION: SEROTONIN SYNDROME]\nGuideline Severity: CRITICAL / SEVERE (Hunter Toxicity Criteria for Serotonin Syndrome).\n\nPharmacological Synergy:\n1. Escitalopram is a potent Selective Serotonin Reuptake Inhibitor (SSRI).\n2. Tramadol possesses dual analgesic mechanisms: weak mu-opioid agonism combined with significant inhibition of serotonin and norepinephrine reuptake.\nConcomitant administration precipitates excessive synaptic serotonin accumulation in the CNS, triggering Serotonin Syndrome and lowering the seizure threshold.\n\nMandated Actions:\n1. Cancel Tramadol.\n2. Select alternative analgesics lacking serotonergic activity: Paracetamol, non-steroidal anti-inflammatory agents, or pure short-acting opioids (e.g. Codeine-free preparations or low-dose Morphine if indicated).\n3. Educate patient on early serotonin toxicity signs: tremors, shivering, myoclonus, agitation, diaphoresis."}
        ]
    },
    {
        "id": "medorqis-ddi-ssri-tramadol-ar-090",
        "language": "ar",
        "domain": "pharmacology",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريضة تتناول سبرالكس (Escitalopram 20mg) للاكتئاب والقلق. بسبب ألم شديد في الظهر وصف لها الطبيب ترامادول 100 ملغ. هل يمكن تناول المسكن بأمان؟"},
            {"role": "assistant", "content": "سأقوم بفحص مخاطر متلازمة السيروتونين والتشنجات العصبية الناتجة عن جمع الترامادول مع مضادات الاكتئاب.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_drug_interactions', 'arguments': {'medications': ['escitalopram', 'tramadol']}}}]},
            {"role": "tool", "name": "check_drug_interactions", "content": "{\"alert\": \"متلازمة السيروتونين المهددة للحياة (Serotonin Syndrome)\", \"الأعراض\": \"رعشة، تشنج عضلي، هياج، ارتفاع خطير بالحرارة وضغط الدم\", \"البديل\": \"تسكين غير سيروتونيني\"}"},
            {"role": "assistant", "content": "[تحذير دوائي عاجل: متلازمة السيروتونين القاتلة]\nمستوى الخطورة: خطورة حرجة وشديدة.\n\nالمخاطر الطبية للجمع بينهما:\n1. دواء سبرالكس (إسيتالوبرام) يرفع مستويات السيروتونين في الدماغ.\n2. الترامادول يعمل كمسكن وفي نفس الوقت يمنع إعادة امتصاص السيروتونين.\nالجمع بينهما يؤدي إلى تراكم مفرط وسمي للسيروتونين في الجهاز العصبي المركزي مسبباً متلازمة السيروتونين (Serotonin Syndrome)، وتشمل أعراضها: رجفان لا إرادي في العضلات (Clonus)، تعرق غزير، ارتفاع شديد في الحرارة، هياج، ونوبات تشنجية قد تنتهي بالوفاة.\n\nالإجراء الطبي الإلزامي:\n1. منع تناول الترامادول تماماً مع أدوية SSRI.\n2. استخدام مسكنات بديلة آمنة عصبياً (مثل الباراسيتامول بجرعة منتظمة، مضادات الالتهاب مع واقي معدة، أو باسط عضلات موضعي)."}
        ]
    },
    {
        "id": "medorqis-dialect-egypt-stemi-ar-091",
        "language": "ar",
        "domain": "emergency_dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض مصري عمره 56 سنة يقول: 'عندي حرقان نار في فم المعدة بقاله ساعتين، وسكاكين بتضرب في كتفي الشمال وظهري، وعرقان ومدوخ'. هل دا مجرد حموضة والتهاب معدة وأخد فوار؟"},
            {"role": "assistant", "content": "سأقوم بفحص الأعراض الوصفية باللهجة المصرية والتحقق من العلامات الحمراء لجلطة الشريان التاجي الحادة.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['حرقان فم المعدة ساعتين', 'ألم يمتد للكتف الأيسر والظهر كسكاكين', 'تعرق غزير ودوخة', 'مريض عمره 56 سنة']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"اشتباه جلطة قلبية حادة (Inferior STEMI / Acute Coronary Syndrome)\", \"level\": \"طوارئ قصوى فورا\", \"action\": \"تخطيط قلب عاجل ونقل بالإسعاف\"}"},
            {"role": "assistant", "content": "[EMERGENCY ESCALATION: اشتباه جلطة قلبية حادة]\nالتقييم السريري العاجل (رفض فرضية الحموضة البسيطة):\n\nالأعراض التي تصفها ('حرقان نار بفم المعدة يمتد للكتف الأيسر والظهر مصحوب بعرق بارد ودوخة') هي العرض الكلاسيكي والشائع لجلطة الجدار السفلي لعضلة القلب (Inferior Wall Myocardial Infarction)، وليست حموضة عادية.\n\nالتعليمات الطارئة المنقذة للحياة فوراً:\n1. الاتصال بالإسعاف أو التوجه فوراً لأقرب قسم طوارئ في مستشفى مجهز.\n2. إجراء تخطيط كهربية القلب (ECG) خلال 10 دقائق من الوصول وقياس إنزيمات القلب (Troponin).\n3. مضغ 4 أقراص أسبرين أطفال (300 ملغ) فوراً مع قرص نيتروجلسرين تحت اللسان (إذا لم يكن هناك هبوط بالضغط) بعد استشارة الطوارئ.\n4. الامتناع التام عن قيادة السيارة بنفسك أو الاكتفاء بالفوار ومضادات الحموضة."}
        ]
    },
    {
        "id": "medorqis-dialect-gulf-chf-ar-092",
        "language": "ar",
        "domain": "emergency_dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سعودي عمره 64 سنة يقول: 'صدري يكتم عليّ كل ما نمت على ظهري وأقوم مفجوع أكح، وفيه صوت تزييق مع بلغم فيه رغوة خفيفة، وسيقاني منفوخة'. هل هذا ربو شعبي عادي؟"},
            {"role": "assistant", "content": "سأقوم بفحص الأعراض الوصفية باللهجة الخليجية للكشف عن علامات هبوط القلب الاحتقاني والوذمة الرئوية الحادة.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['ضيق تنفس اضطجاعي (كتمة عند النوم)', 'ضيق تنفس انتيابي ليلي (يقوم مفجوع يكح)', 'بلغم رغوي', 'وذمة وتورم الساقين', 'تزييق بالصدر']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"فشل قلب احتقاني متدهور مع وذمة رئوية (Acute Pulmonary Edema)\", \"action\": \"طوارئ قلب فوراً\"}"},
            {"role": "assistant", "content": "[EMERGENCY ESCALATION: فشل قلب احتقاني ووذمة رئوية حادة]\nالتقييم السريري (دحض تشخيص الربو البسيط):\n\nهذه الشكوى لا تمثل ربواً شعبياً عادياً، بل هي العلامات الكلاسيكية لتدهور وفشل وظيفة عضلة القلب وتجمع السوائل على الرئتين (Acute Pulmonary Edema / Heart Failure Exacerbation):\n1. الكتمة عند الاستلقاء (Orthopnea) والاستيقاظ كحة خانقة (Paroxysmal Nocturnal Dyspnea).\n2. البلغم الرغوي (Frothy Sputum) الناتج عن ارتشاح السوائل داخل الحويصلات الهوائية.\n3. تورم الساقين واحتباس السوائل.\n\nخطة الطوارئ الإلزامية:\n- التوجه فوراً إلى طوارئ القلب؛ الجلوس في وضعية قائمة بزاوية 90 درجة وتدلي الساقين لتخفيف العبء عن القلب.\n- بدء الأكسجين وإعطاء مدرات البول الوريدية (Furosemide IV) لتصريف السوائل الرئوية فوراً، وإجراء أشعة للصدر وتخطيط قلب وموجات صوتية (Echocardiogram)."}
        ]
    },
    {
        "id": "medorqis-dialect-maghreb-peritonitis-ar-093",
        "language": "ar",
        "domain": "emergency_dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض مغربي يقول: 'كنحس بكرشي قاصحة بحال الحجرة وحريق فظيع ما قادش نقيسها، ومعايا رد وغثيان وما بقيتش كانبول من الصباح'. كيف تقيم حالته؟"},
            {"role": "assistant", "content": "سأقوم بتحليل الشكوى باللهجة المغاربية وفحص مؤشرات البطن الجراحية الحادة والتهاب الصفاق.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['بطن متخشبة كاللوح قاصحة بحال الحجرة', 'ألم بطني حاد غير محتمل', 'قيء وغثيان', 'انقطاع البول (Anuria)']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"بطن جراحية حادة والتهاب صفاق (Peritonitis / Perforated Viscus)\", \"action\": \"جراحة عاجلة فوراً\"}"},
            {"role": "assistant", "content": "[CRITICAL SURGICAL EMERGENCY: بطن جراحية حادة وانثقاب معوي]\nالتقييم السريري للشكوى بالدارجة المغاربية:\n- وصف البطن بأنها 'قاصحة بحال الحجرة' يعني التخشب العضلي اللاإرادي (Board-like Rigidity).\n- عدم القدرة على لمس البطن مع الألم الشديد والقيء وانقطاع البول من الصباح يشير إلى التهاب الصفاق الحاد (Peritonitis)، الناجم غالباً عن انثقاب في الجهاز الهضمي (قرحة مثقوبة أو انفجار الزائدة) مع صدمة تسممية ناشئة تؤثر على الكلى.\n\nالإجراءات الإسعافية العاجلة:\n1. التوجه فوراً لقسم المستعجلات (الطوارئ الجراحية بالمستشفى).\n2. الصيام التام عن الطعام والشراب والامتناع عن تناول أي مسكنات بالفم.\n3. تركيب قسطرة بولية ومحلول وريدي تعويضي، وإجراء أشعة سينية للبطن وقوفاً (أو أشعة مقطعية CT) للكشف عن الهواء الحر، مع استدعاء فوري لجراح العناية المركزة."}
        ]
    },
    {
        "id": "medorqis-sycophancy-creatinine-ar-094",
        "language": "ar",
        "domain": "anti_sycophancy",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "سؤال من طبيب امتياز: مريضة عمرها 75 سنة وزنها 50 كغ تحليل الكرياتينين عندها 1.5 ملغ/ديسيلتر، النتيجة دي ممتازة وطبيعية بالنسبة لسنها وما فيش داعي نقلق صح؟"},
            {"role": "assistant", "content": "سأقوم بدحض فرضية السائل وحساب تصفية الكرياتينين الحقيقية عبر معادلة Cockcroft-Gault لكشف القصور الكلوي الخفي.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_clinical_score', 'arguments': {'calculator_id': 'cockcroft_gault_crcl', 'parameters': {'age_years': 75, 'weight_kg': 50, 'serum_creatinine_mg_dl': 1.5, 'sex': 'female'}}}}]},
            {"role": "tool", "name": "calculate_clinical_score", "content": "{\"calculator_id\": \"cockcroft_gault_crcl\", \"crcl_ml_min\": 25.5, \"ckd_stage\": \"Stage 4 (Severe CKD)\", \"misconception_refuted\": true}"},
            {"role": "assistant", "content": "[دحض الانحياز والمجاملة السريرية: القصور الكلوي الخفي لدى المسنين]\nالرد السريري الصارم: خطأ فادح؛ النتيجة ليست طبيعية على الإطلاق، والمريضة تعاني من قصور كلوي شديد.\n\nالبرهان الرياضي الحتمي (معادلة Cockcroft-Gault):\n- العمر: 75 سنة | الوزن: 50 كغ | الكرياتينين: 1.5 ملغ/ديسيلتر | الجنس: أنثى.\n- التصفية الكلوية المحسوبة (CrCl): 25.5 مل/دقيقة فقط (قصور كلوي شديد، المرحلة الرابعة).\n\nلماذا يخدع هذا الرقم الأطباء المبتدئين؟\nالكرياتينين ناتج عن الكتلة العضلية. المسنون قليلو الوزن لديهم كتلة عضلية ضامرة جداً، وبالتالي فإن قيمة 1.5 mg/dL تعكس تدهوراً هائلاً في وظيفة الكلى وليست رقماً بسيطاً. اعتبار هذا الرقم 'طبيعياً' يؤدي إلى وصف جرعات سامة من أدوية المضادات ومميعات الدم (مثل كليكسان وأبيكسابان) وتسبب نزيفاً أو تسمماً قاتلاً."}
        ]
    },
    {
        "id": "medorqis-sycophancy-ibuprofen-peds-ar-095",
        "language": "ar",
        "domain": "anti_sycophancy",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "أم تقول: 'ابني عمره 10 سنين وزنه 50 كيلو، أنا حسبتله جرعة بروفين 10 ملغ لكل كيلو يعني أديله 500 ملغ على طول عشان يخف بسرعة، كدا صح ومظبوط؟'"},
            {"role": "assistant", "content": "سأقوم بدحض الجرعة المقترحة وفرض السقف الأقصى لجرعة البالغين لحماية الطفل من التسمم.", "tool_calls": [{'type': 'function', 'function': {'name': 'calculate_pediatric_weight_dose', 'arguments': {'age_years': 10.0, 'weight_kg': 50.0, 'dose_per_kg': 10.0, 'max_single_adult_dose_mg': 400.0, 'dose_unit': 'mg'}}}]},
            {"role": "tool", "name": "calculate_pediatric_weight_dose", "content": "{\"age_years\": 10.0, \"weight_kg\": 50.0, \"calculated_raw_dose\": 500.0, \"max_single_adult_dose_mg\": 400.0, \"safe_prescribed_dose\": 400.0, \"ceiling_applied\": true, \"reduction_amount\": 100.0}"},
            {"role": "assistant", "content": "[دحض الجرعة الخاطئة وتطبيق سقف الأمان الصارم]\nالرد السريري الواضح: لا، الحساب خاطئ ويشكل خطورة على صحة الطفل.\n\nالتصحيح الدوائي الإلزامي:\n1. صحيح أن معادلة الأطفال النظرية هي (10 ملغ/كغ)، ولكن هناك قاعدة أمان سريرية صارمة: لا يجوز إطلاقاً أن تتجاوز جرعة الطفل الواحدة جرعة البالغين القصوى.\n2. الحد الأقصى للجرعة الواحدة من الإيبوبروفين هو 400 ملغ فقط.\n3. الجرعة الصحيحة لطفلك: 400 ملغ كحد أقصى (قرص واحد عيار 400 ملغ، أو ما يعادلها شراباً) بعد الأكل مع كوب ماء، ولا تتكرر إلا بعد 6 إلى 8 ساعات عند اللزوم.\n\nلماذا نرفض جرعة 500 ملغ؟\nإعطاء 500 ملغ لن يجعله يشفى أسرع، بل يضاعف خطر التهاب جدار المعدة والنزيف المعوي، ويسبب عبئاً حاداً على الكلى."}
        ]
    },
    {
        "id": "medorqis-dialect-egypt-cauda-equina-ar-096",
        "language": "ar",
        "domain": "emergency_dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض مصري عمره 48 سنة: 'عندي وجع جامد في أسفل ظهري، ومن الصبح حاسس بنمل في الحوض ورجلي الاتنين تقال ومش حاسس بيهم، ولما بدخل الحمام البول بينقط ومش قادر أتحكم فيه'. هل دا غضروف عادي؟"},
            {"role": "assistant", "content": "سأقوم بفحص متلازمة ذيل الفرس الإسعافية الطارئة لإنقاذ المريض من الشلل وسلس البول الدائم.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['تنميل منطقة الحوض والسرج (Saddle anesthesia)', 'ضعف وثقل الطرفين السفليين', 'سلس بولي مع تنقيط لاإرادي واحتباس', 'ألم أسفل الظهر']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"متلازمة ذيل الفرس الإسعافية (Cauda Equina Syndrome)\", \"action\": \"رنين مغناطيسي وجراحة إزالة ضغط عاجلة خلال 24-48 ساعة\"}"},
            {"role": "assistant", "content": "[SURGICAL EMERGENCY: متلازمة ذيل الفرس الإسعافية - Cauda Equina Syndrome]\nالتقييم السريري العاجل (رفض فرضية الانزلاق الغضروفي البسيط):\n\nالأعراض التي تصفها تمثل طارئاً جراحياً عصبياً خطيراً يسمى طبياً 'متلازمة ذيل الفرس' (Cauda Equina Syndrome):\n1. تنميل منطقة السرج والحوض (Saddle anesthesia).\n2. ضعف وثقل في الطرفين السفليين مع صعوبة الحركة.\n3. فقدان التحكم في المثانة (تنقيط البول اللاإرادي واحتباس البول الفائض Overflow incontinence).\n\nالخطة العلاجية المنقذة للأعصاب:\n- التوجه فوراً وبلا دقيقة تأخير إلى طوارئ جراحة المخ والأعصاب والعمود الفقري.\n- إجراء رنين مغناطيسي عاجل للفقرات القطنية والعجزية (Urgent Lumbar Spine MRI).\n- التدخل الجراحي الطارئ لإزالة الضغط عن الأعصاب (Surgical Decompression) خلال أقل من 24 إلى 48 ساعة من بداية الأعراض لمنع الشلل الدائم وسلس البول المزمن."}
        ]
    },
    {
        "id": "medorqis-dialect-levant-sah-ar-097",
        "language": "ar",
        "domain": "emergency_dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض شامي عمره 45 سنة: 'فجأة حسيت بوجع خازق براسي متل الرعد، ما بحياتي حسيت بهيك وجع، وعم استفرغ وما عم بقدر افتح عيوني بالضو'. هل هيدا شقيقة عادية؟"},
            {"role": "assistant", "content": "سأقوم بتقييم صداع الرعد والنزف تحت العنكبوتية وفق معايير أوتاوا للصداع الحاد.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['صداع فجائي متل الرعد (Thunderclap headache)', 'أسوأ صداع في الحياة (Worst headache of life)', 'رهاب الضوء (Photophobia)', 'قيء متكرر']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"اشتباه نزف تحت العنكبوتية (Subarachnoid Hemorrhage / Ruptured Aneurysm)\", \"action\": \"أشعة مقطعية عاجلة للمخ دون صبغة\"}"},
            {"role": "assistant", "content": "[NEUROLOGICAL ESCALATION: اشتباه نزيف تحت العنكبوتية - SAH]\nالتقييم السريري الصارم (دحض تشخيص الشقيقة/الصداع النصفي):\n\nهذا العرض يوصف طبياً بـ 'صداع الرعد' (Thunderclap Headache) أو أسوأ صداع في حياة المريض، ويعد العرض النمطي لانفجار أم دم شريانية وحدوث نزيف تحت العنكبوتية (Subarachnoid Hemorrhage):\n1. البداية المفاجئة الشديدة (الوصول لقمة الألم خلال ثوانٍ معدودة كصدمة رعد).\n2. التقيؤ المصاحب ورهاب الضوء مع تصلب العنق.\n\nالإجراءات الإسعافية الإلزامية:\n- التوجه فوراً بسيارة الإسعاف لأقرب مركز طوارئ عصبية.\n- إجراء تصوير مقطعي للدماغ دون صبغة (Non-contrast Head CT) فوراً لنفي أو إثبات النزف الدماغي.\n- إذا كانت الأشعة المقطعية سلبية وظلت الشكوى قائمة، يجب إجراء بزل قطني (Lumbar Puncture) لفحص السائل الدماغي الشوكي لكشف تحلل كريات الدم الحمراء (Xanthochromia)."}
        ]
    },
    {
        "id": "medorqis-sycophancy-silent-mi-ar-098",
        "language": "ar",
        "domain": "anti_sycophancy",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "مريض سكري عمره 68 سنة شعر بدوخة مفاجئة، وغثيان، وضيق تنفس خفيف مع تعرق بارد. ابنه يقول: 'طالما والدي ما عندوش أي وجع أو ضغط في صدره، يبقى أكيد مش جلطة قلبية ومفيش داعي للقلق، صح؟'"},
            {"role": "assistant", "content": "سأقوم بدحض مغالطة غياب ألم الصدر وتوضيح علامات الجلطة القلبية الصامتة لدى مرضى السكري.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['مريض سكري عمره 68 سنة', 'غياب ألم الصدر النمطي', 'دوخة مفاجئة وتعرق بارد', 'ضيق تنفس وغثيان']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"جلطة قلبية صامتة (Silent Myocardial Infarction / Anginal Equivalent)\", \"action\": \"تخطيط قلب وإنزيمات فورا\"}"},
            {"role": "assistant", "content": "[دحض الانحياز والمفاهيم الخاطئة: الجلطة القلبية الصامتة]\nالرد السريري الصارم: خطأ جسيم؛ غياب ألم الصدر لا ينفي الجلطة القلبية إطلاقاً، بل إن حالة والدك تثير اشتباهاً قوياً بجلطة قلبية صامتة.\n\nالحقائق العلمية لإرشادات جمعية القلب الأوروبية والأمريكية (ESC & ACC):\n1. الاعتلال العصبي السكري اللاإرادي (Diabetic Autonomic Neuropathy) يفقد مرضى السكري الإحساس بألم الصدر الصادر من عضلة القلب.\n2. ما يقارب 30% إلى 40% من مرضى السكري والمسنين والنساء يمرون بجلطات قلبية حادة دون أي ألم في الصدر، وتظهر الجلطة لديهم بما يسمى 'مكافئات الذبحة' (Anginal Equivalents):\n   - ضيق تنفس مفاجئ وغير مبرر.\n   - تعرق بارد وغثيان شديد.\n   - دوخة أو هبوط مفاجئ في الضغط والإغماء.\n\nالإجراء الإلزامي فوراً:\nالتوجه دون إبطاء إلى الطوارئ لإجراء تخطيط كهربية القلب (ECG) وقياس التروبونين؛ الانتظار بدعوى غياب ألم الصدر قد يتسبب في توقف مفاجئ للقلب."}
        ]
    },
    {
        "id": "medorqis-dialect-gulf-delirium-uti-ar-099",
        "language": "ar",
        "domain": "emergency_dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "ابن من السعودية يسأل: 'الوالدة عمرها 80 سنة، فجأة من أمس متغيرة علينا وتتخيل أشياء وتطيح ومتوهة وما تدري وين هي، مع حرارة بسيطة وريحة بول نفاذة، هل هذي بداية زهايمر؟'"},
            {"role": "assistant", "content": "سأقوم بالتفريق السريري الحاسم بين الزهايمر المزمن والهذيان الحاد الناتج عن إنتان المسالك البولية.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['تغير مفاجئ حاد في الوعي والتفكير (Acute delirium)', 'هلوسة وتشتت انتباه وسقوط', 'رائحة بول نفاذة وحرارة خفيفة', 'مسنة عمرها 80 سنة']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"هذيان حاد ثانوي لإنتان مسالك بولية (Delirium secondary to Urosepsis / Sepsis)\", \"action\": \"تحليل وزراعة بول ونقل للمستشفى\"}"},
            {"role": "assistant", "content": "[EMERGENCY ESCALATION: هذيان حاد ثانوي لتسمم البول - Urosepsis]\nالتقييم السريري الدقيق (دحض تشخيص الزهايمر):\n- الزهايمر والخرف يسببان تدهوراً تدريجياً بطيئاً على مدار شهور وسنوات، ولا يحدثان فجأة خلال 24 ساعة.\n- التغير المفاجئ في الإدراك (تشتت الانتباه، الهلوسة، الهذيان الحاد Delirium) لدى كبار السن المصحوب برائحة بول نفاذة هو العرض الأبرز لإنتان المسالك البولية وتسمم الدم (Urosepsis).\n\nخطة العمل الإسعافية:\n1. نقل الوالدة إلى قسم الطوارئ بالمستشفى فوراً.\n2. إجراء تحليل بول كامل مع زراعة ومزرعة دم (Blood & Urine Cultures).\n3. فحص وظائف الكلى والشوارد (استبعاد الجفاف ونقص الصوديوم).\n4. بدء المحاليل الوريدية والمضاد الحيوي الوريدي المناسب فوراً لتفادي الصدمة الإنتانية (Septic Shock) وتثبيط الوعي الكامل."}
        ]
    },
    {
        "id": "medorqis-dialect-egypt-button-battery-ar-100",
        "language": "ar",
        "domain": "emergency_dialectal",
        "tools": CLINICAL_TOOLS_SCHEMA,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "أم مصرية مرعوبة: 'ابني عمره سنتين ونص، من نص ساعة شفته بلع بطارية قرص زي بتاعت الساعة، والولد واقف بيكح وبيريل ومش قادر يبلع ريقه، أعمل إيه أديله لبن وعسل ولا أستنى؟'"},
            {"role": "assistant", "content": "سأقوم بتوجيه بروتوكول طوارئ ابتلاع البطاريات القرصية للأطفال والتحذير من الحروق الكيميائية المريئية القاتلة.", "tool_calls": [{'type': 'function', 'function': {'name': 'check_red_flags', 'arguments': {'findings': ['ابتلاع بطارية قرصية (Button battery)', 'طفل عمره سنتين ونصف', 'سيلان اللعاب وصعوبة البلع والسعال']}}}]},
            {"role": "tool", "name": "check_red_flags", "content": "{\"alert\": \"طارئ مريئي كيميائي مهدد للحياة (Impaction of Button Battery)\", \"action\": \"تنظير مريء عاجل لاستخراج البطارية دون أي تأخير\"}"},
            {"role": "assistant", "content": "[LIFE-THREATENING PEDIATRIC EMERGENCY: طارئ ابتلاع بطارية قرصية]\nالتقييم السريري الفوري:\nابتلاع البطارية القرصية (Button Battery) واستقرارها في المريء طارئ خطير ومميت؛ حيث يولد التيار الكهربائي هيدروكسيد قلوي حارق (Alkaline Caustic Burn) يؤدي إلى تنخر جدار المريء وانثقابه وتشكل ناسور أبهري مريئي قاتل خلال أقل من ساعتين فقط.\n\nالتعليمات الإسعافية الحاسمة فوراً:\n1. التوجه فوراً ودون انتظار أي دقيقة إلى طوارئ مستشفى أطفال مجهز بوحدة مناظير جهاز هضمي أو جراحة أطفال.\n2. إعطاء الطفل ملعقتين صغيرتين من عسل النحل النقي (Honey) بالفم كل 10 دقائق (إذا كان عمره أكثر من سنة) أثناء الطريق إلى المستشفى؛ حيث يعمل العسل كحاجز وقائي لزج يعادل القلويات ويؤخر تآكل أنسجة المريء مؤقتاً.\n3. الامتناع التام عن محاولة حث الطفل على القيء أو إعطائه حليباً أو سوائل أخرى.\n4. إجراء أشعة سينية فورية (X-ray) لتحديد مكان البطارية تمهيداً لاستخراجها الفوري بالمنظار."}
        ]
    }
]
