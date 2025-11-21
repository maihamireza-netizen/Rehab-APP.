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

# --- PERFECTLY CENTERED BUTTONS ---
st.markdown("""
    <style>
        .center-container {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 30px;
            margin-top: 40px;
        }

        .access-btn {
            background-color: #4fb7dd;
            color: white !important;
            padding: 12px 28px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.15);
            transition: 0.2s ease-in-out;
        }

        .access-btn:hover {
            background-color: #3aa6c8;
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="center-container">', unsafe_allow_html=True)

colA, colB = st.columns([1,1])

with colA:
    admin_click = st.button("⚙️ Administrative Access", key="admin_btn", help="Admin login", use_container_width=False)

with colB:
    clinician_click = st.button("👩‍⚕️ Clinician Access", key="clin_btn", help="Clinician login", use_container_width=False)

st.markdown('</div>', unsafe_allow_html=True)

