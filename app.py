import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Vigo Parking Occupation",
    page_icon="🅿️",
    layout="wide"
)

# API endpoint
API_URL = "https://datos.vigo.org/data/trafico/parkings-ocupacion.json"

@st.cache_data(ttl=180)  # Cache for 3 minutes
def fetch_parking_data():
    """Fetch parking data from the API"""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

def create_parking_map(data):
    """Create a Folium map with parking lot markers"""
    if not data:
        return None
    
    # Create a DataFrame for easier manipulation
    df = pd.DataFrame(data)
    
    # Calculate center of all parking lots
    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    
    # Create the map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    # Add markers for each parking lot
    for _, parking in df.iterrows():
        # Determine color based on occupation percentage
        occupation_pct = parking['ocupacion']
        if occupation_pct < 30:
            color = 'green'
        elif occupation_pct < 70:
            color = 'orange'
        else:
            color = 'red'
        
        # Create popup content
        popup_content = f"""
        <div style="font-family: Arial; font-size: 14px;">
            <h4>{parking['nombre']}</h4>
            <p><strong>Free Spaces:</strong> {parking['plazaslibres']}</p>
            <p><strong>Total Spaces:</strong> {parking['totalplazas']}</p>
            <p><strong>Occupation:</strong> {parking['ocupacion']}%</p>
            <p><strong>Last Update:</strong> {parking['fechahora']}</p>
        </div>
        """
        
        # Add marker to map
        folium.Marker(
            location=[parking['lat'], parking['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{parking['nombre']} - {parking['ocupacion']}% occupied",
            icon=folium.Icon(color=color, icon='parking', prefix='fa')
        ).add_to(m)
    
    return m

def main():
    st.title("🅿️ Vigo Parking Occupation Monitor")
    st.markdown("Real-time parking occupation data from Vigo city")
    
    # Add auto-refresh functionality
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    
    # Auto refresh every 3 minutes (180 seconds)
    if (datetime.now() - st.session_state.last_refresh).total_seconds() > 180:
        st.cache_data.clear()
        st.session_state.last_refresh = datetime.now()
        st.rerun()
    
    # Manual refresh button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        st.info(f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch data
    data = fetch_parking_data()
    
    if data:
        # Create DataFrame for summary statistics
        df = pd.DataFrame(data)
        
        # Display summary statistics
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Parking Lots", len(df))
        
        with col2:
            total_spaces = df['totalplazas'].sum()
            st.metric("Total Spaces", f"{total_spaces:,}")
        
        with col3:
            free_spaces = df['plazaslibres'].sum()
            st.metric("Free Spaces", f"{free_spaces:,}")
        
        with col4:
            avg_occupation = df['ocupacion'].mean()
            st.metric("Average Occupation", f"{avg_occupation:.1f}%")
        
        # Create and display the map
        st.subheader("🗺️ Parking Map")
        parking_map = create_parking_map(data)
        
        if parking_map:
            # Display the map
            map_data = st_folium(parking_map, width=None, height=500)
        
        # Display detailed table
        st.subheader("📋 Detailed Information")
        
        # Prepare data for display
        display_df = df[['nombre', 'plazaslibres', 'totalplazas', 'ocupacion', 'fechahora']].copy()
        display_df.columns = ['Parking Name', 'Free Spaces', 'Total Spaces', 'Occupation %', 'Last Update']
        display_df = display_df.sort_values('Occupation %', ascending=False)
        
        # Add occupation status column
        display_df['Status'] = display_df['Occupation %'].apply(
            lambda x: '🟢 Low' if x < 30 else '🟡 Medium' if x < 70 else '🔴 High'
        )
        
        st.dataframe(display_df, width='stretch', hide_index=True)
        
    else:
        st.error("Unable to fetch parking data. Please try again later.")
    
    # Add footer with information
    st.markdown("---")
    st.markdown("Data source: [Vigo City Council Open Data](https://datos.vigo.org/)")
    st.markdown("Updates every 3 minutes automatically")

if __name__ == "__main__":
    main()