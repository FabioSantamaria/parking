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
- Implements caching to reduce API calls
- Responsive design that works on desktop and mobile