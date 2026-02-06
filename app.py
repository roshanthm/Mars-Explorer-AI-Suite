import streamlit as st
import os
from utils import create_sidebar, get_current_page
import importlib.util
from typing import Dict, Any
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
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        section[data-testid="stSidebarNav"],
        header[data-testid="stHeader"],
        div[data-testid="collapsedControl"],
        button[kind="header"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

def load_page(page_name):
    if page_name == "home":
        show_home_page()
        return

    page_map = {
        "chat": "sections/1_AIChatbot.py",
        "facts": "sections/2_MarsInformation.py",
        "nasa": "sections/3_NASAData.py",
        "quiz": "sections/game.py"
    }

    if page_name in page_map:
        spec = importlib.util.spec_from_file_location("module", page_map[page_name])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            module.main()

def show_home_page():
    st.markdown(
        '<h1 class="main-header">Welcome to Humans to Mars!</h1>',
        unsafe_allow_html=True
    )

    # ✅ FIXED IMAGE API
    st.image("mars.gif", width="stretch")

    st.markdown(
        '<p class="sub-header">Explore Mars through data, images, and interactive experiences.</p>',
        unsafe_allow_html=True
    )

    st.markdown("## 🚀 Latest Updates")
    with st.expander("Recent Mission Highlights"):
        st.write("- Perseverance exploring Jezero Crater")
        st.write("- Ingenuity helicopter historic flights")
        st.write("- Evidence of ancient water systems")

    # Use yesterday if early morning
    date = datetime.now()
    if date.hour < 12:
        date -= timedelta(days=1)

    apod = fetch_nasa_apod(date.strftime("%Y-%m-%d"))

    if apod and "url" in apod:
        st.subheader("🌌 NASA Astronomy Picture of the Day")
        st.image(apod["url"], caption=apod.get("title", ""), width="stretch")

        with st.expander("About this image"):
            st.write(apod.get("explanation", "No description available."))

def fetch_nasa_apod(date: str) -> Dict[str, Any]:
    try:
        api_key = os.getenv("NASA_API_KEY")
        if not api_key:
            return {"error": "NASA_API_KEY not set"}

        res = requests.get(
            "https://api.nasa.gov/planetary/apod",
            params={"api_key": api_key, "date": date},
            timeout=10
        )
        res.raise_for_status()
        return res.json()

    except Exception as e:
        return {"error": str(e)}

def main():
    set_page_config()
    load_css()
    page = get_current_page()
    create_sidebar(page)
    load_page(page)

if __name__ == "__main__":
    main()
