#!/bin/bash

echo "🚀 Preparing for deployment..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Using npx to run Vercel (no global installation needed)..."
    VERCEL_CMD="npx vercel"
else
    VERCEL_CMD="vercel"
fi

echo "🔧 Building the project..."
npm run build

echo "🌐 Deploying to Vercel..."
echo ""
echo "📋 During deployment, you'll need to:"
echo "1. Set environment variable: GEMINI_API_KEY = your_api_key"
echo "2. Choose 'Build and Output Settings' if prompted"
echo ""
echo "🚀 Starting deployment..."
$VERCEL_CMD --prod

echo "✅ Deployment complete!"
echo "📝 Don't forget to add your GEMINI_API_KEY in Vercel dashboard:"
echo "   https://vercel.com/dashboard -> Your Project -> Settings -> Environment Variables"