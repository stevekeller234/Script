#!/bin/bash

# Make repository private via GitHub API
# Run this script manually if the Python version has SSL issues

GITHUB_USER="Dev-Ameen01"
REPO_NAME="Script"
GITHUB_TOKEN="${GITHUB_TOKEN:-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}"

echo "Making repository private..."

curl -X PATCH \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}" \
  -d '{"private":true}'

echo ""
echo "✅ Repository should now be private!"
echo "📊 Note: Commits in private repos still count toward your contribution graph!"
