---
annotations_creators:
- expert-generated
- synthetic
language_creators:
- expert-generated
language:
- ar
- en
license: other
license_name: proprietary-restricted
multilinguality:
- bilingual
size_categories:
- 1K<n<10K
source_datasets:
- original
- physionet/mimic-iv-demo
task_categories:
- text-generation
- question-answering
task_ids: []
pretty_name: MedOrqis Clinical Instructions & MIMIC-IV Real Data
tags:
- medical
- clinical-reasoning
- tool-calling
- function-calling
- arabic-medical
- mimic-iv
- nephrology
- hepatology
- critical-care
- safety-guardrails
---

# MedOrqis Clinical Instructions & Tool Calling Dataset (1,258 Records)

The official foundational instruction-tuning and function-calling dataset for the **MedOrqis Medical Foundation Model** (`seotarek/medorqis-karnak-40b-lora`), built on top of `Applied-Innovation-Center/Karnak-40B-v1.0` and `Karnak-6B-v1.0`.

## Key Highlights

- **Bilingual (Arabic & English)**: Clinical scenarios encompassing Standard Medical Arabic, English, and regional dialect complaints.
- **Real-World Clinical Data (MIMIC-IV Demo v2.2)**: 1,058 empirical clinical cases derived directly from authentic ICU and inpatient admissions with genuine lab values (serum creatinine, bilirubin, sodium, INR, platelets).
- **Curated Clinical Scenarios**: 200 guideline-grounded scenarios across cardiology, nephrology, Beers 2023 geriatrics, emergency toxicology, and hospital EHR.
- **Native Tool-Calling (<tool_call>)**: Formatted specifically for Karnak / Qwen ChatML tool schemas.
- **Deterministic Clinical Grounding**: Prompts the LLM to invoke deterministic zero-token calculators rather than guessing mathematical clinical risk scores.
  - `cha2ds2_va_esc2024` (ESC 2024 Atrial Fibrillation Stroke Risk)
  - `ckd_epi_2021_egfr` (KDIGO 2024 Race-Free Renal Equation)
  - `bedside_schwartz_egfr` (Pediatric eGFR)
  - `curb65_score` & `news2_score` (Infection & Acute Deterioration)
  - `wells_dvt_score` & `wells_pe_score` (Thromboembolism)
  - `pediatric_weight_dose` (Weight-based dosing)
  - `check_drug_interactions` (Severe / Fatal DDI detection)
  - `check_red_flags` (Emergency escalation & safety guardrails)
  - `meld_na_score` (Liver Failure & Transplant Listing Priority)
  - `sofa_score` (Sepsis-3 ICU Sequential Organ Failure Assessment)
  - `burch_wartofsky_thyroid_storm` (Endocrine Emergency BWPS Evaluation)
  - `perc_rule_pe` (Pulmonary Embolism Safe Radiation-Free Exclusion)
  - `scrub_phi` (HIPAA 18, Egyptian NID, Saudi Iqama anonymization)
  - `normalize_terminology` (Trade-to-INN and dialect mapping)

## Dataset Structure

Each JSONL record represents a conversational session with:
- `id`: Unique record identifier (e.g. `medorqis-cardio-ar-001`)
- `language`: `ar`, `en`, or `ar-en`
- `domain`: Medical domain (`cardiology`, `nephrology`, `pharmacology`, `pediatrics`, `emergency`, `hepatology`, `critical_care_sofa`, `endocrinology_emergency`, `pulmonology_emergency`)
- `tools`: Available tool declarations formatted in OpenAI/Qwen JSON Schema
- `messages`: Conversational messages formatted in ChatML (`system`, `user`, `assistant`, `tool`)

## License & Attribution

Licensed under MedOrqis™ Proprietary & Restricted Research License (Copyright © 2026 Eng. Tarek Mohamed. All Rights Reserved. Patent & Copyright Pending). Developed as part of the MedOrqis Medical AI Skills Ecosystem.
