"""
Initialization utilities for Streamlit pages.
Handles common setup tasks like API key validation and styling.
"""

import streamlit as st
from utils.config import check_api_configuration


def initialize_page(page_name: str, emoji: str = "📄"):
    """
    Initialize a Streamlit page with common setup.
    
    Parameters
    ----------
    page_name : str
        Name of the page (e.g., "Prevention Tips")
    emoji : str
        Emoji for the page (e.g., "🌱")
    """
    # Check API configuration
    if not check_api_configuration():
        st.stop()
    
    # Apply global styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    p, span, label { font-size: 1.1rem !important; line-height: 1.6; }
    h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
    h2, h3 { font-size: 1.3rem !important; font-weight: 700 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)


def show_feature_not_available():
    """Show message when feature requires API key."""
    st.error("❌ This feature requires a valid Gemini API key.")
    st.info("""
    **Configuration Required:**
    
    1. Go to ⚙️ Settings page
    2. Follow the setup instructions
    3. Return here and refresh
    
    Or visit: https://aistudio.google.com/app/apikey
    """)


def show_loading_message(message: str = "Processing..."):
    """Show custom loading message."""
    with st.spinner(f"⏳ {message}"):
        st.empty()
