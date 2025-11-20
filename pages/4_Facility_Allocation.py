import streamlit as st
import pandas as pd
import json
import plotly.express as px

@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df = load_json()

st.markdown("<div class='header-title'>Facility Allocation Matrix</div>", unsafe_allow_html=True)

ability_map = {"High Ability": 3, "Medium Ability": 2, "Low Ability": 1}
stability_map = {"Low Risk": 30, "Medium Risk": 60, "High Risk": 90}

df["ability_score"] = df["patientParticipationAbility"].map(ability_map)
df["stability_score"] = df["patientStabilityConditionRiskScore"].map(stability_map)

ability_w = st.slider("Participation Weight", 0.0, 1.0, 0.5)
stability_w = 1 - ability_w

df["adj_ability"] = df["ability_score"] * ability_w
df["adj_stability"] = df["stability_score"] * stability_w

fig = px.scatter(
    df,
    x="adj_stability",
    y="adj_ability",
    color="potentialFacilitySetting",
    hover_name="patientId",
    labels={
        "adj_stability": "Stability (weighted)",
        "adj_ability": "Ability (weighted)"
    },
    title="Patient Allocation Matrix"
)

st.plotly_chart(fig, use_container_width=True)
