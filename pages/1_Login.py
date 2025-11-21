import streamlit as st
import base64

# Page config
st.set_page_config(page_title="RehabAiQ Access Portal", layout="wide")

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding-top: 0rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

# -------------------------------------
# Load Background Image
# -------------------------------------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("pages/background.jpg")   # <-- update name if needed


# -------------------------------------
# Centered Layout Container
# -------------------------------------
centered = """
<style>
.login-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -45%);
    text-align: center;
}
.login-title {
    font-size: 52px;
    font-weight: 700;
    color: #003B4A;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.25);
}
.login-subtitle {
    font-size: 20px;
    color: #003B4A;
    margin-top: -10px;
    margin-bottom: 40px;
}
.access-btn {{
    display: inline-block;
    padding: 16px 40px;
    border-radius: 40px;
    font-size: 20px;
    font-weight: 600;
    margin: 10px 15px;
    border: 2px solid #008C99;
    cursor: pointer;
    transition: 0.25s;
}}
.admin {{
    background-color: #008C99;
    color: white;
}}
.admin:hover {{
    background-color: #006F7A;
}}
.clin {{
    background-color: rgba(255,255,255,0.8);
    color: #006F7A;
}}
.clin:hover {{
    background-color: rgba(255,255,255,1);
}}
.continue-btn {{
    position: absolute;
    right: 40px;
    bottom: 40px;
    padding: 12px 28px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 10px;
    background-color: #008C99;
    color: white;
    border: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.25);
    cursor: pointer;
    transition: 0.3s;
}}
.continue-btn:hover {{
    background-color: #006F7A;
}}
</style>
"""

st.markdown(centered, unsafe_allow_html=True)


# -------------------------------------
# HTML UI
# -------------------------------------
st.markdown("""
<div class="login-container">

    <div class="login-title">RehabAiQ Access Portal</div>
    <div class="login-subtitle">Select your access type to continue</div>

    <a href="/?page=2" class="access-btn admin">Administrative Access</a>
    <a href="/?page=3" class="access-btn clin">Clinician Access</a>

</div>

<a href="/?page=2">
    <button class="continue-btn">Continue →</button>
</a>

""", unsafe_allow_html=True)
