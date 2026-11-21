#!/usr/bin/env python3
"""
MedOrqis Open-Core Enterprise Private Infrastructure Provisioner.
Creates and configures strict Private repositories on Hugging Face Hub for:
1. Production / Full MIMIC-IV Trained Model Weights (seotarek/medorqis-llm-enterprise)
2. Protected Clinical Production Datasets (seotarek/medorqis-clinical-production-data)

Enforces PhysioNet Data Use Agreement (DUA) compliance and Commercial IP Protection.
Zero emojis.
"""

import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo

def _load_env_file():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k not in os.environ:
                        os.environ[k] = v

_load_env_file()
HF_TOKEN = os.getenv("HF_TOKEN", "")
if not HF_TOKEN:
    print("[ERROR] HF_TOKEN is not set in environment or .env")
    sys.exit(1)

ENTERPRISE_MODEL_REPO = "seotarek/medorqis-llm-enterprise"
ENTERPRISE_DATASET_REPO = "seotarek/medorqis-clinical-production-data"

ENTERPRISE_MODEL_CARD = """---
license: other
license_name: medorqis-enterprise-commercial
base_model: Applied-Innovation-Center/Karnak-6B-v1.0
language:
- ar
- en
tags:
- medical
- clinical-ai
- enterprise
- mimic-iv-compliant
- private
---

# MedOrqis-LLM Enterprise (Protected Production Weights)

**STATUS: STRICTLY PRIVATE / RESTRICTED ACCESS**

This repository contains the protected production QLoRA adapters and merged clinical checkpoints for **MedOrqis-LLM**, separated from the public research showcase (`seotarek/medorqis-llm`) under the MedOrqis Open-Core governance architecture.

## Governance & Compliance Boundaries

1. **PhysioNet Data Use Agreement (DUA) Protection**:
   Models trained on credentialed full releases of MIMIC-IV, eICU-CRD, or proprietary hospital Electronic Health Records (EHR) are legally restricted from public redistribution and reside exclusively inside this private vault.
2. **Air-Gapped Hospital Deployment**:
   Engineered for 4-bit NF4 quantized local deployment (`7.68 GB VRAM`) inside isolated hospital networks with zero external telemetry.
3. **Pharmaceutical Advisory**:
   Architected by Eng. Tarek Mohamed (Tarek Khallaf) with Pharmaceutical Technology Advisory from Eternal Pharma.
"""

ENTERPRISE_DATASET_CARD = """---
license: other
license_name: physionet-dua-restricted
language:
- ar
- en
tags:
- medical
- mimic-iv
- eicu
- private
---

# MedOrqis Clinical Production Data (Private Vault)

**STATUS: STRICTLY PRIVATE / PROTECTED UNDER DATA USE AGREEMENTS**

Dedicated private storage for full credentialed clinical datasets (Full MIMIC-IV, Full eICU, Regional Trade-to-INN Pharmacopeia Mappings, and Hospital EHR Fine-Tuning Records).
"""

def setup_private_repos():
    api = HfApi(token=HF_TOKEN)
    
    print("=" * 65)
    print("MEDORQIS OPEN-CORE ENTERPRISE PRIVATE VAULT PROVISIONING")
    print("=" * 65)

    # 1. Create Private Enterprise Model Repo
    print(f"[1/2] Provisioning Private Model Repo: {ENTERPRISE_MODEL_REPO}...")
    create_repo(
        repo_id=ENTERPRISE_MODEL_REPO,
        repo_type="model",
        private=True,
        token=HF_TOKEN,
        exist_ok=True
    )
    api.upload_file(
        path_or_fileobj=ENTERPRISE_MODEL_CARD.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=ENTERPRISE_MODEL_REPO,
        repo_type="model",
        token=HF_TOKEN
    )
    print(f"[SUCCESS] Private Model Vault LIVE: https://huggingface.co/{ENTERPRISE_MODEL_REPO}")

    # 2. Create Private Enterprise Dataset Repo
    print(f"[2/2] Provisioning Private Dataset Repo: {ENTERPRISE_DATASET_REPO}...")
    create_repo(
        repo_id=ENTERPRISE_DATASET_REPO,
        repo_type="dataset",
        private=True,
        token=HF_TOKEN,
        exist_ok=True
    )
    api.upload_file(
        path_or_fileobj=ENTERPRISE_DATASET_CARD.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=ENTERPRISE_DATASET_REPO,
        repo_type="dataset",
        token=HF_TOKEN
    )
    print(f"[SUCCESS] Private Dataset Vault LIVE: https://huggingface.co/datasets/{ENTERPRISE_DATASET_REPO}")
    print("=" * 65)

if __name__ == "__main__":
    setup_private_repos()
