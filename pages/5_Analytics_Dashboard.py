import streamlit as st
import pandas as pd
import json
import plotly.express as px
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

# Fix naming if needed
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
# PAGE HEADER
# -------------------------------------------------
st.title("📊 RehabAiQ — Analytics Dashboard")


# -------------------------------------------------
# 4-COLUMN TOP METRICS + DONUTS
# -------------------------------------------------
col1, col2, col3, col4 = st.columns([1.3, 0.8, 1, 1])

# Suggested Facility Chart
with col1:
    st.subheader("Suggested Facility Setting")

    facility_counts = df_json["potentialFacilitySetting"].value_counts()
    fig = px.bar(
        facility_counts,
        labels={"value": "Count", "index": "Facility"},
        color=facility_counts.index,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

# Total Patients
with col2:
    st.subheader("Total Patients")
    st.metric(label="", value=len(df_json))

# Stability Donut
with col3:
    st.subheader("Stability Risk Score")
    fig = px.pie(
        df_json,
        names="patientStabilityConditionRiskScore",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

# Ability Donut
with col4:
    st.subheader("Participation Ability")
    fig = px.pie(
        df_json,
        names="patientParticipationAbility",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------
# SECOND ROW: Functional Deficit + Therapy Goals
# -------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("Functional Deficiencies")
    fig = px.pie(
        df_json,
        names="functional_deficit",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Therapy Goals")
    fig = px.pie(
        df_json,
        names="therapy_goal",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------
# PATIENT TABLE
# -------------------------------------------------
st.subheader("Patients List")

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

st.dataframe(table, use_container_width=True, height=500)
