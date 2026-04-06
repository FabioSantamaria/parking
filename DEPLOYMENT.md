# Fresh Render Deployment Guide

## Step 1: Deploy Backend API
1. Go to Render Dashboard
2. Click "New Web Service"
3. Connect GitHub repository
4. Use `backend/render-clean.yaml`:
   - Root Directory: `backend`
   - Runtime: Python
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Health Check: `/api/health`

## Step 2: Deploy Frontend
1. Click "New Static Site"
2. Connect same repository
3. Use `render-clean.yaml`:
   - Root Directory: `/`
   - Build: `echo 'No build needed'`
   - Publish: `.`
   - Environment: `REACT_APP_API_URL=https://vigo-parking-app.onrender.com`

## Why This Works
- ✅ No Docker complexity
- ✅ Separate services (no port conflicts)
- ✅ Static site for frontend
- ✅ Python service for backend
- ✅ Rewrite rules for API calls

## URLs After Deployment
- Backend: https://vigo-parking-api.onrender.com
- Frontend: https://vigo-parking-app.onrender.com
- API Docs: https://vigo-parking-api.onrender.com/docs
