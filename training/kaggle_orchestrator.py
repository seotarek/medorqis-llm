#!/usr/bin/env python3
"""
MedOrqis Kaggle Cloud Orchestrator
Enables programmatic execution, monitoring, and synchronization with Kaggle GPU VMs
using native REST API with Bearer token authentication.

Features:
- List user kernels and cloud status
- Check kernel execution status and logs
- Push updated notebook versions for dual-T4 training
- Zero emojis (design-doctrine compliance)
"""

import os
import sys
import json
import argparse
import requests

KAGGLE_API_BASE = "https://www.kaggle.com/api/v1"
DEFAULT_TOKEN_FILE = os.path.expanduser("~/.kaggle/access_token")

def get_kaggle_token():
    token = os.environ.get("KAGGLE_API_TOKEN")
    if token:
        return token.strip()
    if os.path.exists(DEFAULT_TOKEN_FILE):
        with open(DEFAULT_TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def get_headers():
    token = get_kaggle_token()
    if not token:
        print("[ERROR] Kaggle API token not found in KAGGLE_API_TOKEN or ~/.kaggle/access_token")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def list_kernels(username="tarekkhallaf"):
    url = f"{KAGGLE_API_BASE}/kernels/list?user={username}"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code == 200:
        data = resp.json()
        print(f"[KAGGLE] Found {len(data)} kernels for user {username}:")
        for k in data:
            print(f"- Ref: {k.get('ref')} | Title: {k.get('title')} | Last Run: {k.get('lastRunTime')}")
        return data
    else:
        print(f"[ERROR] Failed to list kernels (HTTP {resp.status_code}): {resp.text}")
        return None

def check_kernel_status(username="tarekkhallaf", slug="medorqis-llm"):
    url = f"{KAGGLE_API_BASE}/kernels/status?userName={username}&kernelSlug={slug}"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code == 200:
        data = resp.json()
        print(f"[KAGGLE STATUS] {username}/{slug}: {data.get('status')}")
        return data
    else:
        print(f"[KAGGLE STATUS] {username}/{slug} returned HTTP {resp.status_code}: {resp.text}")
        return None

def fetch_logs(username="tarekkhallaf", slug="medorqis-llm", tail=50):
    url = f"{KAGGLE_API_BASE}/kernels/output?userName={username}&kernelSlug={slug}"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code == 200:
        data = resp.json()
        log = data.get("log", "")
        print(f"[KAGGLE LOGS] {username}/{slug} (length: {len(log)} chars):")
        if not log:
            print("(Log buffer is currently empty — container is booting or initializing)")
            return ""
        lines = log.splitlines()
        for l in lines[-tail:]:
            print(l)
        return log
    else:
        print(f"[ERROR] Failed to fetch logs (HTTP {resp.status_code}): {resp.text}")
        return None

def push_training_and_benchmark(username="tarekkhallaf", slug="medorqis-llm"):
    code = """
import os, sys, subprocess

print("=== Starting MedOrqis-LLM Cloud Run ===")
subprocess.run(["nvidia-smi"])

cmd = "pip install -q transformers peft bitsandbytes datasets accelerate huggingface_hub"
subprocess.run(cmd, shell=True, check=True)

print("=== Downloading latest training & benchmark scripts ===")
subprocess.run(["curl", "-s", "-L", "https://raw.githubusercontent.com/seotarek/medorqis-llm/main/training/train_medorqis_cloud.py", "-o", "train.py"], check=True)
subprocess.run(["curl", "-s", "-L", "https://raw.githubusercontent.com/seotarek/medorqis-llm/main/benchmarks/run_clinical_benchmark.py", "-o", "bench.py"], check=True)

print("=== Executing Train ===")
subprocess.run(["python3", "train.py"], check=True)

print("=== Executing Benchmark ===")
subprocess.run(["python3", "bench.py"], check=True)
print("=== All Cloud Tasks Completed ===")
"""
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [code.strip()]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    body = {
        "slug": f"{username}/{slug}",
        "newTitle": slug,
        "text": json.dumps(notebook),
        "language": "python",
        "kernelType": "notebook",
        "isPrivate": True,
        "enableGpu": True,
        "enableInternet": True
    }

    url = f"{KAGGLE_API_BASE}/kernels/push"
    resp = requests.post(url, headers=get_headers(), json=body)
    if resp.status_code == 200:
        data = resp.json()
        print(f"[KAGGLE PUSH SUCCESS] Version {data.get('versionNumber')} queued: {data.get('url')}")
        return data
    else:
        print(f"[ERROR] Push failed (HTTP {resp.status_code}): {resp.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description="MedOrqis Kaggle Cloud Orchestrator")
    parser.add_argument("command", choices=["list", "status", "logs", "push"], help="Command to execute")
    parser.add_argument("--user", default="tarekkhallaf", help="Kaggle username")
    parser.add_argument("--slug", default="medorqis-llm", help="Kernel slug")
    parser.add_argument("--tail", type=int, default=50, help="Number of log lines to show")
    args = parser.parse_args()

    if args.command == "list":
        list_kernels(args.user)
    elif args.command == "status":
        check_kernel_status(args.user, args.slug)
    elif args.command == "logs":
        fetch_logs(args.user, args.slug, args.tail)
    elif args.command == "push":
        push_training_and_benchmark(args.user, args.slug)

if __name__ == "__main__":
    main()
