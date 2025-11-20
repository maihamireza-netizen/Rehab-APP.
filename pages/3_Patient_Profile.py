import streamlit as st
import pandas as pd
import json

@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_csv():
    return pd.read_csv("merged_data_RehabAiQ_Demo.csv")

json_df = load_json()
csv_df = load_csv()

if "selected_patients" not in st.session_state or len(st.session_state.selected_patients) == 0:
    st.error("Please select a patient from Patient Selection.")
    st.stop()

patient_id = st.selectbox("Choose patient", st.session_state.selected_patients)
pdata = json_df[json_df["patientId"] == patient_id].iloc[0]

st.markdown(f"<div class='header-title'>Patient Profile — {patient_id}</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Demographics")
    st.write(f"**Age:** {pdata['patientAge']}")
    st.write(f"**Payor:** {pdata['patientPrimaryPayor']}")
    st.write(f"**Stability Risk:** {pdata['patientStabilityConditionRiskScore']}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Rehab Information")
    st.write(f"**Participation Ability:** {pdata['patientParticipationAbility']}")
    st.write(f"**Recommended Setting:** {pdata['potentialFacilitySetting']}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("Clinical Data (CSV)")
st.dataframe(csv_df.head(50))

