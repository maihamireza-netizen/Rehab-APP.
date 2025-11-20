import streamlit as st
import pandas as pd
import json

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="RehabAiQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- GLOBAL CSS --------------------
st.markdown(
    """
    <style>
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .header-title {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: #1A3C7C;
            padding-top: 10px;
        }

        .subheader {
            font-size: 18px !important;
            color: #5A5A5A;
            padding-bottom: 20px;
        }

        .card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- SIDEBAR LOGO --------------------
st.sidebar.image("Logo.png", use_container_width=True)
st.sidebar.markdown("---")

st.sidebar.write("Use the navigation menu to choose a page.")

# Main file intentionally left minimal
st.title("RehabAiQ Platform")

st.write(
    """
    Welcome!  
    Use the navigation sidebar to choose a page.
    """
)
