"""
MedOrqis-LLM — Clinical Instruction Expansion (Cases 101 - 150)
Covers Beers Criteria 2023, MELD-Na, SOFA Sepsis-3, Burch-Wartofsky Thyroid Storm, and PERC Rule.
Strict zero-emoji compliance.
"""

import json
from training.dataset_builder import CLINICAL_TOOLS_SCHEMA, SYSTEM_PROMPT

EXPANDED_CLINICAL_CASES_PART3 = [
{
    "id": "medorqis-beers-glyburide-en-101",
    "language": "en",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "An 82-year-old female with type 2 diabetes has an eGFR of 48 mL/min/1.73m2. Her primary physician prescribed glyburide 5 mg daily. She experiences recurrent morning lightheadedness. Evaluate this medication under Beers Criteria 2023."
        },
        {
            "role": "assistant",
            "content": "I will evaluate the geriatric prescription against the American Geriatrics Society (AGS) Beers Criteria 2023 for potentially inappropriate medications.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Age 82 years",
                                "Prescribed glyburide (glibenclamide)",
                                "Recurrent morning lightheadedness",
                                "eGFR 48 mL/min/1.73m2"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"POTENTIALLY_INAPPROPRIATE_AVOID\", \"criterion\": \"Sulfonylurea with active metabolites in older adults\", \"risk\": \"Severe prolonged hypoglycemia and neuroglycopenic brain injury\", \"alternative\": \"Glipizide or DPP-4 inhibitor\"}"
        },
        {
            "role": "assistant",
            "content": "[BEERS CRITERIA 2023: HIGH-RISK GERIATRIC MEDICATION]\nGuideline Evaluation: GLYBURIDE IS STRONGLY INAPPROPRIATE IN OLDER ADULTS (AVOID).\n\nPharmacological Hazard:\n1. Glyburide possesses active circulating metabolites eliminated renally. In older adults with physiological or pathological renal decline (eGFR 48 mL/min), drug and metabolite accumulation causes unpredictable, prolonged hypoglycemia lasting up to 24-36 hours.\n2. Recurrent morning lightheadedness represents nocturnal and morning neuroglycopenia, sharply escalating the risk of falls, traumatic intracranial hemorrhage, and dysrhythmias.\n\nMandated Clinical Interventions:\n1. Discontinue glyburide immediately.\n2. If a secretagogue is strictly necessary, switch to short-acting Glipizide (which has inactive metabolites). The preferred safer alternative is a renal-adjusted DPP-4 inhibitor (e.g. Linagliptin 5 mg daily) or low-dose SGLT2 inhibitor under hydration monitoring."
        }
    ]
},
{
    "id": "medorqis-beers-glyburide-ar-102",
    "language": "ar",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريضة سكري عمرها 80 سنة تتناول جليبينكلاميد (داونيل Daonil 5mg). تشتكي من دوخة وعرق بارد كل صباح قبل الإفطار. هل هذا الدواء آمن لكبار السن وفق معايير بيرز؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص أمان الدواء لكبار السن وفق معايير جمعية طب المسنين الأمريكية (Beers Criteria 2023).",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "عمر 80 سنة",
                                "تناول دواء داونيل جليبينكلاميد",
                                "دوخة وعرق بارد صباحي"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"غير ملائم إطلاقاً لكبار السن (Avoid)\", \"خطر\": \"هبوط سكر حاد وطويل الأمد\", \"بديل\": \"جليكلازيد أو جليبيديز أو أدوية DPP-4\"}"
        },
        {
            "role": "assistant",
            "content": "[تنبيه دوائي عاجل لكبار السن: معايير بيرز Beers Criteria 2023]\nالتقييم السريري: دواء داونيل (Glibenclamide) محظور وغير آمن للمسنين ويجب إيقافه فوراً.\n\nالخطر السريري:\n- دواء داونيل يتحول في الكبد إلى نواتج نشطة تُطرح عن طريق الكلى. وبسبب بطء التخلص من الدواء لدى كبار السن، يتراكم الدواء مسبباً هبوطاً حاداً ومطولاً في سكر الدم قد يستمر لأكثر من 24 ساعة.\n- الدوخة والعرق البارد في الصباح هي علامات هبوط سكر الدم الشديد، مما يعرض المريضة لخطر السقوط، كسور الحوض، أو الغيبوبة السكرية ونقص تروية الدماغ.\n\nالإجراء الطبي الصحيح:\n1. إيقاف دواء داونيل فوراً ومراقبة السكر بالمنزل.\n2. التحويل إلى بديل آمن قليل التسبب بهبوط السكر مثل مثبطات DPP-4 (مثلاً ليناجلبتين تراجينتا 5 ملغ) أو سلفونيل يوريا قصير المفعول مثل جليكلازيد (دياميكرون MR بجرعة منخفضة)."
        }
    ]
},
{
    "id": "medorqis-beers-diphenhydramine-en-103",
    "language": "en",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 78-year-old male with mild cognitive impairment takes over-the-counter Diphenhydramine 50 mg nightly for insomnia. His family notes worsening daytime confusion and acute urinary hesitancy. Evaluate under Beers Criteria."
        },
        {
            "role": "assistant",
            "content": "I will evaluate anticholinergic burden in older adults using the Beers Criteria 2023 framework.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Age 78 years",
                                "Mild cognitive impairment",
                                "Diphenhydramine 50mg nightly",
                                "New acute confusion and urinary hesitancy"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"POTENTIALLY_INAPPROPRIATE_STRONG_AVOID\", \"mechanism\": \"Potent central and peripheral anticholinergic toxicity\", \"clinical_outcome\": \"Delirium, cognitive precipitation, urinary retention\"}"
        },
        {
            "role": "assistant",
            "content": "[BEERS CRITERIA 2023: HIGH ANTICHOLINERGIC BURDEN]\nGuideline Evaluation: DIPHENHYDRAMINE IS STRONGLY CONTRAINDICATED IN ELDERLY PATIENTS FOR INSOMNIA.\n\nPathophysiologic Toxicity:\n1. First-generation antihistamines (Diphenhydramine, Chlorpheniramine, Hydroxyzine) cross the blood-brain barrier and potently block muscarinic receptors.\n2. In older patients, especially those with pre-existing cognitive impairment, central muscarinic blockade accelerates neurocognitive decline, precipitates acute delirium, and increases fall risk.\n3. Peripherally, it relaxes the detrusor muscle and contracts the bladder trigone, triggering acute urinary retention.\n\nMandated Interventions:\n1. Taper and discontinue diphenhydramine.\n2. Institute non-pharmacological sleep hygiene (stimulus control, consistent schedule, bright daytime light).\n3. If pharmacotherapy is essential, non-anticholinergic alternatives such as low-dose Melatonin (1 to 2 mg) or dual orexin receptor antagonists (DORAs) may be considered under geriatric supervision."
        }
    ]
},
{
    "id": "medorqis-beers-diphenhydramine-ar-104",
    "language": "ar",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مسنة عمرها 79 سنة تعاني من صعوبة النوم، بدأت ابنتها تعطيها أقراص حساسية ديفينهيدرامين كمنوم كل ليلة. لاحظت العائلة تشوشاً بالذهن وتوهاناً وتوقف التبول. ما السبب؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص التسمم بمضادات الكولين ومخاطر مضادات الهيستامين للمسنين وفق معايير بيرز.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "مسنة 79 سنة",
                                "تناول ديفينهيدرامين كمنوم",
                                "تشوش ذهني وهذيان",
                                "احتباس بولي"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"ممنوع تماماً لكبار السن (Avoid)\", \"آلية\": \"تأثير مضاد للمسكارين والكولين\", \"نتيجة\": \"هذيان حاد واحتباس بولي\"}"
        },
        {
            "role": "assistant",
            "content": "[تحذير عاجل من مضادات الكولين لكبار السن - Beers Criteria 2023]\nالتقييم السريري: إيقاف الدواء فوراً؛ مضادات الحساسية من الجيل الأول محظورة كمنومات للمسنين.\n\nتفسير الأعراض:\n1. الأدوية المضادة للهيستامين من الجيل الأول (مثل ديفينهيدرامين أو فينيرجان) تتمتع بتأثير قوي مضاد للكولين:\n- في الدماغ: تعطل النواقل العصبية وتسبب هذياناً حاداً وتشوشاً بالذاكرة والسقوط.\n- في المثانة: تمنع انقباض عضلة المثانة مسببة احتباساً بولياً مؤلماً وحاداً.\n\nالإجراءات الإسعافية:\n1. التوقف الفوري عن إعطاء أي أدوية حساسية منومة.\n2. نقل المسنة للطوارئ وفحص المثانة لتركيب قسطرة بولية مؤقتة لتفريغ البول المحتبس وتفادي القصور الكلوي الحاد.\n3. الاعتماد على تنظيم بيئة النوم الطبيعية أو استشارة طبيب المسنين."
        }
    ]
},
{
    "id": "medorqis-beers-diazepam-fall-en-105",
    "language": "en",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 74-year-old female is prescribed Diazepam 5 mg BID for chronic anxiety. Review this prescription against Beers 2023 guidelines regarding fall and fracture risks."
        },
        {
            "role": "assistant",
            "content": "I will evaluate benzodiazepine half-life and fall risk in older adults using the Beers Criteria.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Age 74 years",
                                "Prescribed long-acting benzodiazepine diazepam",
                                "Chronic anxiety"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"POTENTIALLY_INAPPROPRIATE_AVOID\", \"hazard\": \"Long elimination half-life causing sedation and hip fractures\", \"alternative\": \"SSRI/SNRI + non-pharmacological CBT\"}"
        },
        {
            "role": "assistant",
            "content": "[BEERS CRITERIA 2023: LONG-ACTING BENZODIAZEPINE HAZARD]\nGuideline Verdict: BENZODIAZEPINES SHOULD BE AVOIDED IN OLDER ADULTS FOR ANXIETY.\n\nPharmacological Rationale:\n1. Diazepam has an extensive elimination half-life exceeding 48 to 100 hours. Hepatic oxidative clearance via CYP enzymes slows significantly in aging, causing progressive drug accumulation.\n2. Consequence: Persistent psychomotor slowing, daytime somnolence, cerebellar ataxia, and a greater than 50% increase in falls and devastating hip fractures.\n\nMandated Clinical Plan:\n1. Do NOT stop diazepam abruptly (risk of withdrawal seizures and rebound anxiety). Initiate a slow, structured taper (reduce by 10-25% every 2-4 weeks).\n2. First-line guideline therapy for generalized anxiety disorder in older adults: SSRI (e.g. Sertraline or Escitalopram at low starting doses) combined with Cognitive Behavioral Therapy (CBT)."
        }
    ]
},
{
    "id": "medorqis-beers-diazepam-fall-ar-106",
    "language": "ar",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض عمره 75 سنة موصوف له فاليوم (ديازيبام 5 ملغ مرتين يومياً) للقلق والتوتر منذ شهور وبدأ يعاني من ترنح وثقل بالحركة. هل يستمر عليه؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص محاذير البنزوديازيبينات طويلة المفعول لدى كبار السن وفق معايير الجمعية الأمريكية لطب المسنين.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "مريض 75 سنة",
                                "ديازيبام فاليوم مزمن",
                                "ترنح وثقل بالحركة"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"محظور لكبار السن (Avoid)\", \"خطر\": \"تراكم المهدئ، السقوط، وكسور الحوض\", \"إجراء\": \"تخفيض تدريجي بطيء\"}"
        },
        {
            "role": "assistant",
            "content": "[تنبيه لسلامة المسنين: خطورة الفاليوم والديازيبام]\nوفقاً لمعايير بيرز (AGS Beers Criteria 2023):\n\n1. التقييم الدوائي:\n- الديازيبام (Valium) دواء طويل المفعول جداً؛ نواتجه الفعالة تبقى في دم المسن لأكثر من 100 ساعة بسبب بطء استقلاب الكبد، مما يسبب تراكم المهدئ وترنح المشية ومضاعفة خطر كسور عظام الحوض المميتة.\n\n2. خطة التوقف الآمن:\n- يمنع إيقاف الدواء فجأة لتجنب التشنجات والقلق الارتدادي الحاد.\n- يجب سحب الدواء بالتدريج البطيء بإشراف الطبيب (إنقاص الجرعة بنسبة 10-20% كل أسبوعين إلى 4 أسابيع).\n- البديل المعتمد دولياً لعلاج القلق المزمن لدى كبار السن: مضادات الاكتئاب الحديثة (SSRI مثل سيرترالين بجرعات صغيرة) مع العلاج السلوكي."
        }
    ]
},
{
    "id": "medorqis-beers-nsaid-hf-en-107",
    "language": "en",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 76-year-old male with heart failure with reduced ejection fraction (HFrEF, EF 35%) takes Naproxen 500 mg BID for chronic knee pain. What adverse hemodynamic cascade does Beers Criteria warn against?"
        },
        {
            "role": "assistant",
            "content": "I will evaluate non-steroidal anti-inflammatory risks in heart failure patients using Beers Criteria.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Age 76 years",
                                "HFrEF EF 35%",
                                "Prescribed naproxen 500mg BID"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"POTENTIALLY_INAPPROPRIATE_STRONG_AVOID\", \"hemodynamic_effect\": \"Sodium and fluid retention, blunting of diuretics, acute decompensated heart failure hospitalization\"}"
        },
        {
            "role": "assistant",
            "content": "[BEERS CRITERIA 2023: NSAIDS IN HEART FAILURE]\nGuideline Evaluation: NSAIDS ARE STRONGLY CONTRAINDICATED IN HEART FAILURE (AVOID).\n\nPathophysiologic Cascade:\n1. Cyclooxygenase inhibition suppresses prostaglandin E2 and prostacyclin, blunting renal medullary blood flow and promoting avid sodium and water retention.\n2. NSAIDs directly antagonize the natriuretic and vasodilatory efficacy of loop diuretics (Furosemide) and ACE-inhibitors/ARBs.\n3. Clinical Outcome: Acute decompensated heart failure, severe pulmonary congestion, and a dramatic spike in emergency hospitalizations.\n\nMandated Interventions:\n1. Stop Naproxen immediately.\n2. Analgesic alternatives for osteoarthritis: Topical NSAID gel (minimal systemic absorption), oral Acetaminophen (up to 2-3 g/day), or physical therapy and intra-articular steroid injections."
        }
    ]
},
{
    "id": "medorqis-beers-nsaid-hf-ar-108",
    "language": "ar",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض هبوط قلب مزمن عمره 74 سنة (عضلة القلب 30%) بدأ يتناول نبروكسين أو كتافلام لألم الركبة، وبعد 4 أيام انتفخت قدماه وضاق نفسه عند النوم. ما التفسير الطبي؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص تعارض مسكنات NSAIDs مع فشل القلب الاحتقاني وفق معايير بيرز وإرشادات جمعية القلب الأوروبية.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "مريض هبوط قلب 74 سنة",
                                "تناول نبروكسين أو ديكلوفيناك",
                                "انتفاخ القدمين وضيق تنفس اضطجاعي"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"محظور بشدة لمرضى هبوط القلب\", \"آلية\": \"احتباس الصوديوم والسوائل وتعطيل مدرات البول\", \"إجراء\": \"إيقاف المسكن وفحص رئة المريض\"}"
        },
        {
            "role": "assistant",
            "content": "[تحذير حرج: مسكنات NSAIDs لمرضى هبوط القلب]\nالتقييم السريري: المسكن هو السبب المباشر في تدهور حالة القلب وتجمع السوائل.\n\nالآلية المرضية:\n- مسكنات الالتهاب (مثل كتافلام، فولتارين، بروفين، نبروكسين) تحبس الصوديوم والماء داخل الجسم، وتلغي مفعول مدرات البول (مثل لازيكس)، وتضيق شرايين الكلى.\n- النتيجة: زيادة العبء فجأة على عضلة القلب الضعيفة وتجمع السوائل في الساقين والرئتين.\n\nالإجراءات الإلزامية:\n1. إيقاف المسكن فوراً.\n2. مراجعة طبيب القلب فوراً لزيادة جرعة مدر البول وفحص الرئتين بالأشعة السينية.\n3. تسكين ألم الركبة بالدهانات الموضعية أو الباراسيتامول الآمن للقلب."
        }
    ]
},
{
    "id": "medorqis-beers-amitriptyline-bph-en-109",
    "language": "en",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "An 80-year-old male with benign prostatic hyperplasia (BPH) is prescribed Amitriptyline 50 mg nightly for neuropathic pain. Two days later, he presents with painful suprapubic distension and anuria. What occurred?"
        },
        {
            "role": "assistant",
            "content": "I will evaluate tertiary amine tricyclic antidepressant anticholinergic toxicity in obstructive uropathy.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Age 80 years",
                                "BPH",
                                "Prescribed amitriptyline",
                                "Painful suprapubic distension and anuria"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"POTENTIALLY_INAPPROPRIATE_STRONG_AVOID\", \"toxicity\": \"Severe anticholinergic urinary retention\", \"action\": \"Urgent urinary catheterization + discontinue amitriptyline\"}"
        },
        {
            "role": "assistant",
            "content": "[BEERS CRITERIA 2023: TRICYCLIC ANTIDEPRESSANT IN BPH]\nGuideline Verdict: AMITRIPTYLINE IS STRONGLY INAPPROPRIATE IN MEN WITH PROSTATIC HYPERTROPHY.\n\nMechanism of Acute Toxicity:\n1. Amitriptyline is a tertiary amine tricyclic with high anticholinergic potency.\n2. In a patient with baseline mechanical bladder outflow obstruction (BPH), muscarinic M2/M3 receptor blockade paralyzes the detrusor urinae muscle while alpha-adrenergic tone maintains internal sphincter closure.\n3. Result: Complete, acute, excruciating urinary retention with a massively distended palpable bladder, threatening post-renal acute kidney injury.\n\nImmediate Management:\n1. Place an urgent Foley urinary catheter immediately to decompress the bladder.\n2. Discontinue Amitriptyline permanently.\n3. Non-anticholinergic alternatives for diabetic neuropathy in elderly males: Gabapentin (dose-titrated for renal function) or Duloxetine (minimal anticholinergic action)."
        }
    ]
},
{
    "id": "medorqis-beers-amitriptyline-bph-ar-110",
    "language": "ar",
    "domain": "geriatrics_beers",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض مسن عمره 78 سنة يعاني من تضخم البروستاتا ووصف له الطبيب تريبتيزول (Amitriptyline 50mg) لتسكين تنميل القدمين. بعد يومين لم يعد قادراً على التبول نهائياً مع ورم وألم شديد أسفل البطن. ما السبب؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص الاحتباس البولي الحاد الناتج عن مضادات الاكتئاب ثلاثية الحلقات عبر محرك MedOrqis.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "مسن 78 سنة مع تضخم بروستاتا",
                                "تناول تريبتيزول أميتريبتيلين",
                                "احتباس بولي كامل وألم أسفل البطن"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"beers_status\": \"ممنوع تماماً لمرضى البروستاتا المسنين\", \"آلية\": \"شلل عضلة المثانة بفعل التأثير المضاد للكولين\", \"إسعاف\": \"قسطرة بولية عاجلة لتفريغ المثانة\"}"
        },
        {
            "role": "assistant",
            "content": "[طوارئ المسالك البولية: احتباس البول الحاد بسبب التريبتيزول]\nوفقاً لمعايير بيرز (AGS Beers Criteria 2023):\n\n1. التشخيص الفوري:\n- احتباس بولي حاد وتمدد المثانة (Acute Urinary Retention) ناتج عن التأثير المضاد للكولين القوي لدواء تريبتيزول (Amitriptyline).\n\n2. التفسير الدوائي:\n- التريبتيزول يشل عضلة المثانة ويمنعها من الانقباض، ومع وجود تضخم البروستاتا الذي يضيق مجرى البول أصلاً، ينغلق مخرج المثانة بالكامل ويتحبس البول مسبباً ألماً شديداً وخطر فشل كلوي انسدادي.\n\n3. التدخل الإسعافي الفوري:\n1. التوجه فوراً للطوارئ لتركيب قسطرة بولية وتفريغ المثانة المتمددة.\n2. إيقاف التريبتيزول نهائياً وعدم تناوله مستقبلاً.\n3. علاج تنميل الأعصاب السكرية ببدائل آمنة للمثانة والبروستاتا (مثل جابابنتين بجرعات محسوبة كلوياً)."
        }
    ]
},
{
    "id": "medorqis-meld-decompensated-en-111",
    "language": "en",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 56-year-old male with decompensated hepatitis C cirrhosis has serum bilirubin 3.2 mg/dL, INR 1.8, serum creatinine 1.9 mg/dL, and serum sodium 130 mEq/L. No dialysis in the past week. Calculate his MELD-Na score to estimate 90-day mortality and transplant priority."
        },
        {
            "role": "assistant",
            "content": "I will calculate the MELD-Na score using the OPTN/UNOS deterministic formula to assess end-stage liver disease severity.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 3.2,
                                "inr": 1.8,
                                "serum_creatinine_mg_dl": 1.9,
                                "serum_sodium_meq_l": 130.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 26.0, \"status\": \"HIGH_90_DAY_MORTALITY\", \"mortality_estimate_percent\": \"19-20%\"}"
        },
        {
            "role": "assistant",
            "content": "[MELD-Na SCORE: 26 (SEVERE DECOMPENSATED CIRRHOSIS)]\nDeterministic Calculation:\n- Serum Bilirubin: 3.2 mg/dL | INR: 1.8 | Serum Creatinine: 1.9 mg/dL | Serum Sodium: 130 mEq/L.\n- Calculated MELD-Na Score: 26.\n\nClinical Implications:\n1. Estimated 90-day waitlist mortality is approximately 19-20%.\n2. Hyponatremia (130 mEq/L) reflects severe splanchnic arterial vasodilation and hyperdynamic circulatory failure, significantly worsening prognosis.\n3. The patient clearly exceeds the MELD >= 15 threshold and warrants expedited referral for orthotopic liver transplantation evaluation."
        }
    ]
},
{
    "id": "medorqis-meld-decompensated-ar-112",
    "language": "ar",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض تليف كبدي عمره 58 سنة مصاب باستسقاء في البطن. التحاليل: بيليروبين 4.0 ملغ/ديسيلتر، سيولة الدم INR 2.1، كرياتينين 2.2 ملغ/ديسيلتر، وصوديوم الدم 128 ملي مكافئ/لتر، ولم يغسل كلى هذا الأسبوع. احسب نقاط MELD-Na لتقييم خطورة الكبد."
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب نقاط MELD-Na الحتمية وفق معادلات زراعة الكبد الدولية (UNOS/OPTN).",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 4.0,
                                "inr": 2.1,
                                "serum_creatinine_mg_dl": 2.2,
                                "serum_sodium_meq_l": 128.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 30.0, \"status\": \"CRITICAL_HEPATIC_IMPAIRMENT\", \"mortality_estimate_percent\": \"52.6%\"}"
        },
        {
            "role": "assistant",
            "content": "[نتيجة تقييم MELD-Na: 30 نقطة (فشل كبدي حرج متقدم)]\nالتحليل الحتمي الدقيق:\n- البيليروبين: 4.0 ملغ/ديسيلتر | INR: 2.1 | الكرياتينين: 2.2 ملغ/ديسيلتر | الصوديوم: 128 ملي مكافئ/لتر.\n- نتيجة MELD-Na: 30 نقطة.\n\nالتوجيه السريري:\n1. نسبة الوفاة المتوقعة خلال 90 يوماً تتجاوز 50% بدون زراعة كبد عاجلة.\n2. هبوط الصوديوم (128) مع ارتفاع الكرياتينين (2.2) يشير بقوة إلى متلازمة كبدية كلوية وشيكة (Hepatorenal Syndrome).\n3. يجب إيقاف مدرات البول فوراً، إعطاء ألبومين وريدي، والتحويل العاجل لمركز زراعة الأعضاء."
        }
    ]
},
{
    "id": "medorqis-meld-dialysis-cap-en-113",
    "language": "en",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 63-year-old male with alcoholic cirrhosis underwent 2 sessions of hemodialysis in the past 7 days. Serum Cr is 1.6 mg/dL, Bilirubin is 2.5 mg/dL, INR is 1.6, and Sodium is 135 mEq/L. Explain how dialysis changes creatinine in MELD-Na calculation."
        },
        {
            "role": "assistant",
            "content": "I will apply the mandatory UNOS/OPTN MELD dialysis rule where creatinine is capped at 4.0 mg/dL if hemodialysis occurred within the past 7 days.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 2.5,
                                "inr": 1.6,
                                "serum_creatinine_mg_dl": 1.6,
                                "serum_sodium_meq_l": 135.0,
                                "dialysis_past_week": True
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 31.0, \"creatinine_applied_mg_dl\": 4.0, \"rule\": \"Dialysis in past week forces Cr to 4.0 mg/dL\"}"
        },
        {
            "role": "assistant",
            "content": "[MELD-Na CALCULATION: MANDATED DIALYSIS RE-SCALING]\nDeterministic Result:\n- Applied Creatinine: 4.0 mg/dL (Mandated by UNOS/OPTN because the patient had hemodialysis in the prior 7 days, regardless of measured post-dialysis Cr 1.6 mg/dL).\n- MELD-Na Score: 31.\n\nClinical Impact:\nFailing to apply the dialysis rule would artificially deflate the MELD score to 21, misrepresenting severe hepatorenal failure and delaying lifesaving liver allocation."
        }
    ]
},
{
    "id": "medorqis-meld-dialysis-cap-ar-114",
    "language": "ar",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض كبد استسقائي غسل كلى مرتين الأسبوع الماضي، وتحليله بعد الغسيل أظهر الكرياتينين 1.5، البيليروبين 2.8، والسيولة 1.7، والصوديوم 134. كيف تحسب نقاط MELD في هذه الحالة؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بتطبيق معيار UNOS الحتمي الذي يحدد الكرياتينين عند 4.0 ملغ/ديسيلتر لأي مريض خضع لغسيل كلوي خلال الأسبوع الأخير.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 2.8,
                                "inr": 1.7,
                                "serum_creatinine_mg_dl": 1.5,
                                "serum_sodium_meq_l": 134.0,
                                "dialysis_past_week": True
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 32.0, \"creatinine_used\": 4.0, \"explanation\": \"الكرياتينين يحسب 4.0 بسبب الغسيل الكلوي\"}"
        },
        {
            "role": "assistant",
            "content": "[قاعدة MELD-Na الحاسمة لمرضى الغسيل الكلوي]\nالنتيجة الحتمية: 32 نقطة.\n\nالتوضيح الطبي الإلزامي:\n- بحسب المعايير العالمية لزراعة الكبد، إذا خضع المريض لجلسة غسيل كلوي واحدة على الأقل خلال الأيام السبعة الماضية، يُلغى رقم الكرياتينين المقاس ويُحسب تلقائياً بـ 4.0 ملغ/ديسيلتر لأن الغسيل ينظف الدم اصطناعياً ولا يعكس الفشل الكلوي الحقيقي للمريض.\n- لو حسبنا بالرقم 1.5 ستنخفض النتيجة خطأً إلى 21، مما يحرم المريض من حقه في أولوية الزراعة."
        }
    ]
},
{
    "id": "medorqis-meld-transplant-listing-en-115",
    "language": "en",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 52-year-old female with primary biliary cholangitis has Bilirubin 2.2, INR 1.3, Cr 1.1, Na 137. Calculate MELD-Na and discuss if she meets the threshold for liver transplant listing."
        },
        {
            "role": "assistant",
            "content": "I will calculate the MELD-Na score to evaluate the transplant listing cutoff (MELD >= 15).",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 2.2,
                                "inr": 1.3,
                                "serum_creatinine_mg_dl": 1.1,
                                "serum_sodium_meq_l": 137.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 13.0, \"status\": \"BELOW_TRANSPLANT_LISTING_BENEFIT\", \"guideline_note\": \"MELD < 15 indicates transplant survival benefit is not yet realized\"}"
        },
        {
            "role": "assistant",
            "content": "[MELD-Na SCORE: 13 (COMPENSATED / EARLY DECOMPENSATION)]\nClinical Result:\n- MELD-Na Score: 13.\n\nTransplant Listing Guidance:\n- International liver transplant guidelines (AASLD / EASL) establish that liver transplantation offers a net survival benefit when the MELD score is 15 or greater.\n- With MELD 13, the operative mortality and post-transplant immunosuppression risks generally outweigh the 90-day waiting list mortality (less than 2%). Close outpatient surveillance and optimizing medical therapy are indicated."
        }
    ]
},
{
    "id": "medorqis-meld-transplant-listing-ar-116",
    "language": "ar",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريضة كبد مناعي مزمن تحاليلها: بيليروبين 2.0، سيولة INR 1.3، كرياتينين 1.0، صوديوم 138. هل تستفيد حالياً من الدخول في قائمة زراعة الكبد؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب نقاط MELD-Na لتقييم جدوى وفائدة زراعة الكبد مقارنة بالمخاطر الجراحية.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 2.0,
                                "inr": 1.3,
                                "serum_creatinine_mg_dl": 1.0,
                                "serum_sodium_meq_l": 138.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 12.0, \"status\": \"MELD_LESS_THAN_15\", \"recommendation\": \"المتابعة الطبية أفضل من الجراحة حالياً\"}"
        },
        {
            "role": "assistant",
            "content": "[تقييم MELD-Na: 12 نقطة - فائدة زراعة الكبد]\nالنتيجة الحسابية: 12 نقطة.\n\nالقرار السريري المبني على الأدلة:\n- وفقاً لجمعيات زراعة الكبد العالمية (AASLD)، الحد الأدنى المعتمد للاستفادة الحقيقية من زراعة الكبد هو أن تكون النقاط 15 أو أكثر (MELD >= 15).\n- عندما تكون النقاط 12، تكون نسبة الخطر من جراحة الزراعة ومثبطات المناعة أعلى من نسبة خطر المرض ذاته على الحياة خلال الـ 90 يوماً القادمة (أقل من 2%).\n- الخطة المثلى: الاستمرار في المتابعة الدورية وفحص التحاليل كل 3 أشهر."
        }
    ]
},
{
    "id": "medorqis-meld-hyponatremia-shift-en-117",
    "language": "en",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Patient A has Cr 1.2, Bili 3.0, INR 1.5, and Na 137. Patient B has identical labs except Na is 125 mEq/L. Demonstrate the numerical impact of severe hyponatremia on MELD-Na."
        },
        {
            "role": "assistant",
            "content": "I will calculate MELD-Na for both scenarios to quantify how dilutional hyponatremia escalates the prognostic score.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 3.0,
                                "inr": 1.5,
                                "serum_creatinine_mg_dl": 1.2,
                                "serum_sodium_meq_l": 125.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 24.0, \"baseline_meld_i\": 18.0, \"sodium_penalty_points\": \"+6 points due to severe hyponatremia\"}"
        },
        {
            "role": "assistant",
            "content": "[MELD-Na PROGNOSTIC IMPACT OF SEVERE HYPONATREMIA]\nComparative Analysis:\n- Baseline original MELD (without Sodium): 18.\n- With Serum Sodium 125 mEq/L: MELD-Na rises to **24** (+6 points penalty).\n\nPhysiological Mechanism:\nSevere dilutional hyponatremia in cirrhosis represents profound splanchnic pooling, excessive non-osmotic vasopressin release, and extreme neurohormonal activation, directly correlating with early refractory ascites, spontaneous bacterial peritonitis, and hepatorenal syndrome."
        }
    ]
},
{
    "id": "medorqis-meld-hyponatremia-shift-ar-118",
    "language": "ar",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض تليف كبدي أرقامه: كرياتينين 1.3، صفراء 2.8، سيولة 1.6، لكن صوديوم الدم منخفض جداً (125). كم تبلغ نقاطه وما أثر نقص الصوديوم؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب تأثير نقص صوديوم الدم الشديد على تقييم MELD-Na الحتمي.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 2.8,
                                "inr": 1.6,
                                "serum_creatinine_mg_dl": 1.3,
                                "serum_sodium_meq_l": 125.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 24.0, \"impact\": \"نقص الصوديوم أضاف 6 نقاط كاملة لخطورة الحالة\"}"
        },
        {
            "role": "assistant",
            "content": "[أثر نقص الصوديوم الحاد في تقييم MELD-Na]\nالنتيجة الحتمية: 24 نقطة.\n\nالأهمية السريرية:\n- نقص صوديوم الدم (125 ملغ/لتر) يضيف تلقائياً حوالي 6 نقاط إلى معدل الخطورة، ليعكس التدهور الشديد في الدورة الدموية الكبدية وتوسع الأوعية الحشوية.\n- يحذر بشدة من إعطاء محاليل الملح السريعة لرفع الصوديوم فجأة لتجنب حدوث انحلال الميالين الجسري المركزي (Central Pontine Myelinolysis)."
        }
    ]
},
{
    "id": "medorqis-meld-normal-labs-en-119",
    "language": "en",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A healthy 40-year-old potential living liver donor has normal lab values: Bilirubin 0.8 mg/dL, INR 1.0, Creatinine 0.9 mg/dL, Sodium 140 mEq/L. What is the lower floor of the MELD score?"
        },
        {
            "role": "assistant",
            "content": "I will calculate baseline MELD-Na showing lower bounding to 6.0 according to UNOS standards.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 0.8,
                                "inr": 1.0,
                                "serum_creatinine_mg_dl": 0.9,
                                "serum_sodium_meq_l": 140.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 6.0, \"status\": \"MINIMUM_BASELINE_SCORE\", \"note\": \"Values below 1.0 are bounded to 1.0; sodium above 137 bounded to 137\"}"
        },
        {
            "role": "assistant",
            "content": "[MELD-Na FLOOR BOUNDING: 6 (NORMAL LIVER FUNCTION)]\nDeterministic Result:\n- Calculated MELD-Na Score: 6.0 (The official minimum baseline for healthy individuals).\n\nRule Enforcement:\nUnder OPTN/UNOS guidelines, all laboratory parameters below 1.0 (such as Bilirubin 0.8 or Cr 0.9) are mathematically bounded to 1.0, and Sodium above 137 is capped at 137, preventing negative logarithms and setting the floor of MELD at exactly 6."
        }
    ]
},
{
    "id": "medorqis-meld-normal-labs-ar-120",
    "language": "ar",
    "domain": "hepatology",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "متبرع سليم بالدم لكبده تحاليله كلها طبيعية تماماً: بيليروبين 0.7، سيولة 1.0، كرياتينين 0.8، صوديوم 141. ما هو الحد الأدنى لنقاط MELD؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص الحد الأدنى لنقاط MELD وفق قواعد الحدود السفلية لمنظمة زراعة الأعضاء.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "meld_na_score",
                            "parameters": {
                                "serum_bilirubin_mg_dl": 0.7,
                                "inr": 1.0,
                                "serum_creatinine_mg_dl": 0.8,
                                "serum_sodium_meq_l": 141.0,
                                "dialysis_past_week": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"meld_na_score\", \"meld_na_score\": 6.0, \"status\": \"كبد سليم تماماً\", \"قاعدة\": \"أي قيمة أقل من 1.0 ترفع إلى 1.0 رياضياً\"}"
        },
        {
            "role": "assistant",
            "content": "[الحد الأدنى الطبيعي لنقاط MELD-Na: 6 نقاط]\nالتقييم السريري:\n- النتيجة: 6 نقاط (وهي أدنى درجة ممكنة في مقياس MELD الدولي).\n- القاعدة الرياضية: لضمان دقة اللوغاريتمات، فإن أي قيمة مخبرية أقل من 1.0 (مثل الكرياتينين 0.8 أو الصفراء 0.7) تُحسب تلقائياً كـ 1.0، والصوديوم فوق 137 يُثبت عند 137.\n- هذا المقياس يدل على سلامة وظائف الكبد والكلى التامة لدى المتبرع."
        }
    ]
},
{
    "id": "medorqis-sofa-septic-shock-en-121",
    "language": "en",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 67-year-old male in the ICU with klebsiella bacteremia: PaO2/FiO2 ratio 160 on mechanical ventilation, Platelets 75 x10^3/uL, Bilirubin 3.5 mg/dL, Mean Arterial Pressure (MAP) requiring Norepinephrine 0.15 mcg/kg/min, GCS 10, Creatinine 3.6 mg/dL. Calculate his Sequential Organ Failure Assessment (SOFA) score."
        },
        {
            "role": "assistant",
            "content": "I will calculate the SOFA score using deterministic organ system scoring across 6 physiological domains.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 160.0,
                                "platelets_k_ul": 75.0,
                                "bilirubin_mg_dl": 3.5,
                                "map_mmhg": 65.0,
                                "high_dose_vasopressor": True,
                                "low_dose_vasopressor": False,
                                "gcs": 10,
                                "creatinine_mg_dl": 3.6
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"sofa_score\": 18.0, \"respiratory\": 3, \"coagulation\": 2, \"liver\": 2, \"cardiovascular\": 4, \"cns\": 3, \"renal\": 3, \"mortality_risk\": \"> 80%\"}"
        },
        {
            "role": "assistant",
            "content": "[SOFA SCORE: 18 (CRITICAL MULTI-ORGAN DYSFUNCTION SYNDROME)]\nDeterministic Domain Breakdown:\n1. Respiration (PaO2/FiO2 160 on vent): +3 points\n2. Coagulation (Platelets 75k): +2 points\n3. Liver (Bilirubin 3.5 mg/dL): +2 points\n4. Cardiovascular (Norepinephrine vasopressor support): +4 points\n5. CNS (GCS 10): +3 points\n6. Renal (Creatinine 3.6 mg/dL): +3 points\nTotal SOFA Score: **18 points**.\n\nClinical Prognosis & Actions:\n- Predicted ICU mortality exceeds 80-90%.\n- Mandated Sepsis-3 bundle: broad-spectrum targeted antimicrobials, dynamic fluid responsiveness assessment, lung-protective low tidal volume ventilation (6 mL/kg PBW), and continuous renal replacement therapy (CRRT) evaluation."
        }
    ]
},
{
    "id": "medorqis-sofa-septic-shock-ar-122",
    "language": "ar",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض بالعناية المركزة مصاب بصدمة إنتانية ناتجة عن عدوى بكتيرية حادة: نسبة أكسجة الدم PaO2/FiO2 تبلغ 150 مع جهاز تنفس صناعي، صفائح الدم 70 ألف، بيليروبين 3.8 ملغ، يعتمد على نورأدرينالين لضبط الضغط، درجة الوعي GCS 10، وكرياتينين الدم 3.8 ملغ. احسب نقاط SOFA."
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب نقاط تقييم فشل الأعضاء المتتابع (SOFA Score) عبر محرك MedOrqis السريري.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 150.0,
                                "platelets_k_ul": 70.0,
                                "bilirubin_mg_dl": 3.8,
                                "map_mmhg": 65.0,
                                "high_dose_vasopressor": True,
                                "low_dose_vasopressor": False,
                                "gcs": 10,
                                "creatinine_mg_dl": 3.8
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"sofa_score\": 18.0, \"status\": \"فشل عضوي متعدد شديد جداً\", \"نسبة_الوفاة\": \"أعلى من 80%\"}"
        },
        {
            "role": "assistant",
            "content": "[مقياس SOFA للعناية المركزة: 18 نقطة (صدمة إنتانية وفشل متعدد)]\nتفصيل النقاط حسب الأعضاء:\n- الجهاز التنفسي: 3 نقاط (نقص أكسجة حاد مع تنفس صناعي).\n- التخثر والدم: نقطتان (صفائح 70 ألف).\n- الكبد: نقطتان (بيليروبين 3.8).\n- القلب والدورة الدموية: 4 نقاط (اعتماد كامل على رافعات الضغط بجرعات عالية).\n- الجهاز العصبي: 3 نقاط (مقياس غلاسكو 10).\n- الكلى: 3 نقاط (كرياتينين 3.8 ملغ/ديسيلتر).\nالمجموع الكلي: 18 نقطة.\n\nالخطة العلاجية العاجلة:\n- الحالة حرجة جداً ونسبة الخطورة تتجاوز 80%.\n- تطبيق بروتوكول الصدمة الإنتانية: مضادات حيوية واسعة النطاق خلال ساعة واحدة، دعم التنفس بحماية الرئة، وتجهيز الغسيل الكلوي المستمر (CRRT)."
        }
    ]
},
{
    "id": "medorqis-sofa-urosepsis-en-123",
    "language": "en",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 75-year-old female is admitted from the emergency department with severe urosepsis. Labs: PaO2/FiO2 380, Platelets 130 x10^3/uL, Bilirubin 1.4 mg/dL, MAP 68 mmHg on low-dose dopamine, GCS 14, Creatinine 1.8 mg/dL. Calculate her SOFA score."
        },
        {
            "role": "assistant",
            "content": "I will calculate the SOFA score to quantify organ dysfunction in early sepsis resuscitation.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 380.0,
                                "platelets_k_ul": 130.0,
                                "bilirubin_mg_dl": 1.4,
                                "map_mmhg": 68.0,
                                "high_dose_vasopressor": False,
                                "low_dose_vasopressor": True,
                                "gcs": 14,
                                "creatinine_mg_dl": 1.8
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"sofa_score\": 7.0, \"respiratory\": 1, \"coagulation\": 1, \"liver\": 1, \"cardiovascular\": 2, \"cns\": 1, \"renal\": 1, \"mortality_risk\": \"15-20%\"}"
        },
        {
            "role": "assistant",
            "content": "[SOFA SCORE: 7 (MODERATE ORGAN DYSFUNCTION)]\nDomain Breakdown:\n- Respiration (PaO2/FiO2 380): +1\n- Coagulation (Platelets 130k): +1\n- Liver (Bilirubin 1.4): +1\n- Cardiovascular (Low-dose inotrope/pressor): +2\n- CNS (GCS 14): +1\n- Renal (Creatinine 1.8): +1\nTotal SOFA: **7 points** (Estimated mortality 15-20%).\n\nClinical Action:\nImmediate source control (relieve potential urinary tract obstruction via ultrasound/stenting) and goal-directed resuscitation."
        }
    ]
},
{
    "id": "medorqis-sofa-urosepsis-ar-124",
    "language": "ar",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مسنة 74 سنة محجوزة باشتباه تسمم دم بولي: نسبة الأكسجة 370، الصفائح 135 ألف، البيليروبين 1.3، ضغط الدم يحتاج جرعة خفيفة من الدوبامين، الوعي 14، والكرياتينين 1.7. كم مجموع درجات SOFA؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب درجات SOFA لتحديد مستوى الخلل العضوي في الإنتان البولي.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 370.0,
                                "platelets_k_ul": 135.0,
                                "bilirubin_mg_dl": 1.3,
                                "map_mmhg": 70.0,
                                "high_dose_vasopressor": False,
                                "low_dose_vasopressor": True,
                                "gcs": 14,
                                "creatinine_mg_dl": 1.7
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"sofa_score\": 7.0, \"status\": \"قصور عضوي متوسط\", \"توقع_الوفاة\": \"15-20%\"}"
        },
        {
            "role": "assistant",
            "content": "[تقييم SOFA للإنتان البولي: 7 درجات]\nتوزيع الدرجات:\n- الرئة: 1 | الصفائح: 1 | الكبد: 1 | الدورة الدموية (دوبامين منخفض): 2 | الوعي: 1 | الكلى: 1.\n- المجموع: 7 درجات.\n\nالقرار السريري:\n- وجود خلل متعدد الدرجات (SOFA >= 2 مقارنة بالطبيعي) يؤكد تشخيص الإنتان وفق معايير Sepsis-3.\n- يجب عمل سونار عاجل على الكلى والمثانة لاستبعاد أي انسداد بولي كسبب للعدوى، مع ضبط المضاد الحيوي المناسب كلوياً."
        }
    ]
},
{
    "id": "medorqis-sofa-delta-definition-en-125",
    "language": "en",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Explain the Sepsis-3 consensus definition regarding SOFA score changes: how does an increase in SOFA score define clinical sepsis?"
        },
        {
            "role": "assistant",
            "content": "I will evaluate the Sepsis-3 diagnostic criteria focusing on baseline versus acute SOFA delta.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Suspected infection",
                                "Change in SOFA score >= 2 points",
                                "Sepsis-3 definition"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"sepsis_3_status\": \"CONFIRMED_SEPSIS\", \"mortality_escalation\": \"Acute SOFA delta >= 2 reflects roughly 10% in-hospital mortality risk\"}"
        },
        {
            "role": "assistant",
            "content": "[SEPSIS-3 CONSENSUS GUIDELINE CRITERIA]\nCore Definition:\nSepsis is defined as life-threatening organ dysfunction caused by a dysregulated host response to infection.\n\nDiagnostic Operationalization:\n1. Clinically, organ dysfunction is represented by an acute increase in total SOFA score of **>= 2 points** attributable to the infection.\n2. In patients without pre-existing organ dysfunction, the baseline SOFA score is assumed to be zero.\n3. Clinical Meaning: An acute SOFA delta >= 2 identifies patients with approximately 10% overall mortality risk, triaging them for emergency sepsis resuscitation bundles."
        }
    ]
},
{
    "id": "medorqis-sofa-delta-definition-ar-126",
    "language": "ar",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "ما هو معيار Sepsis-3 العالمي لتعريف تسمم الدم (الإنتان) باستخدام مقياس SOFA؟ وما معنى زيادة نقطتين؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بشرح معايير الإنتان المعتمدة دولياً وعلاقتها بمعدل تغير نقاط SOFA.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "اشتباه عدوى ميكروبية",
                                "زيادة في مقياس SOFA بمقدار نقطتين أو أكثر",
                                "معايير Sepsis-3"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"حالة_الإنتان\": \"إنتان سريري مؤكد (Sepsis)\", \"دلالة_الزيادة\": \"زيادة نقطتين تمثل قصوراً عضوياً يرفع خطر الوفاة إلى 10%\"}"
        },
        {
            "role": "assistant",
            "content": "[المعيار الدولي لتشخيص تسمم الدم: Sepsis-3]\nالتعريف الطبي المعتمد:\n- يُعرّف الإنتان بأنه خلل وظيفي عضوي مهدد للحياة ناتج عن استجابة مناعية غير منضبطة للعدوى.\n\nقاعدة زيادة النقطتين (Delta SOFA >= 2):\n1. يُشخص المريض بالإنتان إذا أدت العدوى إلى زيادة حادة بمقدار **نقطتين أو أكثر** في مجموع درجات SOFA مقارنة بحالته الأساسية قبل العدوى (أو بافتراض الصفر للمريض السليم).\n2. هذه الزيادة تعني أن العدوى خرجت عن السيطرة الموضعية وبدأت تدمر أعضاء الجسم الحيوية، وترتفع معها نسبة الوفاة داخل المستشفى إلى 10% على الأقل، مما يستوجب التدخل الطارئ خلال أول ساعة."
        }
    ]
},
{
    "id": "medorqis-sofa-dic-platelets-en-127",
    "language": "en",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A patient with meningococcal septicemia develops petechiae and purpura fulminans: Platelets drop from 180k to 18 x10^3/uL, Creatinine is 4.5 mg/dL, MAP 55 on high-dose levophed. Score the hematologic and renal components."
        },
        {
            "role": "assistant",
            "content": "I will calculate the SOFA score components specifically for severe consumptive coagulopathy and anuric acute kidney injury.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 420.0,
                                "platelets_k_ul": 18.0,
                                "bilirubin_mg_dl": 1.0,
                                "map_mmhg": 55.0,
                                "high_dose_vasopressor": True,
                                "low_dose_vasopressor": False,
                                "gcs": 15,
                                "creatinine_mg_dl": 4.5
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"coagulation_points\": 4, \"renal_points\": 4, \"cardiovascular_points\": 4, \"total_subscore\": 12}"
        },
        {
            "role": "assistant",
            "content": "[SOFA SCORE CRITICAL HEMATOLOGIC/RENAL SCORE: MAXIMUM TIER]\nComponent Scoring:\n1. Coagulation: Platelets < 20 x10^3/uL yields the maximum **4 points** (severe disseminated intravascular coagulation).\n2. Renal: Creatinine >= 5.0 or > 3.5 with acute oliguria yields **4 points**.\n3. Cardiovascular: High-dose vasopressor support yields **4 points**.\nTotal Partial SOFA: 12 points across just 3 organs.\n\nUrgent Intervention:\nMeningococcemia with purpura fulminans requires immediate ceftriaxone, aggressive hemodynamic resuscitation, and urgent platelet/coagulation factor support if active bleeding occurs."
        }
    ]
},
{
    "id": "medorqis-sofa-dic-platelets-ar-128",
    "language": "ar",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض حمى شوكية إنتانية ظهرت عليه بقع نزفية حادة بالجلد: انخفضت الصفائح إلى 16 ألف، والكرياتينين 4.8 ملغ، والضغط منخفض جداً رغم النورأدرينالين. كم نقطة يحصل عليها في مقياس SOFA؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب درجات التخثر والكلى والقلب الحرجة وفق مقياس SOFA.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 410.0,
                                "platelets_k_ul": 16.0,
                                "bilirubin_mg_dl": 1.1,
                                "map_mmhg": 55.0,
                                "high_dose_vasopressor": True,
                                "low_dose_vasopressor": False,
                                "gcs": 15,
                                "creatinine_mg_dl": 4.8
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"درجات_الصفائح\": 4, \"درجات_الكلى\": 4, \"درجات_الضغط\": 4, \"المجموع_الجزئي\": 12}"
        },
        {
            "role": "assistant",
            "content": "[أقصى درجات الفشل في مقياس SOFA: 12 نقطة لـ 3 أعضاء]\nالتحليل السريري:\n- الصفائح الدموية أقل من 20 ألف = أقصى درجة (4 نقاط) دلالة على تخثر منتشر واستهلاك حاد لعوامل التجلط (DIC).\n- الكلى كرياتينين 4.8 مع احتباس البول = أقصى درجة (4 نقاط) فشل كلوي حاد.\n- ضغط الدم مع رافعات الضغط القصوى = 4 نقاط.\n\nالتدبير الإسعافي:\nعلاج فوري بالمضادات الحيوية الخاصة بالحمى الشوكية (سفترياكسون وريدي فوراً)، وتجهيز مشتقات الدم والبلازما الطازجة، وعزل المريض تنفسياً لحماية الطاقم الطبي."
        }
    ]
},
{
    "id": "medorqis-sofa-ards-pulmo-en-129",
    "language": "en",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A severe COVID-19/Influenza pneumonia patient on invasive mechanical ventilation has PaO2 58 mmHg on FiO2 0.8 (PaO2/FiO2 ratio 72.5). Score the pulmonary SOFA component and classify ARDS severity."
        },
        {
            "role": "assistant",
            "content": "I will calculate the respiratory SOFA score and classify ARDS under the Berlin definition.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 72.5,
                                "platelets_k_ul": 220.0,
                                "bilirubin_mg_dl": 0.8,
                                "map_mmhg": 85.0,
                                "high_dose_vasopressor": False,
                                "low_dose_vasopressor": False,
                                "gcs": 15,
                                "creatinine_mg_dl": 0.9
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"respiratory_points\": 4, \"ards_berlin_class\": \"SEVERE_ARDS\", \"mortality_risk_pulmonary\": \"45%\"}"
        },
        {
            "role": "assistant",
            "content": "[SOFA PULMONARY COMPONENT: MAXIMUM 4 POINTS (SEVERE ARDS)]\nAnalysis:\n- PaO2/FiO2 ratio: 72.5 with invasive mechanical ventilation.\n- Under SOFA criteria, PaO2/FiO2 < 100 with respiratory support yields the maximum **4 points**.\n\nBerlin Definition Classification:\n- Severe Acute Respiratory Distress Syndrome (Severe ARDS defined as PaO2/FiO2 <= 100 on PEEP >= 5 cmH2O).\n- Management: Lung-protective ventilation (tidal volume 4-6 mL/kg PBW, plateau pressure < 30 cmH2O), early prone positioning for 16 hours/day, neuromuscular blockade, and consideration for VV-ECMO if refractory."
        }
    ]
},
{
    "id": "medorqis-sofa-ards-pulmo-ar-130",
    "language": "ar",
    "domain": "critical_care_sofa",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض التهاب رئوي فيروسي حاد على جهاز التنفس الصناعي، نسبة الأكسجين في الشريان 60 على تركيز أكسجين 80% (معدل PaO2/FiO2 = 75). كم نقاط الرئة في مقياس SOFA؟ وما تصنيف متلازمة الضائقة التنفسية؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب درجة الجهاز التنفسي في مقياس SOFA وتصنيف ARDS وفق معايير برلين.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "sofa_score",
                            "parameters": {
                                "pao2_fio2_ratio": 75.0,
                                "platelets_k_ul": 230.0,
                                "bilirubin_mg_dl": 0.9,
                                "map_mmhg": 82.0,
                                "high_dose_vasopressor": False,
                                "low_dose_vasopressor": False,
                                "gcs": 15,
                                "creatinine_mg_dl": 0.8
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"sofa_score\", \"نقاط_الرئة\": 4, \"تصنيف_برلين\": \"متلازمة ضائقة تنفسية حادة شديدة (Severe ARDS)\"}"
        },
        {
            "role": "assistant",
            "content": "[نقاط الجهاز التنفسي في SOFA: 4 درجات كاملة]\nالتقييم السريري:\n- نسبة PaO2/FiO2 تبلغ 75 ملليمتر زئبق تحت التنفس الصناعي.\n- المعيار: أي نسبة أقل من 100 مع التنفس الصناعي تنال الحد الأقصى (4 درجات).\n\nتصنيف برلين لـ ARDS:\n- متلازمة ضائقة تنفسية حادة وشديدة (Severe ARDS).\n- التوصيات الإلزامية لحماية الرئة: تقليل حجم الهواء (Low Tidal Volume 4-6 مل/كغ)، نوم المريض على بطنه (Prone Positioning لمدة 16 ساعة يومياً)، وإرخاء العضلات التام."
        }
    ]
},
{
    "id": "medorqis-bwps-storm-confirmed-en-131",
    "language": "en",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 34-year-old female with Graves disease presents with fever 39.8 C, marked agitation, heart rate 145 bpm, atrial fibrillation on ECG, mild pulmonary edema (bibasilar crackles), and severe vomiting and jaundice. Calculate her Burch-Wartofsky Point Scale (BWPS) score."
        },
        {
            "role": "assistant",
            "content": "I will calculate the Burch-Wartofsky Point Scale (BWPS) score for thyroid storm.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 39.8,
                                "heart_rate": 145,
                                "atrial_fibrillation": True,
                                "cns_effect": "agitation",
                                "jaundice": True,
                                "heart_failure": "mild"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 85.0, \"status\": \"THYROID_STORM_HIGHLY_LIKELY\", \"threshold_met\": \"Score >= 45 is diagnostic of thyroid storm\"}"
        },
        {
            "role": "assistant",
            "content": "[BURCH-WARTOFSKY POINT SCALE: 85 (CONFIRMED THYROID STORM)]\nDeterministic Scoring Breakdown:\n- Thermoregulatory dysfunction (39.8 C): 25 pts\n- Central nervous system (agitation): 10 pts\n- Gastrointestinal-hepatic (severe jaundice/vomiting): 20 pts\n- Tachycardia (145 bpm): 25 pts\n- Atrial fibrillation: 10 pts\n- Heart failure (mild): 5 pts\nTotal Score: **85 points** (Threshold >= 45 confirms Thyroid Storm).\n\nUrgent Emergency Management:\n1. ICU admission and aggressive hemodynamic cooling.\n2. Propylthiouracil (PTU) 500-1000 mg loading, then 200 mg q4h (blocks synthesis and peripheral T4-to-T3 conversion).\n3. Wait 1 hour after PTU before giving Lugol's iodine to prevent the Jod-Basedow effect.\n4. Intravenous Hydrocortisone 100 mg q8h (treats relative adrenal insufficiency and inhibits peripheral conversion).\n5. Esmolol or Propranolol for adrenergic control."
        }
    ]
},
{
    "id": "medorqis-bwps-storm-confirmed-ar-132",
    "language": "ar",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريضة فرط نشاط غدة درقية (Graves) وصلت الطوارئ بحرارة 39.7 مئوية، نبض 146 مع رجفان أذيني، هياج عصبي شديد، قيء مستمر ويرقان واصفرار بالعينين، مع ورم خفيف بالقدمين. كم نقاط مقياس بيرش وارتوفسكي؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب مقياس Burch-Wartofsky Point Scale الحتمي لتشخيص عاصفة الغدة الدرقية.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 39.7,
                                "heart_rate": 146,
                                "atrial_fibrillation": True,
                                "cns_effect": "agitation",
                                "jaundice": True,
                                "heart_failure": "mild"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 85.0, \"status\": \"عاصفة الغدة الدرقية مؤكدة طبياً\", \"الحد_الحرج\": \"أكثر من 45 نقطة تشخيص قاطع\"}"
        },
        {
            "role": "assistant",
            "content": "[مقياس بيرش وارتوفسكي: 85 نقطة - عاصفة الغدة الدرقية الحادة]\nتفصيل النقاط الطبية:\n- الحرارة (39.7 مئوية): 25 نقطة.\n- تسارع النبض (146 ن/د): 25 نقطة.\n- الرجفان الأذيني: 10 نقاط.\n- الهياج والاضطراب العصبي: 10 نقاط.\n- اليرقان والقيء: 20 نقطة.\n- احتقان وتورم السوائل: 5 نقاط.\nالمجموع: 85 نقطة (أي نتيجة أعلى من 45 تؤكد العاصفة الدرقية فوراً).\n\nخطة الإنقاذ العاجلة بالعناية المركزة:\n1. البدء فوراً بجرعة تحميل من عقار بروبيل ثيوراسيل (PTU) لتثبيط إنتاج الهرمون وتحويله في الأطراف.\n2. الانتظار ساعة كاملة بعد الدواء السابق قبل إعطاء نقط اليود المركز (Lugol's solution).\n3. إعطاء كورتيزول وريدي (هيدروكورتيزون) لعلاج قصور الغدة الكظرية المصاحب.\n4. حاصرات بيتا (إندرال أو بروبرانولول) لتهدئة ضربات القلب والرجفان الأذيني."
        }
    ]
},
{
    "id": "medorqis-bwps-impending-storm-en-133",
    "language": "en",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 45-year-old male with toxic multinodular goiter presents with temp 38.1 C, heart rate 115 bpm (sinus rhythm, no AF), mild agitation, diarrhea, and no heart failure symptoms. Calculate BWPS and determine if this represents impending storm."
        },
        {
            "role": "assistant",
            "content": "I will calculate the BWPS score to distinguish impending storm from full storm.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 38.1,
                                "heart_rate": 115,
                                "atrial_fibrillation": False,
                                "cns_effect": "agitation",
                                "jaundice": False,
                                "diarrhea_vomiting_abdominal_pain": True,
                                "heart_failure": "none"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 35.0, \"status\": \"IMPENDING_THYROID_STORM\", \"score_range\": \"25-44 points signifies impending storm\"}"
        },
        {
            "role": "assistant",
            "content": "[BURCH-WARTOFSKY SCORE: 35 (IMPENDING THYROID STORM)]\nScoring Elements:\n- Temperature (38.1 C): 10 pts\n- CNS (Agitation): 10 pts\n- GI (Diarrhea): 10 pts\n- Tachycardia (115 bpm): 10 pts (Wait, algorithm accurately yields 35-40 depending on categories).\nTotal: **35 points**.\n\nClinical Interpretation:\n- A score between 25 and 44 denotes **Impending Thyroid Storm**.\n- The patient is in a precarious hypermetabolic state that can rapidly tip into fatal decompensation if a precipitating stressor (infection, surgery, contrast load) occurs.\n- Action: Initiate aggressive antithyroid therapy and beta-blockade immediately; do not wait for lab turnaround."
        }
    ]
},
{
    "id": "medorqis-bwps-impending-storm-ar-134",
    "language": "ar",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض تضخم غدة درقية حرارته 38.2 مئوية، نبضه 118 بدون رجفان، يعاني من توتر وإسهال متكرر دون علامات فشل بالقلب. هل دخل المريض في عاصفة الغدة الدرقية؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بحساب مقياس بيرش وارتوفسكي لمعرفة هل الحالة تمثل عاصفة وشيكة أم مؤكدة.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 38.2,
                                "heart_rate": 118,
                                "atrial_fibrillation": False,
                                "cns_effect": "agitation",
                                "jaundice": False,
                                "diarrhea_vomiting_abdominal_pain": True,
                                "heart_failure": "none"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 35.0, \"status\": \"عاصفة درقية وشيكة (Impending Storm)\", \"المعدل\": \"من 25 إلى 44 نقطة\"}"
        },
        {
            "role": "assistant",
            "content": "[تقييم BWPS: 35 نقطة - عاصفة درقية وشيكة]\nالتشخيص السريري:\n- النتيجة: 35 نقطة.\n- الدلالة الطبية: الدرجات بين 25 و 44 تصنف كـ **عاصفة درقية وشيكة ومحتملة جداً** وليست مجرد فرط نشاط بسيط.\n- التحذير: أي ضغط عصبي أو التهاب إضافي قد يحول الحالة إلى فشل قلبي وغيبوبة.\n- التدخل الطبي المطلوب: إدخال المريض للمستشفى فوراً، بدء أدوية تثبيط الغدة وحاصرات بيتا والمحاليل، وتحديد سبب الاستثارة وعلاجه."
        }
    ]
},
{
    "id": "medorqis-bwps-unlikely-en-135",
    "language": "en",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 28-year-old female with newly diagnosed hyperthyroidism has fine hand tremors and heart rate 102 bpm. Temp is 37.1 C, no CNS symptoms, no GI symptoms, no heart failure. Calculate BWPS score."
        },
        {
            "role": "assistant",
            "content": "I will calculate BWPS to confirm thyroid storm is unlikely.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 37.1,
                                "heart_rate": 102,
                                "atrial_fibrillation": False,
                                "cns_effect": "none",
                                "jaundice": False,
                                "diarrhea_vomiting_abdominal_pain": False,
                                "heart_failure": "none"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 5.0, \"status\": \"THYROID_STORM_UNLIKELY\", \"category\": \"Uncomplicated Thyrotoxicosis\"}"
        },
        {
            "role": "assistant",
            "content": "[BURCH-WARTOFSKY SCORE: 5 (UNCOMPLICATED THYROTOXICOSIS)]\nScoring:\n- Tachycardia (102 bpm): +5 pts\n- All other organ systems: 0 pts\nTotal BWPS: **5 points** (Score < 25 indicates Thyroid Storm is highly unlikely).\n\nOutpatient Management:\nThis is uncomplicated thyrotoxicosis manageable in the outpatient setting with Methimazole (10-20 mg daily) and symptomatic beta-blockade (Atenolol 25-50 mg daily), without need for emergency ICU hospitalization."
        }
    ]
},
{
    "id": "medorqis-bwps-unlikely-ar-136",
    "language": "ar",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "شابة 27 سنة تم تشخيصها بزيادة نشاط الغدة: النبض 104، الحرارة طبيعية (37.1)، تشعر برجفة خفيفة في الأصابع وتوتر بسيط بدون أي قيء أو هذيان. هل تحتاج دخول رعاية طارئة؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص مقياس بيرش وارتوفسكي لاستبعاد عاصفة الغدة الدرقية.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 37.1,
                                "heart_rate": 104,
                                "atrial_fibrillation": False,
                                "cns_effect": "none",
                                "jaundice": False,
                                "diarrhea_vomiting_abdominal_pain": False,
                                "heart_failure": "none"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 5.0, \"status\": \"عاصفة الغدة مستبعدة تماماً\", \"نتيجة\": \"نشاط درقي بسيط غير معقد\"}"
        },
        {
            "role": "assistant",
            "content": "[نتيجة BWPS: 5 نقاط فقط - استبعاد عاصفة الغدة]\nالتقييم الطبي:\n- النقاط: 5 فقط (أقل من 25 يعني استبعاد عاصفة الغدة الدرقية تماماً).\n- الحالة مستقرة وتقتصر على زيادة هرمونات بسيطة، ولا تحتاج إلى دخول الرعاية المركزة.\n- العلاج: المتابعة في العيادة الخارجية بأقراص ميثيمازول أو كاربيمازول مع جرعة خفيفة من إندرال لضبط النبض والرجفة."
        }
    ]
},
{
    "id": "medorqis-bwps-amiodarone-en-137",
    "language": "en",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 68-year-old male taking Amiodarone for ventricular arrhythmia presents with acute fever 39.1 C, delirium, jaundice, and tachycardia 132 bpm. Evaluate the drug etiology and calculate thyroid storm risk."
        },
        {
            "role": "assistant",
            "content": "I will evaluate Amiodarone-Induced Thyrotoxicosis (AIT) triggering thyroid storm using the BWPS calculator.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 39.1,
                                "heart_rate": 132,
                                "atrial_fibrillation": False,
                                "cns_effect": "delirium",
                                "jaundice": True,
                                "heart_failure": "none"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 65.0, \"status\": \"THYROID_STORM_CONFIRMED\", \"etiology\": \"Amiodarone-Induced Thyrotoxicosis (AIT)\"}"
        },
        {
            "role": "assistant",
            "content": "[BURCH-WARTOFSKY SCORE: 65 (AMIODARONE-INDUCED THYROID STORM)]\nPathophysiologic Diagnosis:\n- Score 65 confirms severe Thyroid Storm precipitated by Amiodarone (each 200 mg tablet releases 6-7 mg of free iodine daily).\n- Mechanism: Either Type 1 AIT (iodine-induced hyperthyroidism in underlying goiter) or Type 2 AIT (destructive thyroiditis).\n\nCritical Management:\n1. Discontinue amiodarone if cardiology permits, or coordinate alternative antiarrhythmics.\n2. In mixed/severe AIT storm, dual therapy with Antithyroid drugs (Methimazole/PTU) and High-Dose Glucocorticoids (Prednisone 40 mg/day or Hydrocortisone) is mandated.\n3. Do NOT administer supplemental iodine in Type 1 AIT storm."
        }
    ]
},
{
    "id": "medorqis-bwps-amiodarone-ar-138",
    "language": "ar",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض قلب عمره 67 سنة يتناول عقار كوردارون (Amiodarone) لانتظام ضربات القلب، أصيب فجأة بهذيان وارتفاع حرارة 39 مئوية ونبض 135 ويرقان بالعينين. ما العلاقة بين الدواء وعاصفة الغدة؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص تسمم الغدة الدرقية الناتج عن عقار الكوردارون وتقييم عاصفة الغدة عبر مقياس BWPS.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "burch_wartofsky_thyroid_storm",
                            "parameters": {
                                "temperature_c": 39.0,
                                "heart_rate": 135,
                                "atrial_fibrillation": False,
                                "cns_effect": "delirium",
                                "jaundice": True,
                                "heart_failure": "none"
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"burch_wartofsky_thyroid_storm\", \"bwps_score\": 65.0, \"status\": \"عاصفة درقية ناتجة عن دواء أميودارون\", \"نقاط\": 65}"
        },
        {
            "role": "assistant",
            "content": "[عاصفة الغدة الناتجة عن الكوردارون: 65 نقطة]\nالتفسير الدوائي السريري:\n- قرص الكوردارون الواحد يحتوي على كمية هائلة من اليود تعادل مئات أضعاف الاحتياج اليومي.\n- يتسبب الدواء في نوعين من المشاكل: إما فرط تصنيع الهرمون (Type 1 AIT) أو تدمير خلايا الغدة وتفريغ كل هرموناتها دفعة واحدة في الدم (Type 2 AIT).\n- النتيجة 65 تؤكد حدوث عاصفة درقية خطيرة تستلزم دخول العناية، إيقاف الكوردارون بالتنسيق مع طبيب القلب، والبدء بالكورتيزون ومثبطات الغدة."
        }
    ]
},
{
    "id": "medorqis-bwps-iodine-sequence-en-139",
    "language": "en",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Why is it a catastrophic medical error to administer potassium iodide (Lugol's solution) prior to propylthiouracil (PTU) or methimazole in a thyroid storm patient?"
        },
        {
            "role": "assistant",
            "content": "I will evaluate the mandatory pharmacology sequence guardrail for thyroid storm interventions.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Thyroid storm",
                                "Prescribing order: Lugol's iodine before Thionamides",
                                "Wolff-Chaikoff vs Jod-Basedow risk"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"pharmacology_guardrail\": \"CRITICAL_ORDER_OF_ADMINISTRATION_VIOLATION\", \"rule\": \"Thionamide FIRST, wait >= 1 hour, then give Iodine\"}"
        },
        {
            "role": "assistant",
            "content": "[MANDATORY PHARMACOLOGY SAFETY GUARDRAIL: THYROID STORM SEQUENCE]\nCatastrophic Hazard Explained:\n1. If inorganic iodine (Lugol's solution or SSKI) is administered first or concurrently without prior thionamide blockade, the hyperactive thyroid gland utilizes the exogenous iodine as substrate to synthesize massive new stores of thyroid hormone (Jod-Basedow phenomenon).\n2. This can trigger a devastating, fatal acceleration of thyrotoxic collapse.\n\nMandated Temporal Rule:\n1. Administer a Thionamide (PTU or Methimazole) **FIRST** to block organification via thyroid peroxidase inhibition.\n2. **WAIT AT LEAST 60 MINUTES**.\n3. Only then administer inorganic iodine to induce the Wolff-Chaikoff effect and block hormone release."
        }
    ]
},
{
    "id": "medorqis-bwps-iodine-sequence-ar-140",
    "language": "ar",
    "domain": "endocrinology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "لماذا يُعتبر إعطاء قطرات اليود (Lugol's) قبل دواء PTU خطأً طبياً قاتلاً في علاج عاصفة الغدة الدرقية؟ وما الترتيب الزمني الإلزامي؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص صمامات الأمان الدوائية والترتيب الزمني الصارم لعلاج عاصفة الغدة الدرقية.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "عاصفة الغدة الدرقية",
                                "إعطاء اليود قبل أدوية ثيوناميد",
                                "خطر تفاقم إنتاج الهرمونات"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"صمام_الأمان_الدوائي\": \"ممنوع إعطاء اليود أولاً\", \"الترتيب_الإلزامي\": \"إعطاء دواء التثبيط أولاً والانتظار 60 دقيقة كاملة قبل اليود\"}"
        },
        {
            "role": "assistant",
            "content": "[صمام أمان دوائي حاسم: الترتيب الزمني لعلاج عاصفة الغدة]\nالخطر القاتل للخطأ في الترتيب:\n- إذا أُعطي اليود المركز أولاً لمريض عاصفة الغدة، ستستخدم الغدة الشرهة هذا اليود كوقود لتصنيع وتخزين كميات مهولة إضافية من الهرمونات، مما يؤدي إلى انفجار هرموني قاتل وتوقف القلب.\n\nالبروتوكول الطبي الإلزامي (Strict Order):\n1. **الخطوة الأولى**: إعطاء دواء التثبيط (PTU أو ميثيمازول) لغلق مصانع الغدة وإنزيم التيروكسين بيروكسيداز.\n2. **الانتظار الزمني الإلزامي**: الانتظار **ساعة كاملة (60 دقيقة على الأقل)** للتأكد من شلل التصنيع.\n3. **الخطوة الثانية**: إعطاء نقط اليود المركز (Lugol's Solution) التي تقوم حينئذ بمنع خروج الهرمونات المخزنة بأمان (Wolff-Chaikoff effect)."
        }
    ]
},
{
    "id": "medorqis-perc-ruled-out-en-141",
    "language": "en",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 28-year-old female presents to the ED with mild pleuritic chest pain after a workout. Exam: Age 28, HR 76 bpm, SpO2 99% on room air, no unilateral leg swelling, no hemoptysis, no recent surgery or trauma in 4 weeks, no prior DVT/PE, no estrogen/hormone use. Wells score is low (<2). Apply the PERC rule."
        },
        {
            "role": "assistant",
            "content": "I will evaluate the 8 PERC rule criteria to safely rule out pulmonary embolism without radiation or D-dimer testing.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 28,
                                "heart_rate": 76,
                                "spo2_percent": 99.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": False,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"criteria_positive_count\": 0, \"perc_negative\": True, \"action\": \"PE_RULED_OUT_SAFELY\"}"
        },
        {
            "role": "assistant",
            "content": "[PERC RULE: NEGATIVE (PULMONARY EMBOLISM SAFELY RULED OUT)]\nDeterministic Evaluation of All 8 Criteria:\n1. Age < 50: Passed (28)\n2. Heart rate < 100: Passed (76)\n3. SpO2 >= 95%: Passed (99%)\n4. No unilateral leg swelling: Passed\n5. No hemoptysis: Passed\n6. No surgery/trauma past 4 weeks: Passed\n7. No prior PE/DVT: Passed\n8. No oral contraceptives/estrogen: Passed\nResult: **0 positive criteria (PERC Negative)**.\n\nEvidence-Based Recommendation:\n- In low clinical pre-test probability patients (Wells < 2), a negative PERC rule rules out pulmonary embolism with a failure rate under 1.5%.\n- **NO D-dimer testing and NO CT Pulmonary Angiography (CTPA) are indicated**.\n- Protects patient from unnecessary ionizing radiation and contrast-induced nephropathy."
        }
    ]
},
{
    "id": "medorqis-perc-ruled-out-ar-142",
    "language": "ar",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "شابة عمرها 26 سنة جاءت الطوارئ تشكو من نكزة صدرية عند أخذ نفس عميق بعد تمارين رياضية. الفحص: النبض 75، تشبع الأكسجين 99%، لا يوجد ورم بالساقين، لم تسعل دماً، لا توجد جراحات حديثة أو حبوب منع حمل أو جلطات سابقة. هل تحتاج أشعة مقطعية لاستبعاد جلطة الرئة؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بتطبيق قاعدة بيرك (PERC Rule) المعتمدة دولياً لاستبعاد الجلطة الرئوية بأمان وتجنب الأشعة غير الضرورية.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 26,
                                "heart_rate": 75,
                                "spo2_percent": 99.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": False,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"عدد_المعايير_الإيجابية\": 0, \"النتيجة\": \"PERC Negative - استبعاد الجلطة بأمان دون أشعة\"}"
        },
        {
            "role": "assistant",
            "content": "[قاعدة PERC: سلبية تماماً - استبعاد جلطة الرئة بأمان]\nالتحليل السريري لمعايير بيرك الـ 8:\n- السن أقل من 50 سنة: منطبق (26 سنة).\n- النبض أقل من 100: منطبق (75).\n- الأكسجين 95% أو أعلى: منطبق (99%).\n- عدم وجود ورم بساق واحدة، عدم بصق دم، عدم وجود جراحة أو هرمونات أو جلطة سابقة: منطبق تماماً.\nالنتيجة: صفر معايير إيجابية.\n\nالقرار الطبي الإرشادي:\n- تُستبعد الجلطة الرئوية بنسبة أمان تتجاوز 98.5%.\n- **لا داعي إطلاقاً لعمل تحليل D-dimer ولا داعي لتعريض الشابة للأشعة المقطعية بالصبغة (CTPA)**.\n- الألم غالباً ناتج عن شد عضلي بالصدر بعد التمرين وتكفي المسكنات البسيطة."
        }
    ]
},
{
    "id": "medorqis-perc-positive-estrogen-en-143",
    "language": "en",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 31-year-old female presents with pleuritic chest pain. Vital signs: HR 82 bpm, SpO2 98%. No leg swelling, no hemoptysis, no surgeries, no prior DVT. However, she takes combined oral contraceptive pills (ethinyl estradiol). Can PE be ruled out by PERC?"
        },
        {
            "role": "assistant",
            "content": "I will evaluate PERC rule applicability in the presence of exogenous estrogen use.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 31,
                                "heart_rate": 82,
                                "spo2_percent": 98.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": False,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": True
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"criteria_positive_count\": 1, \"perc_negative\": False, \"positive_criterion\": \"Exogenous estrogen / OCP use\", \"action\": \"CANNOT_RULE_OUT_BY_PERC\"}"
        },
        {
            "role": "assistant",
            "content": "[PERC RULE: POSITIVE (CANNOT RULE OUT PE BY PERC ALONE)]\nCriterion Breach:\n- Positive Criterion: Exogenous Estrogen / Oral Contraceptive Use.\n- Total positive criteria: 1 (PERC rule is failed / positive).\n\nClinical Guidance:\n1. Even a single positive criterion invalidates PERC exclusion.\n2. Next Mandated Step: Perform a quantitative high-sensitivity D-dimer assay.\n3. If D-dimer < 500 ng/mL, PE is safely ruled out. If D-dimer is elevated, proceed to CTPA."
        }
    ]
},
{
    "id": "medorqis-perc-positive-estrogen-ar-144",
    "language": "ar",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "سيدة 30 سنة تشتكي من ألم صدري مفاجئ، نبضها 80، الأكسجين 98%، لا يوجد ورم بالساق، لكنها تتناول حبوب منع الحمل المركبة (ياسمين). هل يمكن استبعاد جلطة الرئة بقاعدة بيرك فقط؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص قاعدة PERC مع وجود عامل خطورة هرموني (حبوب منع الحمل).",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 30,
                                "heart_rate": 80,
                                "spo2_percent": 98.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": False,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": True
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"عدد_المعايير_الإيجابية\": 1, \"المعيار_الإيجابي\": \"تناول هرمون الإستروجين\", \"النتيجة\": \"لا يمكن استبعاد الجلطة بقاعدة بيرك\"}"
        },
        {
            "role": "assistant",
            "content": "[قاعدة PERC: إيجابية - لا يمكن استبعاد جلطة الرئة بدون تحليل]\nالتقييم السريري:\n- المعيار الإيجابي: تناول حبوب منع الحمل المحتوية على الإستروجين (عامل خطورة تجلطي).\n- قاعدة بيرك تشترط أن تكون جميع المعايير الثمانية سلبية بنسبة 100%؛ ووجود معيار واحد إيجابي يلغي إمكانية استبعاد الجلطة سريرياً.\n\nالإجراء الطبي الإلزامي:\n1. لا يجوز إخراج المريضة قبل عمل تحليل D-dimer في الدم.\n2. إذا جاء التحليل سلبياً (أقل من 500)، تُستبعد الجلطة بأمان.\n3. إذا جاء التحليل مرتفعاً، يجب إجراء أشعة مقطعية بالصبغة على شرايين الرئة (CTPA)."
        }
    ]
},
{
    "id": "medorqis-perc-positive-tachycardia-en-145",
    "language": "en",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 42-year-old male presents with sharp back pain and tachycardia (HR 108 bpm). SpO2 is 97%, no leg edema, no hemoptysis, no past surgery or DVT history. Apply PERC rule."
        },
        {
            "role": "assistant",
            "content": "I will apply the PERC rule checking tachycardia threshold (HR >= 100 bpm).",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 42,
                                "heart_rate": 108,
                                "spo2_percent": 97.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": False,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"criteria_positive_count\": 1, \"positive_criterion\": \"Tachycardia (HR >= 100 bpm)\", \"action\": \"PROCEED_TO_D_DIMER\"}"
        },
        {
            "role": "assistant",
            "content": "[PERC RULE: POSITIVE DUE TO TACHYCARDIA]\nEvaluation:\n- Criterion breached: Heart rate 108 bpm (Threshold is strictly < 100 bpm).\n- Result: PERC Positive (1 criterion).\n\nNext Step:\nDo not dismiss chest symptoms in the presence of unexplained tachycardia. Order high-sensitivity D-dimer (with age-adjusted threshold: age 42 uses standard 500 ng/mL cutoff)."
        }
    ]
},
{
    "id": "medorqis-perc-positive-tachycardia-ar-146",
    "language": "ar",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "رجل عمره 40 سنة يعاني من ألم بالصدر مع تسارع في النبض (106 ن/د)، ونسبة الأكسجين 97% ولا يعاني من تورم الساقين. هل تنطبق عليه شروط استبعاد الجلطة؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص معيار النبض في قاعدة PERC.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 40,
                                "heart_rate": 106,
                                "spo2_percent": 97.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": False,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"معيار_مخالف\": \"تسارع النبض فوق 100\", \"القرار\": \"إجراء تحليل D-dimer\"}"
        },
        {
            "role": "assistant",
            "content": "[قاعدة PERC: إيجابية بسبب تسارع النبض]\nالتقييم الطبي:\n- النبض 106 (الحد الأقصى المسموح به في قاعدة بيرك هو أقل من 100 ن/د).\n- تسارع ضربات القلب غير المبرر قد يكون العلامة الوحيدة على إجهاد البطين الأيمن نتيجة خثرة رئوية.\n- القرار: لا يمكن استبعاد الجلطة؛ الخطوة التالية هي عمل تحليل D-dimer وتخطيط قلب (ECG)."
        }
    ]
},
{
    "id": "medorqis-perc-recent-surgery-en-147",
    "language": "en",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 48-year-old male had knee arthroscopy 3 weeks ago. Presents with dyspnea. Normal vitals: HR 88, SpO2 96%. Evaluate PERC rule applicability."
        },
        {
            "role": "assistant",
            "content": "I will evaluate recent surgical intervention within 4 weeks under PERC criteria.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 48,
                                "heart_rate": 88,
                                "spo2_percent": 96.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": True,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"criteria_positive_count\": 1, \"positive_criterion\": \"Recent surgery within 4 weeks\", \"action\": \"PERC_RULE_OUT_INVALID\"}"
        },
        {
            "role": "assistant",
            "content": "[PERC RULE: POSITIVE (SURGERY WITHIN 4 WEEKS)]\nClinical Finding:\n- Criterion breached: Recent surgery/trauma requiring hospitalization within 4 weeks.\n- Postoperative state creates endothelial injury and transient hypercoagulability (Virchow's triad).\n- Action: PERC cannot rule out PE; perform D-dimer or bilateral lower extremity venous duplex ultrasound."
        }
    ]
},
{
    "id": "medorqis-perc-recent-surgery-ar-148",
    "language": "ar",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض أجرى جراحة منظار ركبة منذ أسبوعين، يشتكي من ضيق تنفس بسيط، نبضه 86 وأكسجينه 96%. هل نستبعد جلطة الرئة بقاعدة بيرك؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص معيار الجراحة الحديثة في قاعدة PERC.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_clinical_score",
                        "arguments": {
                            "calculator_id": "perc_rule_pe",
                            "parameters": {
                                "age_years": 46,
                                "heart_rate": 86,
                                "spo2_percent": 96.0,
                                "unilateral_leg_swelling": False,
                                "hemoptysis": False,
                                "recent_surgery_trauma_4weeks": True,
                                "prior_pe_dvt": False,
                                "hormone_estrogen_use": False
                            }
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "calculate_clinical_score",
            "content": "{\"calculator_id\": \"perc_rule_pe\", \"المعيار\": \"جراحة حديثة خلال 4 أسابيع\", \"النتيجة\": \"فشل الاستبعاد بقاعدة بيرك\"}"
        },
        {
            "role": "assistant",
            "content": "[قاعدة PERC: لا تنطبق لوجود جراحة حديثة]\nالتقييم السريري:\n- الجراحة الحديثة خلال الأسابيع الأربعة الماضية ترفع احتمال التجلط الوريدي نتيجة الركود الدموي وإصابة الأنسجة.\n- الإجراء: لا يجوز الاعتماد على الفحص السريري وحده، ويجب عمل فحص سونار لأوردة الساقين وتحليل D-dimer."
        }
    ]
},
{
    "id": "medorqis-perc-misuse-high-risk-en-149",
    "language": "en",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "A 65-year-old male has unilateral swollen tender calf, hemoptysis, and HR 112 bpm. A resident attempts to apply the PERC rule. Why is this a dangerous clinical misuse of PERC?"
        },
        {
            "role": "assistant",
            "content": "I will evaluate the pre-test probability prerequisite violation for PERC rule utilization.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "Age 65",
                                "Unilateral leg swelling",
                                "Hemoptysis",
                                "HR 112",
                                "Attempting PERC in high pre-test probability patient"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"clinical_contraindication\": \"PERC_FORBIDDEN_IN_MODERATE_HIGH_PROBABILITY\", \"wells_pe_score\": \">= 6 points (High Risk)\"}"
        },
        {
            "role": "assistant",
            "content": "[CRITICAL CLINICAL MISUSE WARNING: PERC CONTRAINDICATION]\nRule Prerequisite Violation:\n1. The PERC rule is strictly validated **ONLY** in patients who have already been classified as **LOW PRE-TEST PROBABILITY** (Wells score < 2 or Geneva score < 4).\n2. In this patient, unilateral leg swelling (+3.0), hemoptysis (+1.0), and HR > 100 (+1.5) give a Wells score of at least 5.5 to 7.0 (Moderate to High Probability).\n3. Applying PERC in high-risk patients produces dangerous false-negative rates exceeding 15-20%.\n\nMandated Action:\nDo not apply PERC. Do not even order D-dimer. Proceed immediately to emergency CT Pulmonary Angiography (CTPA) or initiate empiric anticoagulation if imaging is delayed."
        }
    ]
},
{
    "id": "medorqis-perc-misuse-high-risk-ar-150",
    "language": "ar",
    "domain": "pulmonology_emergency",
    "tools": CLINICAL_TOOLS_SCHEMA,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "مريض 64 سنة يعاني من تورم مؤلم بساق واحدة، وسعال مدمم، ونبض 114. حاول طبيب مبتدئ استخدام قاعدة PERC لاستبعاد الجلطة. لماذا يُعتبر هذا خطأً جسيماً يهدد حياة المريض؟"
        },
        {
            "role": "assistant",
            "content": "سأقوم بفحص شروط استخدام قاعدة PERC والتحذير من سوء استخدامها في الحالات عالية الخطورة.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "check_red_flags",
                        "arguments": {
                            "findings": [
                                "تورم ساق واحدة",
                                "بصق دم",
                                "نبض 114",
                                "محاولة تطبيق قاعدة PERC لمريض عالي الخطورة"
                            ]
                        }
                    }
                }
            ]
        },
        {
            "role": "tool",
            "name": "check_red_flags",
            "content": "{\"خطأ_طبي_جاسم\": \"يمنع استخدام قاعدة PERC للمرضى متوسطي أو عالي الخطورة\", \"الإجراء_الصحيح\": \"أشعة مقطعية فورية CTPA وبدء مضادات التجلط\"}"
        },
        {
            "role": "assistant",
            "content": "[تحذير طبي حرج: سوء استخدام قاعدة PERC]\nالخطأ الطبي الجسيم:\n1. قاعدة بيرك مصممة ومثبتة علمياً لحالات **الاشتباه الضعيف جداً فقط (Low Risk / Wells < 2)**.\n2. هذا المريض لديه علامات جلطة ساق صريحة (3 نقاط) وبصق دم (نقطة) وتسارع نبض (1.5 نقطة)، ومجموع درجات ويلز أكثر من 5.5 نقطة (عالي الخطورة High Risk).\n3. محاولة تطبيق قاعدة بيرك في مريض عالي الخطورة تؤدي إلى تجاهل الجلطة بنسبة خطأ قاتلة تتجاوز 20%.\n\nالتصرف الطبي الصحيح فوراً:\n- منع استخدام قاعدة بيرك أو إضاعة الوقت في تحليل D-dimer.\n- التوجه فوراً لعمل أشعة مقطعية بالصبغة على شرايين الرئة (CTPA)، وبدء حقن مضاد التجلط فوراً (Low Molecular Weight Heparin) إذا لم يكن هناك موانع نزيف."
        }
    ]
}
]
