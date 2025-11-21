import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_csv():
    return pd.read_csv("merged_data_RehabAiQ_Demo.csv")

df_json = load_json()
df_csv = load_csv()


# -------------------------------------------------
# FIX FIELD NAMES
# -------------------------------------------------
if "patientid" in df_json.columns:
    df_json.rename(columns={"patientid": "patientId"}, inplace=True)


# -------------------------------------------------
# MOCK FIELDS (Functional Deficit + Therapy Goals)
# -------------------------------------------------
def map_functional_deficit(row):
    risk = row["patientStabilityConditionRiskScore"]
    ability = row["patientParticipationAbility"]

    if ability == "Low Ability" and risk == "High Risk":
        return "Complex Deficit"
    if risk == "High Risk":
        return "High Deficit"
    if ability == "Low Ability":
        return "High Deficit"
    return "Medium Deficit"

df_json["functional_deficit"] = df_json.apply(map_functional_deficit, axis=1)

therapy_categories = ["Mobility Goals", "Cognitive Goals", "Self-Care Goals", "Behavioral Goals"]
df_json["therapy_goal"] = df_json["patientId"].apply(lambda x: therapy_categories[hash(x) % 4])


# -------------------------------------------------
# PAGE STYLES (Sidebar light, dashboard dark)
# -------------------------------------------------
st.markdown("""
<style>

    /* Sidebar stays white */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }

    /* Dashboard background */
    div.block-container {
        background-color: #0d1117 !important;
        padding-top: 25px;
    }

    /* Text color inside dashboard */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #f3f4f6 !important;
    }

    /* Dataframe styling */
    .dataframe th {
        color: white !important;
        background-color: #1f2937 !important;
    }
    .dataframe td {
        color: white !important;
        background-color: #111827 !important;
    }

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("<h1>📊 RehabAiQ — Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-bottom:20px;'>Performance view of all patients and recommended settings.</p>", unsafe_allow_html=True)



# -------------------------------------------------
# TOP ROW CHARTS
# -------------------------------------------------
col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

# Suggested Facility bar
with col1:
    st.markdown("### Suggested Facility Setting")
    facility_counts = df_json["potentialFacilitySetting"].value_counts()

    fig = px.bar(
        facility_counts,
        color=facility_counts.index,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

# Total Patients
with col2:
    st.markdown("### Total Patients")
    st.markdown(f"<h1 style='font-size:72px; color:#10b981;'>{len(df_json)}</h1>", unsafe_allow_html=True)

# Stability Risk donut
with col3:
    st.markdown("### Stability Risk Score")
    fig = px.pie(
        df_json,
        names="patientStabilityConditionRiskScore",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(paper_bgcolor="#0d1117", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# Participation Ability donut
with col4:
    st.markdown("### Participation Ability")
    fig = px.pie(
        df_json,
        names="patientParticipationAbility",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(paper_bgcolor="#0d1117", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)



# -------------------------------------------------
# SECOND ROW (Functional Deficit + Therapy)
# -------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    st.markdown("### Functional Deficiencies")
    fig = px.pie(
        df_json,
        names="functional_deficit",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(paper_bgcolor="#0d1117", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.markdown("### Therapy Goals")
    fig = px.pie(
        df_json,
        names="therapy_goal",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Alphabet
    )
    fig.update_layout(paper_bgcolor="#0d1117", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)



# -------------------------------------------------
# PATIENT TABLE
# -------------------------------------------------
st.markdown("### Patients List")

table = df_json[[
    "patientId",
    "patientName",
    "potentialFacilitySetting",
    "patientStabilityConditionRiskScore",
    "patientParticipationAbility",
    "functional_deficit",
    "therapy_goal"
]]

table = table.rename(columns={
    "patientId": "Patient ID",
    "patientName": "Patient Name",
    "potentialFacilitySetting": "Best Setting",
    "patientStabilityConditionRiskScore": "Risk",
    "patientParticipationAbility": "Ability",
    "functional_deficit": "Functional Deficit",
    "therapy_goal": "Therapy Goal"
})

st.dataframe(table, use_container_width=True, height=480)
