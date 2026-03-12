#!/bin/bash

# Script to push code to a new GitHub repository
# IMPORTANT: Do NOT use your exposed token. Create a new one first!

set -e

echo "=========================================="
echo "GitHub Repository Push Helper"
echo "=========================================="
echo ""
echo "⚠️  SECURITY WARNING:"
echo "Your previous token was exposed. DO NOT use it."
echo "Create a new token at: https://github.com/settings/tokens"
echo ""

# Get repository name
read -p "Enter your GitHub username: " GITHUB_USER
read -p "Enter repository name (will be created if it doesn't exist): " REPO_NAME
read -p "Enter your NEW GitHub token (ghp_...): " GITHUB_TOKEN

if [ -z "$GITHUB_USER" ] || [ -z "$REPO_NAME" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: All fields are required."
    exit 1
fi

# Check if token starts with ghp_ (classic token)
if [[ ! "$GITHUB_TOKEN" =~ ^ghp_ ]]; then
    echo "Warning: Token should start with 'ghp_' for classic tokens"
    read -p "Continue anyway? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        exit 1
    fi
fi

# Set branch to main
git branch -M main

# Add remote (remove if exists)
git remote remove origin 2>/dev/null || true
git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Create repo via API if it doesn't exist
echo ""
echo "Checking if repository exists..."
REPO_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}")

if [ "$REPO_EXISTS" = "404" ]; then
    echo "Repository doesn't exist. Creating it..."
    curl -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/user/repos" \
        -d "{\"name\":\"${REPO_NAME}\",\"private\":false}" > /dev/null
    echo "Repository created!"
elif [ "$REPO_EXISTS" = "200" ]; then
    echo "Repository already exists."
else
    echo "Error checking repository. HTTP code: $REPO_EXISTS"
    exit 1
fi

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo ""
echo "⚠️  Remember to revoke your old exposed token!"
