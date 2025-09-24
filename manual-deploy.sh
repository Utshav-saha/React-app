#!/bin/bash

echo "🚀 Building your app for deployment..."

# Build the React app
echo "⚛️ Building React frontend..."
npm run build

echo ""
echo "✅ Build complete!"
echo ""
echo "📋 **MANUAL DEPLOYMENT STEPS:**"
echo ""
echo "🌐 **Deploy to Vercel (Easiest):**"
echo "1. Go to https://vercel.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'Import Project'"
echo "4. Select this GitHub repository (push to GitHub first if needed)"
echo "5. In Environment Variables, add: GEMINI_API_KEY = your_api_key"
echo "6. Deploy!"
echo ""
echo "🔗 **Deploy to Netlify:**"
echo "1. Go to https://netlify.com"
echo "2. Drag the 'dist' folder to the deploy area"
echo "3. Note: You'll need to deploy the backend separately"
echo ""
echo "📁 Your built files are in the 'dist' folder"
echo ""
echo "🔄 **Need to push to GitHub first?**"
echo "   git add ."
echo "   git commit -m 'Ready for deployment'"
echo "   git push origin main"