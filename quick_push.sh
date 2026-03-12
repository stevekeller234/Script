#!/bin/bash

# Quick push script - creates repo and pushes code
# ⚠️ WARNING: Using provided token. Revoke it after use and create a new one!

set -e

GITHUB_USER="${1:-Dev-Ameen01}"  # Default username, can override
REPO_NAME="${2:-Script}"  # Default repo name, can override
GITHUB_TOKEN="${GITHUB_TOKEN:-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}"

echo "=========================================="
echo "Pushing to GitHub"
echo "=========================================="
echo "Username: $GITHUB_USER"
echo "Repo: $REPO_NAME"
echo ""
echo "⚠️  WARNING: Using exposed token!"
echo "Revoke this token after pushing and create a new one."
echo ""

# Set branch to main
cd /Users/dev/Desktop/Script
git branch -M main 2>/dev/null || git branch -M main

# Remove existing remote if any
git remote remove origin 2>/dev/null || true

# Add remote with token
git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Create repo via API if it doesn't exist
echo "Creating repository (if it doesn't exist)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}")

if [ "$HTTP_CODE" = "404" ]; then
    echo "Repository doesn't exist. Creating it..."
    curl -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/user/repos" \
        -d "{\"name\":\"${REPO_NAME}\",\"private\":false,\"description\":\"Git commit history generator script\"}" > /dev/null
    echo "✅ Repository created!"
elif [ "$HTTP_CODE" = "200" ]; then
    echo "Repository already exists."
else
    echo "Error: HTTP code $HTTP_CODE"
    exit 1
fi

# Push to GitHub
echo ""
echo "Pushing code to GitHub..."
git push -u origin main --force

echo ""
echo "✅ Successfully pushed!"
echo "Repository: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo ""
echo "⚠️  IMPORTANT: Revoke your token after use and create a new one!"
echo "   Go to: https://github.com/settings/tokens"
