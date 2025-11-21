import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Patient Profile", layout="wide")

# -------------------------------------------------
# Load CSV (clinical data) and JSON model
# -------------------------------------------------
@st.cache_data
def load_csv():
    return pd.read_csv("merged_data_RehabAiQ_Demo.csv")

@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

csv_df = load_csv()
json_df = load_json()

# -------------------------------------------------
# UI Styling
# -------------------------------------------------
st.markdown("""
<style>
.page-title {
    font-size: 32px;
    font-weight: 800;
    color: #2e466c;
    margin-bottom: -4px;
}
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #2e466c;
    margin-top: 30px;
}
.kpi-box {
    background-color: #f9fbff;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #d8e3f2;
    text-align: center;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #2e466c;
}
.kpi-label {
    font-size: 14px;
    color: #6a7c92;
}
.risk-flag {
    background: #ffecec;
    border-left: 6px solid #d9534f;
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 8px;
    color: #8a2724;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Patient Selection
# -------------------------------------------------
patient_name_list = sorted(json_df["patientId"].unique())
selected_patient = st.selectbox("Choose patient", patient_name_list)

st.markdown(f"<div class='page-title'>Patient Profile — {selected_patient}</div>", unsafe_allow_html=True)
st.write("")

# -------------------------------------------------
# Filter JSON for demographics
# -------------------------------------------------
pdata = json_df[json_df["patientId"] == selected_patient].iloc[0]
age = pdata.get("patientAge", "N/A")
payor = pdata.get("patientPrimaryPayor", "N/A")
stability = pdata.get("patientStabilityConditionRiskScore", "N/A")
ability = pdata.get("patientParticipationAbility", "N/A")

# -------------------------------------------------
# Filter CSV for patient clinical data
# -------------------------------------------------
pdf = csv_df[csv_df["file_name"] == selected_patient].copy()
if "Date" in pdf:
    pdf["Date"] = pd.to_datetime(pdf["Date"], errors="coerce")

# -------------------------------------------------
# KPI Function
# -------------------------------------------------
def safe_avg(col):
    return round(pdf[col].dropna().astype(float).mean(), 1) if col in pdf.columns else None

kpi_heart = safe_avg("Heart rate (/min)")
kpi_sys = safe_avg("Systolic Blood Pressure (mm[Hg])")
kpi_dia = safe_avg("Diastolic Blood Pressure (mm[Hg])")
kpi_glucose = safe_avg("Glucose (mg/dL)")
kpi_a1c = safe_avg("Hemoglobin A1c/Hemoglobin.total in Blood (%)")
kpi_ef = safe_avg("Left ventricular Ejection fraction (%)")

# -------------------------------------------------
# Trend Slope Function
# -------------------------------------------------
def compute_slope(df, col):
    if col not in df.columns or df[col].dropna().empty:
        return None
    tmp = df.dropna(subset=[col])
    if len(tmp) < 2:
        return None
    x = np.array(range(len(tmp))).reshape(-1, 1)
    y = tmp[col].astype(float).values.reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    slope = model.coef_[0][0]
    return round(slope, 3)

trend_heart = compute_slope(pdf, "Heart rate (/min)")
trend_sys = compute_slope(pdf, "Systolic Blood Pressure (mm[Hg])")
trend_dia = compute_slope(pdf, "Diastolic Blood Pressure (mm[Hg])")
trend_glu = compute_slope(pdf, "Glucose (mg/dL)")

# -------------------------------------------------
# Risk Flags
# -------------------------------------------------
flags = []

if kpi_sys and kpi_sys > 140:
    flags.append("⚠️ Possible Hypertension — Elevated Systolic BP")
if kpi_dia and kpi_dia > 90:
    flags.append("⚠️ Possible Hypertension — Elevated Diastolic BP")
if kpi_glucose and kpi_glucose > 180:
    flags.append("⚠️ Hyperglycemia Risk — High Glucose Levels")
if kpi_a1c and kpi_a1c > 6.5:
    flags.append("⚠️ Diabetes Risk — Elevated Hemoglobin A1C")
if kpi_ef and kpi_ef < 40:
    flags.append("⚠️ Heart Failure Risk — Low Ejection Fraction")
if trend_sys and trend_sys > 0.5:
    flags.append("⚠️ BP Trend Increasing — Monitor Closely")

# -------------------------------------------------
# Display Risk Flags
# -------------------------------------------------
if flags:
    st.markdown("<div class='section-title'>Risk Flags</div>", unsafe_allow_html=True)
    for f in flags:
        st.markdown(f"<div class='risk-flag'>{f}</div>", unsafe_allow_html=True)

# -------------------------------------------------
# AI-Style Clinical Summary
# -------------------------------------------------
summary = f"""
### 🧠 Clinical Summary
Patient **{selected_patient}**, age **{age}**, shows:

- **Blood Pressure Trend:** {'increasing' if trend_sys and trend_sys > 0 else 'stable/decreasing'}
- **Glucose Levels:** {'elevated' if kpi_glucose and kpi_glucose > 150 else 'normal range'}
- **Heart Rate:** averaging **{kpi_heart} bpm**, trend is {'upward' if trend_heart and trend_heart > 0 else 'stable'}
- **Ejection Fraction:** **{kpi_ef}%**, indicating { 'potential cardiac impairment' if kpi_ef and kpi_ef < 50 else 'normal ventricular function'}

Overall, the patient displays:  
- **{stability} stability risk category**  
- **{ability} participation ability**  
"""

st.markdown(summary)

# -------------------------------------------------
# KPI Row
# -------------------------------------------------
st.markdown("<div class='section-title'>Clinical Summary Metrics</div>", unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)

def kpi(col, value, label):
    with col:
        st.markdown("<div class='kpi-box'>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{value if value else 'N/A'}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-label'>{label}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

kpi(k1, kpi_heart, "Avg Heart Rate")
kpi(k2, kpi_sys, "Avg Systolic BP")
kpi(k3, kpi_dia, "Avg Diastolic BP")
kpi(k4, kpi_glucose, "Avg Glucose")
kpi(k5, kpi_a1c, "Avg Hemoglobin A1C")
kpi(k6, kpi_ef, "Ejection Fraction")

# -------------------------------------------------
# Radar Chart
# -------------------------------------------------
st.markdown("<div class='section-title'>Clinical Radar Overview</div>", unsafe_allow_html=True)

radar_vals = [kpi_heart or 0, kpi_sys or 0, kpi_dia or 0, kpi_glucose or 0, kpi_a1c or 0, kpi_ef or 0]
radar_labels = ["Heart Rate", "Sys BP", "Dia BP", "Glucose", "A1C", "EF"]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=radar_vals,
    theta=radar_labels,
    fill='toself',
    name="Patient Metrics",
    line_color="#3a8ddf"
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Timeline Chart
# -------------------------------------------------
if "Date" in pdf:
    st.markdown("<div class='section-title'>Clinical Timeline</div>", unsafe_allow_html=True)
    timeline = pdf.groupby("Date").size().reset_index(name="Events")
    fig_tl = px.bar(timeline, x="Date", y="Events", title="Events per Day")
    st.plotly_chart(fig_tl, use_container_width=True)

# -------------------------------------------------
# Conditions Table
# -------------------------------------------------
if "Condition_display" in pdf:
    st.markdown("<div class='section-title'>Conditions</div>", unsafe_allow_html=True)
    st.dataframe(pdf[["Condition_display","Condition_code"]].drop_duplicates(), use_container_width=True)

# -------------------------------------------------
# Notes Table
# -------------------------------------------------
if "Note" in pdf:
    st.markdown("<div class='section-title'>Clinical Notes</div>", unsafe_allow_html=True)
    st.dataframe(pdf[["Date","Note"]].dropna(), use_container_width=True)
