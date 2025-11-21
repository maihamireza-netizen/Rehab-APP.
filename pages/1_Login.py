import streamlit as st
import base64

st.set_page_config(page_title="Login", layout="wide")

# ------------------------------------------------------------
# 🎨 Set Background Image
# ------------------------------------------------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")    # make sure this file is in your repo root


# ------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------
st.markdown("<h1 style='color:#0F172A; font-weight:700;'>RehabAiQ Access Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top:-10px; font-size:16px;'>Select your access type to continue</p>", unsafe_allow_html=True)

# Center the two buttons using CSS
st.markdown("""
    <style>
        .center-box {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 40px;
        }
        .access-btn {
            background-color: #3DB5D9;
            color: white !important;
            padding: 12px 32px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.25);
            transition: 0.2s ease-in-out;
        }
        .access-btn:hover {
            background-color: #2AA5C5;
            box-shadow: 0 6px 14px rgba(0,0,0,0.35);
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

# --- PERFECT CENTERING USING ABSOLUTE HTML LAYER ---
st.markdown("""
<style>
/* Absolute container centered in the page */
.center-abs {
    position: absolute;
    top: 55%;                     
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: row;
    gap: 40px;
}

/* Button styling */
.center-btn {
    background-color: #4fb7dd;
    color: white !important;
    padding: 14px 32px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    transition: 0.2s ease-in-out;
}

.center-btn:hover {
    background-color: #3aa6c8;
    transform: scale(1.04);
}
</style>
""", unsafe_allow_html=True)

# HTML wrapper
st.markdown("""
<div class="center-abs">
    <form action="/Patient_Selection">
        <button class="center-btn">⚙️ Administrative Access</button>
    </form>

    <form action="/Patient_Selection">
        <button class="center-btn">👩‍⚕️ Clinician Access</button>
    </form>
</div>
""", unsafe_allow_html=True)
