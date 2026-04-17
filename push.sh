#!/bin/bash
# Push AITools to remote and trigger deployment
set -e

cd "$(dirname "$0")"

# Build locally to verify
echo "Building..."
npx hexo generate --silent

# Add all changes
git add -A

# Commit with message from args or auto
if [ -n "$1" ]; then
    git commit -m "$1"
else
    git commit -m "update: $(date '+%Y-%m-%d %H:%M')"
fi

# Push
git push origin main

echo "Pushed! EdgeOne Pages will auto-deploy in ~1-2 minutes."
echo "Verify: curl -s -o /dev/null -w '%{http_code}' 'https://aitools.nmdft.cn/'"
