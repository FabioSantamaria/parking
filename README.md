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

### **Option 1: Unified Docker Deployment (Recommended)**

**Single Service Deployment** - Frontend + Backend in one container:

1. **Push to GitHub**:
   ```bash
   git push origin main
   ```

2. **Render Setup**:
   - **Web Service** → Connect GitHub repo
   - **Name**: `vigo-parking-app`
   - **Environment**: Docker
   - **Root Directory**: `/` (root)
   - **Dockerfile Path**: `./Dockerfile`
   - **Health Check**: `/api/health`

### **Option 2: Separate Services**

**Backend + Frontend as separate services**:

1. **Backend (FastAPI)**:
   - Web Service → Connect GitHub repo
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Frontend (React)**:
   - Static Site → Connect GitHub repo  
   - Root Directory: `frontend`
   - Build: `npm install && npm run build`
   - Environment: `REACT_APP_API_URL=https://your-backend-url.onrender.com`

### **Docker Architecture**

**Unified Dockerfile Features**:
- Multi-stage build (Node.js + Python)
- Nginx reverse proxy
- Frontend static files served
- Backend API proxied to `/api/`
- Single deployment endpoint

### **Local Testing**
```bash
# Unified deployment
docker-compose -f docker-compose.prod.yml up --build

# Separate services
docker-compose up --build
```

### **Environment Variables**
- `REACT_APP_API_URL` - Frontend backend URL
- `PYTHONUNBUFFERED` - Backend logging