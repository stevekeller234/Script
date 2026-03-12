#!/usr/bin/env python3
"""Make GitHub repository private via API."""

import os
import requests
import json

GITHUB_USER = "Dev-Ameen01"
REPO_NAME = "git-commit-generator"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")  # Set via env or replace

url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

data = {
    "private": True
}

print(f"Making repository {REPO_NAME} private...")
response = requests.patch(url, headers=headers, json=data)

if response.status_code == 200:
    repo_data = response.json()
    print(f"✅ Repository is now private!")
    print(f"Repository URL: {repo_data['html_url']}")
    print(f"Private: {repo_data['private']}")
    print("\n📊 Note: Commits in private repositories still count toward your contribution graph!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
