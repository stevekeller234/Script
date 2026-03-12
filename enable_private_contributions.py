#!/usr/bin/env python3
"""Enable private contributions on GitHub profile via API."""

import os
import requests
import json

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")  # Set via env or replace

# GitHub API endpoint to update user profile
url = "https://api.github.com/user"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Get current user settings
print("Fetching current profile settings...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    user_data = response.json()
    print(f"Current user: {user_data.get('login')}")
    
    # Note: GitHub API doesn't directly support changing "Include private contributions"
    # This setting must be changed via the web interface
    print("\n⚠️  Note: GitHub API doesn't support changing contribution visibility directly.")
    print("You need to enable it via the web interface:")
    print("\n1. Go to: https://github.com/settings/profile")
    print("2. Scroll to 'Contributions & activity' section")
    print("3. Check: 'Include private contributions on my profile'")
    print("4. Save changes")
    print("\nOr use the direct link to contribution settings:")
    print("https://github.com/settings/profile#profile-settings")
    
else:
    print(f"Error: {response.status_code}")
    print(response.text)
