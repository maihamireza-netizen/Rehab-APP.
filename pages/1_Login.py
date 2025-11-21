import streamlit as st
import base64

st.set_page_config(page_title="Login", layout="wide")


# -----------------------------
# Set Background Image
# -----------------------------
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

        /* Center container */
        .center-box {{
            text-align: center;
            margin-top: 80px;
        }}

        /* Sky-blue button style */
        .sky-btn {{
            background-color: #4CB8D9 !important;
            color: white !important;
            padding: 12px 28px !important;
            border-radius: 25px !important;
            border: none !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }}

        .sky-btn:hover {{
            background-color: #3AA8C8 !important;
            color: white !important;
        }}

        /* Continue button */
        .continue-btn {{
            position: absolute;
            right: 60px;
            bottom: 120px;
            background-color: #4CB8D9 !important;
            color: white !important;
            padding: 12px 26px !important;
            border-radius: 25px !important;
            font-size: 15px !important;
            font-weight: 500 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg("LoginBG.png")   # Make sure LoginBG.png is in /pages folder or root repository


# -----------------------------
# Page Layout
# -----------------------------
st.markdown(
    """
    <div style="margin-left: 40px; margin-top: 40px;">
        <h1 style="color:#0F172A; font-weight:700;">RehabAiQ Access Portal</h1>
        <p style="color:#1E293B; font-size:16px; margin-top:-10px;">
            Select your access type to continue
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Centered Buttons
# -----------------------------
st.markdown("<div class='center-box'>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.5, 2, 1.5])

with c2:
    st.markdown(
        """
        <div style="display:flex; justify-content:center; gap:25px;">
            <button class="sky-btn">🔧 Administrative Access</button>
            <button class="sky-btn">🩺 Clinician Access</button>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Continue Button
# -----------------------------
if st.button("Continue ➜", key="cont_btn"):
    st.switch_page("pages/2_Patient_Selection.py")


st.markdown("<div class='continue-btn'></div>", unsafe_allow_html=True)
