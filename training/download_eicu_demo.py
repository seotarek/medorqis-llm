#!/usr/bin/env python3
"""
eICU Collaborative Research Database Demo (v2.0.1) Downloader for MedOrqis.
Downloads official PhysioNet eICU 2.0.1 demo clinical tables from verified mirror.
Strict zero-emoji compliance.
"""

import os
import shutil
from pathlib import Path
from huggingface_hub import hf_hub_download

REPO_ID = "rafiaa/eicu_demo"
PREFIX = "physionet.org/files/eicu-crd-demo/2.0.1/"

TARGET_FILES = [
    "patient.csv.gz",
    "diagnosis.csv.gz",
    "admissionDx.csv.gz",
    "lab.csv.gz",
    "medication.csv.gz",
    "treatment.csv.gz",
    "pastHistory.csv.gz",
    "vitalAperiodic.csv.gz"
]

def download_eicu_demo(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading eICU Demo (v2.0.1) tables to: {output_dir}")
    
    for rel_path in TARGET_FILES:
        repo_filename = PREFIX + rel_path
        dest_path = output_dir / rel_path
        
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

    print("eICU Demo download complete.")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent / "data" / "eicu-demo"
    download_eicu_demo(base_dir)
