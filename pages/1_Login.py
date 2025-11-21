import streamlit as st
import base64

st.set_page_config(page_title="RehabAiQ Login", layout="wide")

# -------------------------
# Background image
# -------------------------
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

        .access-btn {{
            background-color: #5EC6E8;
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            border: none;
            font-size: 16px;
            cursor: pointer;
            margin: 10px;
        }}
        
        .access-btn:hover {{
            background-color: #4DB5D7;
        }}

        .center-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 40px;
            gap: 30px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")

# -------------------------
# Header
# -------------------------
st.markdown(
    """
    <h1 style='margin-top:40px; margin-left:40px; color:#0A2B42;'>
        RehabAiQ Access Portal
    </h1>
    <p style='margin-left:40px;'>Select your access type to continue</p>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Center Buttons (HTML for perfect centering)
# -------------------------
st.markdown(
    """
    <div class="center-container">
        <button class="access-btn" onclick="window.location.href='?page=Patient_Selection'">⚙️ Administrative Access</button>
        <button class="access-btn" onclick="window.location.href='?page=Patient_Selection'">👩‍⚕️ Clinician Access</button>
    </div>
    """,
    unsafe_allow_html=True
)
