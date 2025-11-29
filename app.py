import streamlit as st
import os
from pathlib import Path
from utils import create_sidebar, get_current_page
import importlib.util
from typing import Dict, Any, Tuple
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def set_page_config():
    st.set_page_config(
        page_title="Mars Explorer",
        page_icon="🚀",
        layout="wide"
    )
        
def load_css():
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: green;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #666666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .cta-button {
            background-color: #FF4B4B;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            margin: 0.5rem;
        }
        
        /* Hide the default sidebar nav */
        section[data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Hide any default navigation elements */
        .stApp header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Additional selectors to hide automatic sidebar */
        div[data-testid="collapsedControl"] {
            display: none !important;
        }
        
        button[kind="header"] {
            display: none !important;
        }
        
        .st-emotion-cache-1cypcdb {
            display: none !important;
        }
        
        .st-emotion-cache-r421ms {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

def load_page(page_name):
    if page_name == "home":
        show_home_page()
    else:
        page_map = {
            "chat": "sections/1_AIChatbot.py",
            "facts": "sections/2_MarsInformation.py",
            "nasa": "sections/3_NASAData.py",
            "quiz": "sections/game.py"
        }
        
        if page_name in page_map:
            file_path = page_map[page_name]
            spec = importlib.util.spec_from_file_location("module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'main'):
                module.main()

def show_home_page():
    st.markdown('<h1 class="main-header">Welcome to Humans to Mars! </h1>', unsafe_allow_html=True)
    
    # Display Mars header image
    st.image("mars.gif", use_container_width=True)
    
    st.markdown('<p class="sub-header">Embark on a journey to explore the Red Planet through data, images, and interactive experiences.</p>', unsafe_allow_html=True)
    
    # Mission highlights
    st.markdown("## Latest Updates")
    st.write("Stay informed about the latest discoveries and missions on Mars.")
    
    with st.expander("Recent Mission Highlights"):
        st.write("- Perseverance Rover continues its exploration of Jezero Crater")
        st.write("- Ingenuity helicopter completes successful flights on Mars")
        st.write("- New discoveries about Mars' ancient water systems")
    
    # Get today's NASA APOD (ensure we don't request future dates)
    current_date = datetime.now()
    if current_date.hour < 12:  # If it's before noon, use yesterday's date
        current_date = current_date - timedelta(days=1)
    
    apod_date = current_date.strftime("%Y-%m-%d")
    apod_data = fetch_nasa_apod(apod_date)
    
    if apod_data:
        if "error" in apod_data:
            st.error(f"Error fetching APOD: {apod_data['error']}")
        elif 'url' in apod_data:
            st.subheader("NASA Astronomy Picture of the Day")
            st.image(apod_data['url'], caption=apod_data.get('title', ''), use_container_width=True)
            if 'explanation' in apod_data:
                with st.expander("Learn more about this image"):
                    st.write(apod_data['explanation'])

def fetch_nasa_apod(date: str = None) -> Dict[str, Any]:
    """Fetch NASA's Astronomy Picture of the Day"""
    try:
        API_KEY = os.getenv('NASA_API_KEY')
        if not API_KEY:
            return {"error": "NASA API key not found"}
            
        endpoint = "https://api.nasa.gov/planetary/apod"
        params = {
            "api_key": API_KEY,
            "date": date
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Debug information
        #st.write("APOD Response:", data)
        
        return data
    except requests.RequestException as e:
        return {"error": f"Failed to fetch APOD: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def main():
    set_page_config()
    load_css()
    current_page = get_current_page()
    create_sidebar(current_page)
    load_page(current_page)

if __name__ == "__main__":
    main()