import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Patient Profile", layout="wide")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
@st.cache_data
def load_csv():
    return pd.read_csv("merged_data_RehabAiQ_Demo.csv")

@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

csv_df = load_csv()
json_df = load_json()

# ------------------------------------------------------------
# STYLE (Hybrid Blue + Teal)
# ------------------------------------------------------------
st.markdown("""
<style>

.page-title {
    font-size: 32px;
    font-weight: 900;
    color: #1d3557;
    margin-bottom: -4px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #1d3557;
    margin-top: 35px;
}

.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dce3eb;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.kpi-card {
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    color: white;
    background: linear-gradient(135deg, #1d3557 0%, #008b8b 100%);
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.kpi-value {
    font-size: 26px;
    font-weight: 800;
}

.kpi-label {
    font-size: 14px;
    opacity: 0.9;
}

.kpi-good {
    background: linear-gradient(135deg, #2a9d8f 0%, #1d7874 100%);
}

.kpi-warn {
    background: linear-gradient(135deg, #ffb703 0%, #fb8500 100%);
}

.kpi-bad {
    background: linear-gradient(135deg, #e63946 0%, #b4161b 100%);
}

.risk-flag {
    background: #ffefef;
    border-left: 6px solid #e63946;
    padding: 10px 15px;
    border-radius: 10px;
    font-weight: 600;
    color: #b4161b;
    margin-bottom: 6px;
}

.sparkline {
    margin-top: -10px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# PATIENT DROPDOWN
# ------------------------------------------------------------
patient_list = sorted(json_df["patientId"].unique())
selected_patient = st.selectbox("Choose patient", patient_list)

st.markdown(f"<div class='page-title'>Patient Profile — {selected_patient}</div>", unsafe_allow_html=True)
st.write("")

# ------------------------------------------------------------
# JSON DEMOGRAPHICS
# ------------------------------------------------------------
pdata = json_df[json_df["patientId"] == selected_patient].iloc[0]

age = pdata.get("patientAge", "N/A")
payor = pdata.get("patientPrimaryPayor", "N/A")
stability = pdata.get("patientStabilityConditionRiskScore", "N/A")
ability = pdata.get("patientParticipationAbility", "N/A")

# ------------------------------------------------------------
# CSV CLINICAL DATA
# ------------------------------------------------------------
pdf = csv_df[csv_df["file_name"] == selected_patient].copy()

if "Date" in pdf.columns:
    pdf["Date"] = pd.to_datetime(pdf["Date"], errors="coerce")
    pdf = pdf.sort_values("Date")

# ------------------------------------------------------------
# KPI CALC
# ------------------------------------------------------------
def avg(col):
    if col in pdf and pdf[col].dropna().shape[0] > 0:
        return round(pdf[col].astype(float).mean(), 1)
    return None

heart = avg("Heart rate (/min)")
sys = avg("Systolic Blood Pressure (mm[Hg])")
dia = avg("Diastolic Blood Pressure (mm[Hg])")
glu = avg("Glucose (mg/dL)")
a1c = avg("Hemoglobin A1c/Hemoglobin.total in Blood (%)")
ef = avg("Left ventricular Ejection fraction (%)")

# ------------------------------------------------------------
# KPI COLOR LOGIC
# ------------------------------------------------------------
def kpi_style(vital, val):
    if val is None:
        return "kpi-card"
    if vital == "sys":
        if val >= 140: return "kpi-card kpi-bad"
        if val >= 130: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "dia":
        if val >= 90: return "kpi-card kpi-bad"
        if val >= 85: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "hr":
        if val > 110: return "kpi-card kpi-bad"
        if val > 100: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "glu":
        if val > 180: return "kpi-card kpi-bad"
        if val > 140: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "a1c":
        if val > 6.5: return "kpi-card kpi-bad"
        if val > 6: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "ef":
        if val < 40: return "kpi-card kpi-bad"
        if val < 50: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    return "kpi-card"

# ------------------------------------------------------------
# KPI ROWS (2 COLUMNS × 3)
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Clinical KPIs</div>", unsafe_allow_html=True)

kpi_cols = st.columns(3)
metrics = [
    ("hr", heart, "Heart Rate"),
    ("sys", sys, "Systolic BP"),
    ("dia", dia, "Diastolic BP"),
    ("glu", glu, "Glucose"),
    ("a1c", a1c, "Hemoglobin A1C"),
    ("ef", ef, "Ejection Fraction"),
]

for (i, (code, val, label)) in enumerate(metrics):
    col = kpi_cols[i % 3]
    with col:
        st.markdown(f"<div class='{kpi_style(code, val)}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{val if val else 'N/A'}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-label'>{label}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# RISK FLAGS
# ------------------------------------------------------------
flags = []

if sys and sys >= 140:
    flags.append("⚠️ Possible Hypertension — Elevated Systolic BP")
if dia and dia >= 90:
    flags.append("⚠️ Possible Hypertension — Elevated Diastolic BP")
if glu and glu >= 180:
    flags.append("⚠️ Hyperglycemia — High Glucose Levels")
if a1c and a1c >= 6.5:
    flags.append("⚠️ Diabetes Risk — Elevated A1C")
if ef and ef < 40:
    flags.append("⚠️ Heart Failure Risk — Low Ejection Fraction")

if flags:
    st.markdown("<div class='section-title'>Risk Flags</div>", unsafe_allow_html=True)
    for f in flags:
        st.markdown(f"<div class='risk-flag'>{f}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# CLINICAL SUMMARY
# ------------------------------------------------------------
summary_text = f"""
### 🧠 Clinical Summary  
Patient **{selected_patient}**, age **{age}**, insured via **{payor}**:

- **Stability Risk:** {stability}  
- **Participation Ability:** {ability}  

Key observations:
- **Blood pressure:** {sys} / {dia} mmHg  
- **Heart rate:** {heart} bpm  
- **Glucose:** {glu} mg/dL  
- **A1C:** {a1c}%  
- **Ejection Fraction:** {ef}%  

"""

st.markdown(summary_text)

# ------------------------------------------------------------
# 2-COLUMN LAYOUT FOR CHARTS
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Clinical Trends</div>", unsafe_allow_html=True)
left_col, right_col = st.columns(2)

# Helper chart function
def line_chart(col, df, y, title, color):
    if y not in df.columns:
        return
    fig = px.line(df, x="Date", y=y, title=title, markers=True,
                  color_discrete_sequence=[color])
    fig.update_layout(template="simple_white")
    col.plotly_chart(fig, use_container_width=True)

with left_col:
    line_chart(left_col, pdf, "Systolic Blood Pressure (mm[Hg])", "Systolic BP Trend", "#1d3557")
    line_chart(left_col, pdf, "Heart rate (/min)", "Heart Rate Trend", "#008b8b")

with right_col:
    line_chart(right_col, pdf, "Glucose (mg/dL)", "Glucose Trend", "#6a4c93")
    line_chart(right_col, pdf, "Left ventricular Ejection fraction (%)", "Ejection Fraction Trend", "#2a9d8f")

# ------------------------------------------------------------
# RADAR CHART
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Overall Clinical Fingerprint</div>", unsafe_allow_html=True)

radar_vals = [
    heart or 0,
    sys or 0,
    dia or 0,
    glu or 0,
    a1c or 0,
    ef or 0
]

radar_labels = ["HR", "SysBP", "DiaBP", "Glucose", "A1C", "EF"]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=radar_vals,
    theta=radar_labels,
    fill='toself',
    name="Vitals",
    line_color="#1d3557"
))
fig_radar.update_layout(template="simple_white", showlegend=False)
st.plotly_chart(fig_radar, use_container_width=True)

# ------------------------------------------------------------
# CONDITIONS & NOTES IN 2 COLUMNS
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Conditions & Notes</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

if "Condition_display" in pdf:
    c1.markdown("### Conditions")
    c1.dataframe(pdf[["Condition_display", "Condition_code"]].drop_duplicates())

if "Note" in pdf:
    c2.markdown("### Clinical Notes")
    c2.dataframe(pdf[["Date", "Note"]].dropna())
