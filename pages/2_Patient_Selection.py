import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Patient Selection", layout="wide")

# --------------------------
# Load Data
# --------------------------
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df = load_json()

# Extract patient names (or IDs if names not available)
patient_list = df["patientId"].tolist()

# ------------------------------------
# Custom CSS for Modern UI
# ------------------------------------
custom_css = """
<style>
.page-title {
    font-size: 32px;
    font-weight: 700;
    color: #2e466c;
    margin-bottom: -4px;
}

.page-subtitle {
    font-size: 17px;
    color: #4b5b73;
    margin-bottom: 25px;
}

.selection-box {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 10px;
    border: 1px solid #e6e6e6;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
}

.btn-select {
    background-color: #3a8ddf !important;
    color: white !important;
    border-radius: 6px;
    padding: 6px 14px;
}

.btn-clear {
    background-color: #cccccc !important;
    color: #333 !important;
    border-radius: 6px;
    padding: 6px 14px;
}

.continue-btn {
    background-color: #3a8ddf !important;
    color: white !important;
    padding: 0.7em 1.4em;
    border-radius: 8px;
}

.continue-btn:hover {
    background-color: #276bb0 !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------------------
# Title Section
# ------------------------------------
st.markdown("<div class='page-title'>Patient Selection</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='page-subtitle'>Select one or multiple patients to continue.</div>",
    unsafe_allow_html=True,
)

# ------------------------------------
# Selection Box UI
# ------------------------------------
st.markdown("<div class='selection-box'>", unsafe_allow_html=True)

# Create two columns
col_left, col_right = st.columns([3, 1])

with col_left:
    st.write("**Choose Patients:**")

    # Use session state to store selection
    if "selected_patients" not in st.session_state:
        st.session_state.selected_patients = []

    # Multi-select widget
    selected = st.multiselect(
        "Search or pick patients...",
        options=patient_list,
        default=st.session_state.selected_patients,
        label_visibility="collapsed"
    )

    st.session_state.selected_patients = selected

with col_right:
    st.write("**Quick Actions:**")
    if st.button("Select All", key="select_all"):
        st.session_state.selected_patients = patient_list
    if st.button("Deselect All", key="deselect_all"):
        st.session_state.selected_patients = []

# Close style box wrapper
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------
# Continue Button
# ------------------------------------
st.write("")
right_align = st.columns([6, 1])[1]

with right_align:
    if st.button("Continue ➜", key="continue_btn", use_container_width=True):
        st.switch_page("pages/3_Patient_Profile.py")
