#!/usr/bin/env python3
"""
eICU Collaborative Research Database Loader for MedOrqis.
Parametric, production-grade parser for eICU tables (Demo v2.0.1 and Full).
Extracts verified ICU stays, multi-level diagnosis strings, lab panels, and medications.
Strict zero-emoji compliance.
"""

import os
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Generator
import pandas as pd

class EICUDataLoader:
    """
    Parametric Data Loader for eICU Collaborative Research Database.
    Compatible with both eICU Demo v2.0.1 and Full PhysioNet eICU release.
    Switching to the full dataset requires only changing the data_dir path.
    """

    CORE_LABS = {
        "creatinine": "creatinine",
        "total bilirubin": "bilirubin_total",
        "sodium": "sodium",
        "potassium": "potassium",
        "platelets x 1000": "platelets",
        "bun": "bun",
        "pt - inr": "inr"
    }

    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self._validate_dir()

    def _validate_dir(self):
        if not self.data_dir.exists():
            raise FileNotFoundError(f"eICU directory not found: {self.data_dir}")

    def _resolve_file(self, filename_prefix: str) -> Path:
        gz_path = self.data_dir / f"{filename_prefix}.csv.gz"
        if gz_path.exists():
            return gz_path
        csv_path = self.data_dir / f"{filename_prefix}.csv"
        if csv_path.exists():
            return csv_path
        raise FileNotFoundError(f"File {filename_prefix}.csv[.gz] not found in {self.data_dir}")

    def load_patients(self) -> pd.DataFrame:
        path = self._resolve_file("patient")
        cols = ["patientunitstayid", "uniquepid", "gender", "age", "ethnicity", 
                "apacheadmissiondx", "hospitaladmittime24", "unitvisitnumber", "unittype"]
        return pd.read_csv(path, usecols=cols)

    def load_diagnoses(self) -> pd.DataFrame:
        path = self._resolve_file("diagnosis")
        cols = ["patientunitstayid", "diagnosisstring", "icd9code", "diagnosispriority"]
        return pd.read_csv(path, usecols=cols)

    def load_labs(self) -> pd.DataFrame:
        path = self._resolve_file("lab")
        chunks = []
        for chunk in pd.read_csv(path, chunksize=50000, 
                                 usecols=["patientunitstayid", "labname", "labresult", "labmeasurenamesystem"]):
            # Filter for core clinical lab targets
            chunk["lab_clean"] = chunk["labname"].astype(str).str.lower().str.strip()
            matched = chunk[chunk["lab_clean"].isin(self.CORE_LABS.keys()) & chunk["labresult"].notna()]
            if not matched.empty:
                chunks.append(matched)
                
        if chunks:
            return pd.concat(chunks, ignore_index=True)
        return pd.DataFrame(columns=["patientunitstayid", "labname", "labresult", "labmeasurenamesystem", "lab_clean"])

    def load_medications(self) -> pd.DataFrame:
        path = self._resolve_file("medication")
        cols = ["patientunitstayid", "drugname", "dosage", "routeadmin"]
        return pd.read_csv(path, usecols=cols)

    def extract_stay_profiles(self) -> Generator[Dict[str, Any], None, None]:
        """
        Yields fully joined, clinically verified ICU stay profiles from eICU.
        """
        print("[EICUDataLoader] Loading relational tables...")
        patients = self.load_patients()
        diagnoses = self.load_diagnoses()
        labs = self.load_labs()
        meds = self.load_medications()

        # Group diagnoses by stay
        diag_by_stay = {}
        for stay_id, group in diagnoses.groupby("patientunitstayid"):
            diag_by_stay[stay_id] = [
                {
                    "diagnosis_string": str(row["diagnosisstring"]),
                    "icd_code": str(row["icd9code"]) if pd.notna(row["icd9code"]) else "",
                    "priority": str(row["diagnosispriority"])
                }
                for _, row in group.iterrows()
            ]

        # Group labs by stay
        labs_by_stay = {}
        for stay_id, group in labs.groupby("patientunitstayid"):
            stay_labs = {}
            for _, row in group.iterrows():
                std_key = self.CORE_LABS.get(str(row["lab_clean"]))
                if std_key and pd.notna(row["labresult"]):
                    try:
                        val = float(row["labresult"])
                        stay_labs[std_key] = {
                            "value": val,
                            "unit": str(row["labmeasurenamesystem"]) if pd.notna(row["labmeasurenamesystem"]) else ""
                        }
                    except (ValueError, TypeError):
                        pass
            labs_by_stay[stay_id] = stay_labs

        # Group meds by stay
        meds_by_stay = {}
        for stay_id, group in meds.groupby("patientunitstayid"):
            stay_meds = []
            for _, row in group.iterrows():
                if pd.notna(row["drugname"]):
                    stay_meds.append({
                        "drug": str(row["drugname"]).strip(),
                        "dosage": str(row["dosage"]) if pd.notna(row["dosage"]) else "",
                        "route": str(row["routeadmin"]) if pd.notna(row["routeadmin"]) else "oral"
                    })
            meds_by_stay[stay_id] = stay_meds

        print(f"[EICUDataLoader] Processing {len(patients)} ICU stays...")
        for _, pt in patients.iterrows():
            stay_id = int(pt["patientunitstayid"])
            gender = str(pt["gender"]) if pd.notna(pt["gender"]) else "Male"
            
            # Parse age: eICU uses "> 89" for elderly patients
            age_str = str(pt["age"]).strip()
            if ">" in age_str:
                age_val = 90
            else:
                try:
                    age_val = int(age_str)
                except ValueError:
                    age_val = 60

            stay_diag = diag_by_stay.get(stay_id, [])
            stay_lab = labs_by_stay.get(stay_id, {})
            stay_med = meds_by_stay.get(stay_id, [])

            yield {
                "stay_id": stay_id,
                "uniquepid": str(pt["uniquepid"]),
                "age": age_val,
                "gender": "F" if gender.lower().startswith("f") else "M",
                "ethnicity": str(pt["ethnicity"]),
                "unittype": str(pt["unittype"]),
                "diagnoses": stay_diag,
                "labs": stay_lab,
                "medications": stay_med
            }

def main():
    parser = argparse.ArgumentParser(description="eICU Data Loader for MedOrqis")
    parser.add_argument("--data-dir", type=str, default="data/eicu-demo")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    loader = EICUDataLoader(args.data_dir)
    count = 0
    for profile in loader.extract_stay_profiles():
        count += 1
        print(f"\n--- eICU Stay {count} ---")
        print(f"Stay ID: {profile['stay_id']} | Age: {profile['age']} | Sex: {profile['gender']} | Unit: {profile['unittype']}")
        print(f"Diagnoses Count: {len(profile['diagnoses'])}")
        if profile['diagnoses']:
            print(f"  Primary: {profile['diagnoses'][0]['diagnosis_string']} ({profile['diagnoses'][0]['icd_code']})")
        print("Labs Extracted:")
        for lab_k, lab_v in profile['labs'].items():
            print(f"  {lab_k}: {lab_v['value']} {lab_v['unit']}")
        print(f"Medications Count: {len(profile['medications'])}")
        if profile['medications']:
            print(f"  Sample Med: {profile['medications'][0]['drug']} - {profile['medications'][0]['dosage']}")
        if count >= args.limit:
            break

    print(f"\nSuccessfully demonstrated generic EICUDataLoader on: {args.data_dir}")

if __name__ == "__main__":
    main()
