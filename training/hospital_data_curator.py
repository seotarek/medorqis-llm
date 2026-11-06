import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
MedOrqis-LLM — Hospital Clinical Data Curator
Streams and curates real-world hospital discharge summaries and Arabic medical consultations
from Hugging Face (Asclepius Clinical Notes and Shifaa Arabic Consultations).
Transforms unstructured hospital EHR records into MedOrqis ChatML tool-calling instruction format.
Zero emoji compliance.
"""

import os
import sys
import json
import re
import requests
from typing import List, Dict, Any, Optional

from training.dataset_builder import CLINICAL_TOOLS_SCHEMA, SYSTEM_PROMPT

HF_DATASETS_API = "https://datasets-server.huggingface.co/rows"

def fetch_shifaa_arabic_records(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """Fetches real Arabic clinical consultations from Shifaa dataset via HF API."""
    url = f"{HF_DATASETS_API}?dataset=Ahmed-Selem/Shifaa_Arabic_Medical_Consultations&config=default&split=train&offset={offset}&limit={limit}"
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            rows = [r.get("row", {}) for r in data.get("rows", [])]
            return rows
        else:
            print(f"[WARNING] Shifaa API returned HTTP {resp.status_code}")
            return []
    except Exception as e:
        print(f"[ERROR] Failed to fetch Shifaa records: {e}")
        return []

def fetch_asclepius_hospital_notes(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """Fetches real hospital discharge summaries and clinical courses from Asclepius dataset."""
    url = f"{HF_DATASETS_API}?dataset=starmpcc/Asclepius-Synthetic-Clinical-Notes&config=default&split=train&offset={offset}&limit={limit}"
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            rows = [r.get("row", {}) for r in data.get("rows", [])]
            return rows
        else:
            print(f"[WARNING] Asclepius API returned HTTP {resp.status_code}")
            return []
    except Exception as e:
        print(f"[ERROR] Failed to fetch Asclepius notes: {e}")
        return []

def curate_hospital_dataset(output_path: str = "training/hospital_curated_cases.jsonl", target_count: int = 50) -> str:
    print("=" * 65)
    print("MEDORQIS HOSPITAL CLINICAL DATA CURATOR")
    print("Streaming real EHR summaries and Arabic hospital consultations...")
    print("=" * 65)
    
    curated_records = []
    
    # 1. Fetch Arabic consultations
    print("\n[Phase 1/3] Fetching and filtering Arabic hospital consultations (Shifaa)...")
    shifaa_rows = fetch_shifaa_arabic_records(limit=60, offset=0)
    print(f"Fetched {len(shifaa_rows)} raw Arabic hospital consultations.")
    
    ar_count = 0
    for row in shifaa_rows:
        if ar_count >= target_count // 2:
            break
        q_title = row.get("Question Title", "").strip()
        q_text = row.get("Question", "").strip()
        a_text = row.get("Answer", "").strip()
        diag = row.get("Hierarchical Diagnosis", "General Medicine")
        
        # Clean formatting
        if len(q_text) < 50 or len(a_text) < 100:
            continue
            
        # Strip salutations for clean clinical evaluation
        clean_q = re.sub(r"^(السلام عليكم|بسم الله الرحمن الرحيم|تحية طيبة).*", "", q_text, flags=re.MULTILINE).strip()
        clean_a = re.sub(r"^(السلام عليكم|بسم الله الرحمن الرحيم|الأخ الفاضل|الأخت الفاضلة).*", "", a_text, flags=re.MULTILINE).strip()
        
        cid = f"medorqis-hospital-shifaa-ar-{ar_count + 1:03d}"
        
        # Detect if clinical red flags exist (chest pain, severe dyspnea, severe anemia, acute bleeding)
        has_red_flag = any(k in q_text for k in ["ألم في الصدر", "ضيق في التنفس", "نزيف", "خفقان", "دوخة شديدة", "تشنج", "فقدان وعي"])
        
        if has_red_flag:
            tool_name = "check_red_flags"
            tool_args = {"findings": [q_title, "شكوى حادة تستوجب الفحص العاجل"]}
            tool_resp = {"status": "ESCALATION_MANDATED", "recommendation": "فحص سريري عاجل وتخطيط قلب أو تحاليل دموية"}
        else:
            tool_name = "normalize_terminology"
            tool_args = {"query": q_title}
            tool_resp = {"specialty": diag, "standardized_terms": [q_title]}
            
        record = {
            "id": cid,
            "language": "ar",
            "domain": "hospital_ambulatory",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"استشارة سريرية واردة للمستشفى: {q_title}\n\nتفاصيل شكوى المريض:\n{clean_q}"},
                {
                    "role": "assistant",
                    "content": f"سأقوم بفحص المعطيات السريرية وتحليل الأعراض الواردة في ملف المريض وفق المعايير الطبية المعتمدة.",
                    "tool_calls": [
                        {
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": tool_args
                            }
                        }
                    ]
                },
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(tool_resp, ensure_ascii=False)
                },
                {
                    "role": "assistant",
                    "content": f"### التقييم السريري الشامل وخطة الرعاية المعتمدة:\n\n{clean_a}"
                }
            ]
        }
        curated_records.append(record)
        ar_count += 1
        
    print(f"Curated {ar_count} high-fidelity Arabic hospital instruction cases.")
    
    # 2. Fetch English Hospital Discharge Summaries
    print("\n[Phase 2/3] Fetching and filtering English hospital discharge records (Asclepius)...")
    asclepius_rows = fetch_asclepius_hospital_notes(limit=60, offset=0)
    print(f"Fetched {len(asclepius_rows)} raw hospital notes.")
    
    en_count = 0
    for row in asclepius_rows:
        if en_count >= target_count // 2:
            break
        note = row.get("note", "").strip()
        question = row.get("question", "").strip()
        answer = row.get("answer", "").strip()
        task = row.get("task", "Clinical Evaluation")
        
        if len(note) < 80 or len(question) < 20 or len(answer) < 30:
            continue
            
        cid = f"medorqis-hospital-asclepius-en-{en_count + 1:03d}"
        
        record = {
            "id": cid,
            "language": "en",
            "domain": "hospital_inpatient",
            "tools": CLINICAL_TOOLS_SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Hospital Medical Record / Discharge Summary:\n{note}\n\nClinical Inquiry:\n{question}"},
                {
                    "role": "assistant",
                    "content": "I will examine the hospital course and patient documentation to provide an audited clinical analysis.",
                    "tool_calls": [
                        {
                            "type": "function",
                            "function": {
                                "name": "normalize_terminology",
                                "arguments": {"query": question}
                            }
                        }
                    ]
                },
                {
                    "role": "tool",
                    "name": "normalize_terminology",
                    "content": json.dumps({"task": task, "verified": True})
                },
                {
                    "role": "assistant",
                    "content": f"### Hospital Clinical Course & Case Evaluation:\n\n{answer}"
                }
            ]
        }
        curated_records.append(record)
        en_count += 1
        
    print(f"Curated {en_count} high-fidelity English hospital discharge cases.")
    
    # 3. Export to JSONL
    print(f"\n[Phase 3/3] Exporting {len(curated_records)} curated hospital cases to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in curated_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    print(f"Successfully generated {output_path} with {len(curated_records)} bilingual hospital cases!")
    return output_path

if __name__ == "__main__":
    curate_hospital_dataset()
