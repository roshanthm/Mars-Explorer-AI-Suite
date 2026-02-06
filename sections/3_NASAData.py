import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()
def fetch_mars_weather():
    """
    Fetch Mars weather data from NASA's API
    """
    try:
        API_KEY = os.getenv('NASA_API_KEY')
        if not API_KEY:
            st.error("Please set your NASA_API_KEY environment variable")
            return None
            
        url = f"https://api.nasa.gov/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Mars weather data: {str(e)}")
        return None

def fetch_rover_photos(rover="curiosity", earth_date=None):
    """
    Fetch Mars Rover photos from NASA's API
    """
    try:
        API_KEY = os.getenv('NASA_API_KEY')
        if not API_KEY:
            st.error("Please set your NASA_API_KEY environment variable")
            return None
            
        earth_date = earth_date or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
        params = {
            "earth_date": earth_date,
            "api_key": API_KEY,
            "page": 1,
            "per_page": 12  # Limit to 12 photos for better performance
        }
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching rover photos: {str(e)}")
        return None

def create_weather_visualization(weather_data):
    """
    Create interactive weather visualizations using Plotly
    """
    # Create sample weather data for visualization (replace with actual API data)
    dates = pd.date_range(start='2024-02-01', periods=7)
    temperatures = [-60, -55, -63, -58, -61, -57, -59]
    pressure_values = [685, 682, 688, 684, 687, 683, 686]
    wind_speed = [15, 18, 12, 20, 16, 14, 17]
    
    # Temperature chart
    temp_df = pd.DataFrame({
        'Date': dates,
        'Temperature (°C)': temperatures
    })
    fig_temp = px.line(temp_df, x='Date', y='Temperature (°C)', 
                      title='Mars Temperature Variation')
    fig_temp.update_traces(line_color='#FF4B4B')
    
    # Pressure chart
    pressure_df = pd.DataFrame({
        'Date': dates,
        'Pressure (Pa)': pressure_values
    })
    fig_pressure = px.line(pressure_df, x='Date', y='Pressure (Pa)', 
                          title='Atmospheric Pressure Variation')
    fig_pressure.update_traces(line_color='#1f77b4')
    
    # Wind speed chart
    wind_df = pd.DataFrame({
        'Date': dates,
        'Wind Speed (m/s)': wind_speed
    })
    fig_wind = px.line(wind_df, x='Date', y='Wind Speed (m/s)', 
                       title='Wind Speed Variation')
    fig_wind.update_traces(line_color='#2ca02c')
    
    return fig_temp, fig_pressure, fig_wind

def display_weather_data(weather_data):
    st.subheader("Current Mars Weather")
    
    # Create and display weather visualizations
    fig_temp, fig_pressure, fig_wind = create_weather_visualization(weather_data)
    
    # Display charts in tabs
    tab1, tab2, tab3 = st.tabs(["Temperature", "Pressure", "Wind Speed"])
    
    with tab1:
        st.plotly_chart(fig_temp, use_container_width=True)
    with tab2:
        st.plotly_chart(fig_pressure, use_container_width=True)
    with tab3:
        st.plotly_chart(fig_wind, use_container_width=True)
        
    # Add weather summary
    with st.expander("Weather Summary"):
        st.write("""
        Note: This data is simulated for demonstration purposes. 
        In a production environment, it would be replaced with real-time data from NASA's API.
        
        The weather patterns on Mars are influenced by:
        - The planet's thin atmosphere
        - Seasonal changes
        - Dust storms
        - Daily temperature variations
        """)

def display_rover_photos(photos_data):
    st.subheader("Latest Mars Rover Photos")
    
    # Filter controls
    col1, col2 = st.columns(2)
    
    with col1:
        rovers = ["Curiosity", "Perseverance", "Opportunity"]
        selected_rover = st.selectbox("Select Rover", rovers)
    
    with col2:
        selected_date = st.date_input(
            "Select Date",
            datetime.now() - timedelta(days=7)
        )
    
    # Fetch photos based on selected filters
    with st.spinner("Fetching photos..."):
        photos = fetch_rover_photos(selected_rover.lower(), selected_date.strftime("%Y-%m-%d"))
        
        if photos and 'photos' in photos and len(photos['photos']) > 0:
            # Create a grid of photos
            cols = st.columns(3)
            for idx, photo in enumerate(photos['photos']):
                with cols[idx % 3]:
                    st.image(
                        photo['img_src'],
                        caption=f"Taken by {photo['rover']['name']} on {photo['earth_date']}",
                        use_container_width=True
                    )
                    with st.expander("Photo Details"):
                        st.write(f"Camera: {photo['camera']['full_name']}")
                        st.write(f"Sol: {photo['sol']}")
                        st.write(f"Mission Status: {photo['rover']['status'].title()}")
        else:
            st.info("No photos available for the selected criteria. Try a different date or rover.")

def main():
    st.title("NASA Mars Data Dashboard")
    
    # Check for NASA API key
    if not os.getenv('NASA_API_KEY'):
        st.error("""
        Please set your NASA_API_KEY environment variable.
        You can get an API key from: https://api.nasa.gov/
        """)
        st.stop()
    
    # Create tabs for different data sections
    tab1, tab2 = st.tabs(["Weather Data", "Rover Photos"])
    
    with tab1:
        with st.spinner("Fetching Mars weather data..."):
            weather_data = fetch_mars_weather()
            display_weather_data(weather_data)
    
    with tab2:
        with st.spinner("Fetching rover photos..."):
            photos_data = fetch_rover_photos()
            display_rover_photos(photos_data)
    
    # Add data source information
    st.markdown("---")
    st.markdown("""
    **Data Sources:**
    - Weather data provided by NASA's InSight Mars Weather Service
    - Photos provided by NASA's Mars Rover Photos API
    
    *Note: Some features may be using simulated data when API limits are reached or during testing.*
    """)

if __name__ == "__main__":
    main()