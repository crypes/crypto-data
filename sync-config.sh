#!/bin/bash
# Pogo Config Sync Script
# Automatically syncs configuration changes to GitHub

set -e

REPO_DIR="/tmp/pogo"
WORKSPACE_DIR="/root/.openclaw/.openclaw/workspace"
SKILLS_DIR="/usr/local/lib/node_modules/openclaw/skills"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "🔄 Starting Pogo config sync at $TIMESTAMP"

# Ensure we're in the repo directory
cd "$REPO_DIR"

# Pull latest changes first to avoid conflicts
echo "📥 Pulling latest changes..."
git pull origin main || true

# Sync workspace config files
echo "📋 Syncing configuration files..."
cp "$WORKSPACE_DIR/SOUL.md" . 2>/dev/null || echo "  - SOUL.md not found in workspace"
cp "$WORKSPACE_DIR/IDENTITY.md" . 2>/dev/null || echo "  - IDENTITY.md not found in workspace"
cp "$WORKSPACE_DIR/USER.md" . 2>/dev/null || echo "  - USER.md not found in workspace"
cp "$WORKSPACE_DIR/AGENTS.md" . 2>/dev/null || echo "  - AGENTS.md not found in workspace"
cp "$WORKSPACE_DIR/TOOLS.md" . 2>/dev/null || echo "  - TOOLS.md not found in workspace"

# Sync skills
echo "🔧 Syncing skills..."
for skill in healthcheck skill-creator weather; do
    if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
        mkdir -p "skills/$skill"
        cp "$SKILLS_DIR/$skill/SKILL.md" "skills/$skill/"
        echo "  - Synced $skill"
    fi
done

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ No changes to sync"
    exit 0
fi

# Add all changes
echo "📦 Staging changes..."
git add -A

# Show what's being committed
echo "📊 Changes to commit:"
git status --short

# Commit with timestamp
echo "💾 Committing..."
git commit -m "Auto-sync: Configuration update at $TIMESTAMP"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo "✨ Sync complete! Changes pushed to https://github.com/crypes/pogo"
