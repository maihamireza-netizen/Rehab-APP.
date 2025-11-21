import streamlit as st
import pandas as pd
import json

@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df = load_json()

st.markdown("<div class='header-title'>Patient Selection</div>", unsafe_allow_html=True)

patients = df["patientId"].unique()

selected = st.multiselect(
    "Select patients",
    patients,
    placeholder="Choose patients..."
)

st.session_state.selected_patients = selected

st.success(f"{len(selected)} patient(s) selected.")

if st.button("Go to Profile ➜") and selected:
    st.switch_page("pages/3_Patient_Profile.py")

