import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

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
# MOCK FIELDS (Functional Deficit + Therapy Goals)
# -------------------------------------------------

# Functional deficit based on Ability + Risk
def map_functional_deficit(row):
    ability = row["patientParticipationAbility"]
    risk = row["patientStabilityConditionRiskScore"]
    
    if ability == "Low Ability" and risk == "High Risk":
        return "Complex Deficit"
    if risk == "High Risk":
        return "High Deficit"
    if ability == "Low Ability":
        return "High Deficit"
    return "Medium Deficit"

df_json["functional_deficit"] = df_json.apply(map_functional_deficit, axis=1)

# Therapy goals (mock)
# Therapy goals (mock)
therapy_categories = ["Mobility Goals", "Cognitive Goals", "Self-Care Goals", "Behavioral Goals"]
df_json["therapy_goal"] = df_json["patientId"].apply(lambda x: therapy_categories[hash(x) % 4])

# -------------------------------------------------
# DARK THEME STYLE
# -------------------------------------------------
st.markdown("""
<style>
body { background-color: #111827; }
.block-container { background-color: #111827; padding-top: 20px; }
h1, h2, h3, h4, h5, h6, p, label, div, span {
    color: #f3f4f6 !important;
}
.dataframe th { color: white !important; background-color: #1f2937 !important; }
.dataframe td { color: white !important; background-color: #111827 !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("<h1>📊 RehabAiQ — Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #374151;'>", unsafe_allow_html=True)

# -------------------------------------------------
# TOP STATS ROW (4 columns)
# -------------------------------------------------
col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])

with col1:
    st.markdown("<h3>Suggested Facility Setting</h3>", unsafe_allow_html=True)
    facility_counts = df_json["potentialFacilitySetting"].value_counts()
    fig = px.bar(facility_counts, 
                 color=facility_counts.index,
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Total Patients", len(df_json))

with col3:
    st.markdown("<h4>Stability Condition Risk</h4>", unsafe_allow_html=True)
    fig = px.pie(df_json, names="patientStabilityConditionRiskScore",
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 hole=0.45)
    fig.update_layout(paper_bgcolor="#111827", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown("<h4>Participation Ability</h4>", unsafe_allow_html=True)
    fig = px.pie(df_json, names="patientParticipationAbility",
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 hole=0.45)
    fig.update_layout(paper_bgcolor="#111827", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# SECOND ROW (2 donut charts)
# -------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    st.markdown("<h4>Functional Deficiencies</h4>", unsafe_allow_html=True)
    fig = px.pie(df_json, names="functional_deficit",
                 color_discrete_sequence=px.colors.qualitative.Dark24,
                 hole=0.45)
    fig.update_layout(paper_bgcolor="#111827", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.markdown("<h4>Therapy Goals</h4>", unsafe_allow_html=True)
    fig = px.pie(df_json, names="therapy_goal",
                 color_discrete_sequence=px.colors.qualitative.Pastel1,
                 hole=0.45)
    fig.update_layout(paper_bgcolor="#111827", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# THIRD ROW (Patient Table + Mock Map)
# -------------------------------------------------
col7, col8 = st.columns([2, 1])

with col7:
    st.markdown("<h3>Patients List</h3>", unsafe_allow_html=True)
    table = df_json[[
        "patientid",
        "patientName",
        "potentialFacilitySetting",
        "patientStabilityConditionRiskScore",
        "patientParticipationAbility",
        "functional_deficit",
        "therapy_goal"
    ]].rename(columns={
        "patientid": "Patient ID",
        "patientName": "Patient Name",
        "potentialFacilitySetting": "Best Setting",
        "patientStabilityConditionRiskScore": "Risk Score",
        "patientParticipationAbility": "Participation Ability",
        "functional_deficit": "Functional Deficit",
        "therapy_goal": "Therapy Goal"
    })
    st.dataframe(table, use_container_width=True, height=500)

with col8:
    st.markdown("<h3>Suggested Facility Setting Map</h3>", unsafe_allow_html=True)

    # MOCK GEO COORDINATES
    import numpy as np
    df_json["lat"] = 27.5 + np.random.uniform(-0.3, 0.3, len(df_json))
    df_json["lon"] = -82.5 + np.random.uniform(-0.3, 0.3, len(df_json))

    fig = px.scatter_mapbox(df_json,
                            lat="lat", lon="lon",
                            color="potentialFacilitySetting",
                            zoom=7,
                            height=500,
                            color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="#111827")
    st.plotly_chart(fig, use_container_width=True)
