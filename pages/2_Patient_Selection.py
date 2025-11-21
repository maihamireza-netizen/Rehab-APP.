import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Patient Selection", layout="wide")

# ----------------------------------------
# 🔹 Background Image (same as Login)
# ----------------------------------------
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

        /* White glass card effect */
        .glass-card {{
            background: rgba(255, 255, 255, 0.75);
            padding: 35px;
            border-radius: 16px;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.3);
            box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        }}

        .title-text {{
            font-size: 36px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
        }}

        .subtitle-text {{
            margin-top: -10px;
            font-size: 16px;
            color: #334155;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")

# ----------------------------------------
# Load Patient Data
# ----------------------------------------
df = pd.read_json("idx_vw_rehab_recruitment_DEV.json")
patient_list = df["patientid"].astype(str).tolist()

# ----------------------------------------
# Main Layout Container
# ----------------------------------------
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>Patient Selection</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Select one or multiple patients to continue.</p>", unsafe_allow_html=True)

st.write("")

# Row layout
col1, col2 = st.columns([4, 1])

with col1:
    selected = st.multiselect(
        "Choose Patients:",
        options=patient_list,
        default=None,
        placeholder="Select one or more patients"
    )

with col2:
    st.markdown("**Quick Actions:**")
    if st.button("Select All"):
        selected = patient_list
    if st.button("Deselect All"):
        selected = []

st.write("")
st.write("")

# Continue button (redirect)
if st.button("Continue ➜"):
    if selected:
        st.session_state["selected_patients"] = selected
        st.switch_page("pages/3_Patient_Profile.py")
    else:
        st.warning("Please select at least one patient.")

st.markdown("</div>", unsafe_allow_html=True)
