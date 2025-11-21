import streamlit as st
import base64
from streamlit import switch_page

st.set_page_config(page_title="RehabAiQ Login", layout="wide")

# -----------------------
# Background Image
# -----------------------
def set_bg(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")

# -----------------------
# Title
# -----------------------
st.markdown(
    """
    <div style='margin-top:40px; margin-left:40px;'>
        <h1>RehabAiQ Access Portal</h1>
        <p>Select your access type to continue</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Centered Buttons
# -----------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.write("")  
    admin = st.button("⚙️ Administrative Access", use_container_width=True)
    clinician = st.button("🧑‍⚕️ Clinician Access", use_container_width=True)

# -----------------------
# Navigation
# -----------------------
if admin or clinician:
    switch_page("Patient_Selection")
