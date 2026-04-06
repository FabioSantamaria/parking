# Vigo Parking Occupation Monitor

A Streamlit application that displays real-time parking occupation data for Vigo city on an interactive map.

## Features

- **Real-time Data**: Fetches parking data from Vigo city council API every 3 minutes
- **Interactive Map**: Displays parking locations with color-coded occupation levels
- **Detailed Information**: Click on parking pins to see detailed information
- **Summary Statistics**: Overview of total spaces, free spaces, and average occupation
- **Automatic Refresh**: Data automatically refreshes every 3 minutes
- **Manual Refresh**: Button to manually refresh data

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Data Source

Data is fetched from the Vigo City Council Open Data portal:
- API Endpoint: `https://datos.vigo.org/data/trafico/parkings-ocupacion.json`
- Updates every 3 minutes

## Map Features

- **Green Pins**: Parking lots with low occupation (< 30%)
- **Orange Pins**: Parking lots with medium occupation (30-70%)
- **Red Pins**: Parking lots with high occupation (> 70%)
- **Click on pins** to see detailed information including:
  - Parking name
  - Free spaces
  - Total spaces
  - Occupation percentage
  - Last update time

## Technical Details

- Built with Streamlit for the web interface
- Uses Folium for map visualization

## Deployment on Render

### **Simplest Deployment (Recommended)**

**Step 1: Backend API**
1. **Web Service** → Connect GitHub repo
2. **Root Directory**: `backend`
3. **Environment**: Python
4. **Build**: `pip install -r requirements.txt`
5. **Start**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Health Check**: `/api/health`

**Step 2: Frontend**
1. **Static Site** → Connect GitHub repo
2. **Root Directory**: `/` (root)
3. **Build**: `echo 'No build needed'`
4. **Publish**: `.`
5. **Environment**: `REACT_APP_API_URL=https://vigo-parking-api.onrender.com`

### **Why This is Simple**
- ✅ **No Docker** - Just static HTML + Python
- ✅ **No build step** - HTML file is ready to serve
- ✅ **No npm dependencies** - Uses CDN libraries
- ✅ **Fast deployment** - Both services on free tier
- ✅ **Auto-deployment** - Updates on git push

### **Files Needed**
- `backend/render-simple.yaml` - Backend config
- `render-simple.yaml` - Frontend config
- `frontend/index.html` - Ready-to-serve HTML file

### **Access URLs**
- **Backend**: `https://vigo-parking-api.onrender.com`
- **Frontend**: `https://vigo-parking-app.onrender.com`
- **API Docs**: `https://vigo-parking-app.onrender.com/docs`

### **Local Testing**
```bash
# Backend
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (any static server)
cd frontend && python -m http.server 3000
# Or open frontend/index.html directly in browser
```