import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

def create_sidebar(current_page):
    with st.sidebar:
        st.title("Navigation")
        
        if st.button("Home", key=f"{current_page}_home", use_container_width=True):
            st.query_params["page"] = "home"
            st.rerun()
            
        if st.button("Chat with AI Expert", key=f"{current_page}_chat", use_container_width=True):
            st.query_params["page"] = "chat"
            st.rerun()
            
        if st.button("Explore Mars Facts", key=f"{current_page}_facts", use_container_width=True):
            st.query_params["page"] = "facts"
            st.rerun()
            
        if st.button("View NASA Data", key=f"{current_page}_nasa", use_container_width=True):
            st.query_params["page"] = "nasa"
            st.rerun()
            
        if st.button("Space Quiz", key=f"{current_page}_quiz", use_container_width=True):
            st.query_params["page"] = "quiz"
            st.rerun()

def get_current_page():
    return st.query_params.get("page", "home")