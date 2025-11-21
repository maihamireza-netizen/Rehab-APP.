import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df_json = load_json()

# -------------------------
# Mock Functional Deficit Category
# -------------------------
def mock_functional_deficit(row):
    if row["patientParticipationAbility"] == "Low Ability":
        return "High Deficit"
    if row["patientParticipationAbility"] == "Medium Ability":
        return "Medium Deficit"
    return "Low Deficit"

df_json["functional_deficit"] = df_json.apply(mock_functional_deficit, axis=1)

# -------------------------
# Therapy Goal Mock
# -------------------------
therapy_goals = ["Mobility Goals", "Cognitive Goals", "Self-Care Goals", "Behavioral Goals"]
df_json["therapy_goal"] = df_json["patientId"].apply(lambda x: therapy_goals[hash(x) % 4])

# -------------------------
# Page Header
# -------------------------
st.markdown("""
<div style="display:flex; align-items:center; gap:12px;">
    <img src='Logo.png' width='120'>
    <h1 style='margin-top:15px;'>RehabAiQ — Analytics Dashboard</h1>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------
# TOP ROW — PIE CHARTS
# -------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Stability Risk Score")
    fig_risk = px.pie(
        df_json,
        names="patientStabilityConditionRiskScore",
        color="patientStabilityConditionRiskScore",
        color_discrete_map={
            "Low Risk": "#7CD992",
            "Medium Risk": "#FFAF66",
            "High Risk": "#FF6B6B"
        }
    )
    fig_risk.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_risk, use_container_width=True)

with col2:
    st.subheader("Participation Ability")
    fig_ability = px.pie(
        df_json,
        names="patientParticipationAbility",
        color="patientParticipationAbility",
        color_discrete_map={
            "Low Ability": "#A78BFA",
            "Medium Ability": "#60A5FA",
            "High Ability": "#34D399"
        }
    )
    fig_ability.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_ability, use_container_width=True)

with col3:
    st.subheader("Functional Deficit")
    fig_deficit = px.pie(
        df_json,
        names="functional_deficit",
        color="functional_deficit",
        color_discrete_map={
            "Low Deficit": "#6EE7B7",
            "Medium Deficit": "#60A5FA",
            "High Deficit": "#F472B6"
        }
    )
    fig_deficit.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_deficit, use_container_width=True)

with col4:
    st.subheader("Therapy Goals")
    fig_goals = px.pie(
        df_json,
        names="therapy_goal",
        color="therapy_goal",
        color_discrete_map={
            "Mobility Goals": "#34D399",
            "Cognitive Goals": "#FBBF24",
            "Self-Care Goals": "#60A5FA",
            "Behavioral Goals": "#F87171"
        }
    )
    fig_goals.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_goals, use_container_width=True)

# -------------------------
# FACILITY SETTING BAR CHART
# -------------------------
st.subheader("Suggested Facility Setting")
fig_fac = px.bar(
    df_json,
    x="potentialFacilitySetting",
    color="potentialFacilitySetting",
    color_discrete_map={
        "ALF": "#34D399",
        "ARF": "#60A5FA",
        "SNF": "#A78BFA",
        "ACH": "#F87171"
    }
)
st.plotly_chart(fig_fac, use_container_width=True)

# -------------------------
# PATIENT LIST TABLE
# -------------------------

# Facility Color Mapping
facility_colors = {
    "ALF": "background-color:#34D399;color:white;",
    "ARF": "background-color:#60A5FA;color:white;",
    "SNF": "background-color:#A78BFA;color:white;",
    "ACH": "background-color:#F87171;color:white;",
}

styled_df = df_json[[
    "patientId",
    "potentialFacilitySetting",
    "patientStabilityConditionRiskScore",
    "patientParticipationAbility",
    "patientPrimaryPayor",
    "patientAge",
    "functional_deficit",
    "therapy_goal"
]].rename(columns={
    "patientId": "Patient ID",
    "potentialFacilitySetting": "Facility",
    "patientStabilityConditionRiskScore": "Risk Score",
    "patientParticipationAbility": "Ability",
    "patientPrimaryPayor": "Payor",
    "patientAge": "Age",
    "functional_deficit": "Functional Deficit",
    "therapy_goal": "Therapy Goal"
})

def color_facility(val):
    return facility_colors.get(val, "")

st.subheader("Patients List")
st.dataframe(
    styled_df.style.applymap(color_facility, subset=["Facility"]),
    use_container_width=True,
    height=600
)
