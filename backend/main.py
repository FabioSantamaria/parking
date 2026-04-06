from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Vigo Parking API",
    description="API for real-time Vigo parking occupation data",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoint
API_URL = "https://datos.vigo.org/data/trafico/parkings-ocupacion.json"

# Cache for parking data
parking_cache = {
    "data": None,
    "last_updated": None,
    "cache_duration": 180  # 3 minutes
}

class ParkingData(BaseModel):
    nombre: str
    plazaslibres: int
    totalplazas: int
    ocupacion: float
    lat: float
    lon: float
    fechahora: str

class ParkingSummary(BaseModel):
    total_parking_lots: int
    total_spaces: int
    free_spaces: int
    avg_occupation: float
    last_updated: str

async def fetch_parking_data() -> Optional[List[Dict]]:
    """Fetch parking data from the API"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def is_cache_valid() -> bool:
    """Check if cache is still valid"""
    if parking_cache["last_updated"] is None:
        return False
    
    cache_age = (datetime.now() - parking_cache["last_updated"]).total_seconds()
    return cache_age < parking_cache["cache_duration"]

async def get_parking_data() -> Optional[List[Dict]]:
    """Get parking data from cache or fetch fresh data"""
    if is_cache_valid() and parking_cache["data"]:
        return parking_cache["data"]
    
    data = await fetch_parking_data()
    if data:
        parking_cache["data"] = data
        parking_cache["last_updated"] = datetime.now()
        return data
    
    return None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Vigo Parking API", "version": "1.0.0"}

@app.get("/api/parking", response_model=List[ParkingData])
async def get_parking():
    """Get all parking data"""
    data = await get_parking_data()
    if not data:
        raise HTTPException(status_code=503, detail="Unable to fetch parking data")
    
    return data

@app.get("/api/parking/summary", response_model=ParkingSummary)
async def get_parking_summary():
    """Get parking summary statistics"""
    data = await get_parking_data()
    if not data:
        raise HTTPException(status_code=503, detail="Unable to fetch parking data")
    
    df = pd.DataFrame(data)
    
    summary = ParkingSummary(
        total_parking_lots=len(df),
        total_spaces=int(df['totalplazas'].sum()),
        free_spaces=int(df['plazaslibres'].sum()),
        avg_occupation=float(df['ocupacion'].mean()),
        last_updated=datetime.now().isoformat()
    )
    
    return summary

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    data = await get_parking_data()
    return {
        "status": "healthy" if data else "unhealthy",
        "last_updated": parking_cache["last_updated"].isoformat() if parking_cache["last_updated"] else None,
        "cache_valid": is_cache_valid()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
