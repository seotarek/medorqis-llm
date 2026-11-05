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

def main():
    parser = argparse.ArgumentParser(description="MedOrqis Kaggle Cloud Orchestrator")
    parser.add_argument("command", choices=["list", "status"], help="Command to execute")
    parser.add_argument("--user", default="tarekkhallaf", help="Kaggle username")
    parser.add_argument("--slug", default="medorqis-llm", help="Kernel slug")
    args = parser.parse_args()

    if args.command == "list":
        list_kernels(args.user)
    elif args.command == "status":
        check_kernel_status(args.user, args.slug)

if __name__ == "__main__":
    main()
