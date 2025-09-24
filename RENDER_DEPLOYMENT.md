# Render Deployment

## 1. Frontend (Static Site)
- Connect GitHub repo to Render
- Build command: `npm run build`
- Publish directory: `dist`

## 2. Backend (Web Service)  
- Connect GitHub repo to Render
- Build command: `pip install -r backend/requirements.txt`
- Start command: `python backend/simple_server.py`
- Environment variable: `GEMINI_API_KEY=your_key`

## 3. Update CORS in backend
Add your Render frontend URL to CORS origins in simple_server.py