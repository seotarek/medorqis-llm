#!/usr/bin/env python3
"""
MedOrqis-LLM — CI/CD Automated Test Suite
Verifies:
1. Deterministic clinical calculators accuracy
2. Pediatric safety ceiling capping
3. Dataset schema integrity (200 records, ChatML structure)
4. Strict zero-emoji policy compliance
"""

import os
import re
import json
import unittest
from benchmarks.run_clinical_benchmark import execute_deterministic_calculator

class TestClinicalCalculators(unittest.TestCase):
    def test_ckd_epi_2021_male(self):
        # 60yo male, SCr 1.2 mg/dL
        res, msg = execute_deterministic_calculator("ckd_epi_2021_egfr", {"age_years": 60, "serum_creatinine_mg_dl": 1.2, "sex": "male"})
        self.assertIsNotNone(res)
        self.assertAlmostEqual(res, 69.8, delta=1.5)

    def test_ckd_epi_2021_female(self):
        # 65yo female, SCr 0.9 mg/dL -> exactly 70.4 mL/min/1.73m2
        res, msg = execute_deterministic_calculator("ckd_epi_2021_egfr", {"age_years": 65, "serum_creatinine_mg_dl": 0.9, "sex": "female"})
        self.assertIsNotNone(res)
        self.assertAlmostEqual(res, 70.4, delta=0.5)

    def test_cha2ds2_va_esc2024(self):
        # 76yo (2 pts) + HTN (1 pt) + Stroke (2 pts) = 5 pts
        res, msg = execute_deterministic_calculator("cha2ds2_va_esc2024", {
            "age_years": 76, "hx_hypertension": True, "hx_stroke_tia_thromboembolism": True
        })
        self.assertEqual(res, 5.0)

    def test_pediatric_dose_capping(self):
        # 50kg child, dose 25 mg/kg = 1250 mg, but adult cap is 1000 mg
        res, msg = execute_deterministic_calculator("calculate_pediatric_weight_dose", {
            "weight_kg": 50, "dose_per_kg": 25, "max_single_adult_dose_mg": 1000
        })
        self.assertEqual(res, 1000.0)

    def test_meld_na_score(self):
        # Bilirubin 3.5, INR 2.1, Creatinine 1.8, Sodium 128
        res, msg = execute_deterministic_calculator("meld_na_score", {
            "serum_bilirubin_mg_dl": 3.5, "inr": 2.1, "serum_creatinine_mg_dl": 1.8, "serum_sodium_meq_l": 128
        })
        self.assertIsNotNone(res)
        self.assertTrue(27 <= res <= 31)

    def test_sofa_score(self):
        # PaO2/FiO2 180 (3), Plt 85 (2), Bili 2.5 (2), Pressor (2/3), GCS 11 (2), Cr 2.2 (2)
        res, msg = execute_deterministic_calculator("sofa_score", {
            "pao2_fio2_ratio": 180, "platelets_k_ul": 85, "bilirubin_mg_dl": 2.5,
            "low_dose_vasopressor": True, "gcs": 11, "creatinine_mg_dl": 2.2
        })
        self.assertIsNotNone(res)
        self.assertTrue(res >= 10)

    def test_perc_rule_pe(self):
        # 28yo, HR 72, SpO2 99%, all negative
        res, msg = execute_deterministic_calculator("perc_rule_pe", {
            "age_years": 28, "heart_rate": 72, "spo2_percent": 99,
            "previous_dvt_pe": False, "recent_surgery_trauma": False,
            "hemoptysis": False, "exogenous_estrogen": False, "unilateral_leg_swelling": False
        })
        self.assertEqual(res, 0.0)


class TestDatasetIntegrity(unittest.TestCase):
    def test_clinical_dataset_count_and_format(self):
        dataset_path = "training/medorqis_clinical_instructions.jsonl"
        self.assertTrue(os.path.exists(dataset_path), f"Dataset file not found at {dataset_path}")
        
        count = 0
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                self.assertIn("id", record, f"Line {line_num} missing 'id'")
                self.assertIn("messages", record, f"Line {line_num} missing 'messages'")
                self.assertIsInstance(record["messages"], list)
                self.assertTrue(len(record["messages"]) >= 3, f"Line {line_num} has fewer than 3 messages")
                count += 1
        
        self.assertGreaterEqual(count, 200, f"Expected at least 200 records, found {count}")

    def test_zero_emoji_guard(self):
        # Verify no emojis in dataset or key documentation
        files_to_check = [
            "training/medorqis_clinical_instructions.jsonl",
            "benchmarks/BENCHMARK_REPORT.md",
            "README.md"
        ]
        
        emoji_pattern = re.compile(
            r"[\U0001F600-\U0001F64F"  # emoticons
            r"\U0001F300-\U0001F5FF"  # symbols & pictographs
            r"\U0001F680-\U0001F6FF"  # transport & map
            r"\U0001F1E0-\U0001F1FF"  # flags
            r"\U00002702-\U000027B0"  # dingbats
            r"\U0001F900-\U0001F9FF"  # supplemental symbols
            r"\U0001FA00-\U0001FA6F"  # chess/symbols
            r"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended
            r"\U00002600-\U000026FF"  # misc symbols
            r"]+", flags=re.UNICODE
        )
        
        for file_path in files_to_check:
            if not os.path.exists(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    # Exclude known git hashes or technical strings
                    matches = emoji_pattern.findall(line)
                    self.assertEqual(
                        len(matches), 0,
                        f"Found emoji {matches} in {file_path} at line {line_num}: {line.strip()[:60]}"
                    )

if __name__ == "__main__":
    unittest.main()
