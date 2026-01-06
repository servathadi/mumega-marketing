#!/bin/bash
# Autonomous Deployment Script
# Deploys Marketing HQ to Render (Agents) and Vercel (Content)

set -e

echo "🚀 Deploying Marketing Guild..."

# 1. Sync to GitHub (Source of Truth)
echo "📦 Syncing to GitHub..."
git add .
git commit -m "deploy: Update artifacts for cloud run" || echo "Nothing to commit"
git push origin master

# 2. Deploy Agents to Render (if RENDER_API_KEY is present)
if [ -n "$RENDER_API_KEY" ]; then
    echo "🧠 Deploying Agents to Render..."
    # This assumes a Render Service ID is set, or uses a CLI tool
    # render deploy --service srv-xxxx
    echo "   (Render deployment triggered via Git Push hook)"
else
    echo "⚠️ RENDER_API_KEY not found. Skipping Render deploy."
fi

# 3. Deploy Content to Vercel (if VERCEL_TOKEN is present)
if [ -n "$VERCEL_TOKEN" ]; then
    echo "🌐 Deploying Content to Vercel..."
    # vercel --prod --token $VERCEL_TOKEN
    echo "   (Vercel deployment triggered via Git Push hook)"
else
    echo "⚠️ VERCEL_TOKEN not found. Skipping Vercel deploy."
fi

echo "✅ Deployment Sequence Complete."
