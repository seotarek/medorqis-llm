#!/usr/bin/env python3
"""
MIMIC-IV Clinical Database Demo (v2.2) Downloader for MedOrqis.
Downloads official PhysioNet MIMIC-IV 2.2 demo clinical tables from verified mirror.
Strictly adheres to zero emojis and deterministic medical data standards.
"""

import os
import shutil
from pathlib import Path
from huggingface_hub import hf_hub_download

REPO_ID = "rafiaa/mimiciv_demo"
PREFIX = "physionet.org/files/mimic-iv-demo/2.2/"

TARGET_FILES = [
    # Hospital module
    "hosp/patients.csv.gz",
    "hosp/admissions.csv.gz",
    "hosp/diagnoses_icd.csv.gz",
    "hosp/d_icd_diagnoses.csv.gz",
    "hosp/labevents.csv.gz",
    "hosp/d_labitems.csv.gz",
    "hosp/prescriptions.csv.gz",
    "hosp/transfers.csv.gz",
    # ICU module
    "icu/icustays.csv.gz",
    "icu/chartevents.csv.gz",
    "icu/d_items.csv.gz",
]

def download_mimic_demo(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading MIMIC-IV Demo (v2.2) tables to: {output_dir}")
    
    for rel_path in TARGET_FILES:
        repo_filename = PREFIX + rel_path
        dest_path = output_dir / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        if dest_path.exists() and dest_path.stat().st_size > 0:
            print(f"Already downloaded: {rel_path} ({dest_path.stat().st_size} bytes)")
            continue
            
        print(f"Downloading: {rel_path}...")
        downloaded = hf_hub_download(
            repo_id=REPO_ID,
            filename=repo_filename,
            repo_type="dataset"
        )
        shutil.copy2(downloaded, dest_path)
        print(f"Saved: {dest_path} ({dest_path.stat().st_size} bytes)")

    print("MIMIC-IV Demo download complete.")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent / "data" / "mimic-iv-demo"
    download_mimic_demo(base_dir)
