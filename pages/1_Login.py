import streamlit as st
import base64

st.set_page_config(page_title="RehabAiQ Access Portal", layout="wide")

# =========================
# Load Background Image
# =========================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")   # Make sure the filename matches exactly


# =========================
# Centered Layout
# =========================
st.markdown("<br><br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,3,1])

with col2:

    st.markdown(
        """
        <h1 style="text-align:center; color:#0b2e40; font-size:40px;">
        RehabAiQ Access Portal
        </h1>
        <p style="text-align:center; font-size:18px; color:#1b1b1b;">
        Select your access type to continue
        </p>
        """,
        unsafe_allow_html=True
    )

    # --------------------
    # Horizontal Button Row
    # --------------------
    b1, b2 = st.columns([1,1])

    button_style = """
        <style>
        .blue-btn button {
            background-color: #48b6c8 !important;
            color: white !important;
            border-radius: 25px !important;
            padding: 0.6rem 1.2rem !important;
            font-size: 16px !important;
            border: none !important;
        }
        .blue-btn button:hover {
            background-color: #2ca4b6 !important;
            color: white !important;
        }
        </style>
    """

    st.markdown(button_style, unsafe_allow_html=True)

    with b1:
        st.markdown('<div class="blue-btn">', unsafe_allow_html=True)
        admin = st.button("🔧 Administrative Access", key="admin_btn")
        st.markdown("</div>", unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="blue-btn">', unsafe_allow_html=True)
        clinician = st.button("🩺 Clinician Access", key="clin_btn")
        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# Continue → Patient Selection
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
right_col = st.columns([6,1])[1]

with right_col:
    st.markdown('<div class="blue-btn">', unsafe_allow_html=True)
    continue_clicked = st.button("Continue →", key="continue_btn")
    st.markdown("</div>", unsafe_allow_html=True)

if continue_clicked:
    st.switch_page("pages/2_Patient_Selection.py")
