# Netlify + Railway Deployment

## Frontend (Netlify)
1. Build the React app: `npm run build`
2. Drag `dist/` folder to netlify.com
3. Set environment variable in Netlify: `VITE_API_URL=https://your-railway-app.railway.app`

## Backend (Railway)
1. Connect GitHub repo to Railway
2. Set environment variable: `GEMINI_API_KEY=your_key`
3. Railway will automatically deploy your Flask app

## Update API URL in React
Update the fetch URL in App.jsx to use: `${import.meta.env.VITE_API_URL}/analyze`