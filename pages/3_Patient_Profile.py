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
# STYLE
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

.chip {
    display: inline-block;
    background: #e8f2ff;
    color: #1d3557;
    padding: 6px 14px;
    border-radius: 12px;
    margin: 4px;
    font-size: 13px;
    border: 1px solid #ccdff7;
}

.note-bubble {
    background: #f7faff;
    padding: 12px 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #457b9d;
    font-size: 14px;
}

.kpi-card {
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    color: white;
    background: linear-gradient(135deg, #1d3557 0%, #008b8b 100%);
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.kpi-value { font-size: 26px; font-weight: 800; }
.kpi-label { font-size: 14px; opacity: 0.9; }

.kpi-good { background: linear-gradient(135deg, #2a9d8f, #1d7874); }
.kpi-warn { background: linear-gradient(135deg, #ffb703, #fb8500); }
.kpi-bad  { background: linear-gradient(135deg, #e63946, #b4161b); }

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
# DEMOGRAPHICS
# ------------------------------------------------------------
pdata = json_df[json_df["patientId"] == selected_patient].iloc[0]
pdf = csv_df[csv_df["file_name"] == selected_patient].copy()

if "Date" in pdf:
    pdf["Date"] = pd.to_datetime(pdf["Date"], errors="coerce")
    pdf = pdf.sort_values("Date")

age = pdata.get("patientAge", "N/A")
payor = pdata.get("patientPrimaryPayor", "N/A")
stability = pdata.get("patientStabilityConditionRiskScore", "N/A")
ability = pdata.get("patientParticipationAbility", "N/A")

# ------------------------------------------------------------
# KPI Calculations
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
ef   = avg("Left ventricular Ejection fraction (%)")

# KPI color logic
def kpi_style(vital, val):
    if val is None: return "kpi-card"
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
# CLINICAL SUMMARY (Moved BEFORE KPIs)
# ------------------------------------------------------------
st.markdown("<div class='section-title'>🧠 Clinical Summary</div>", unsafe_allow_html=True)

summary_col = st.columns([1])[0]

summary_text = f"""
**• Age:** {age}  
**• Primary Payor:** {payor}  
**• Stability Risk Category:** {stability}  
**• Participation Ability:** {ability}  

**Vitals Overview:**  
- BP: **{sys}/{dia}** mmHg  
- Heart Rate: **{heart} bpm**  
- Glucose: **{glu} mg/dL**  
- A1C: **{a1c}%**  
- Ejection Fraction: **{ef}%**  
"""

summary_col.markdown(summary_text)

# ------------------------------------------------------------
# KPI SECTION
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

for i, (code, val, label) in enumerate(metrics):
    with kpi_cols[i % 3]:
        st.markdown(f"<div class='{kpi_style(code, val)}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{val if val else 'N/A'}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-label'>{label}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# RADAR CHART + INTERPRETATION IN 2 COLUMNS
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Overall Clinical Fingerprint</div>", unsafe_allow_html=True)
radar_left, radar_right = st.columns([1.3, 1])

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
    line_color="#1d3557",
    opacity=0.85
))
fig_radar.update_layout(
    template="simple_white",
    showlegend=False,
    width=550,
    height=500
)
radar_left.plotly_chart(fig_radar, use_container_width=True)

radar_right.markdown("""
### Interpretation
This radar chart summarizes the patient's overall **clinical signature**, comparing  
their core vital metrics on the same scale.

- **Wider spikes** indicate elevated or abnormal values  
- **Tighter shapes** reflect stable or normal physiological readings  
""")

# ------------------------------------------------------------
# CHARTS (2 Columns)
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Clinical Trends</div>", unsafe_allow_html=True)
left_col, right_col = st.columns(2)

def line(col, y, title, color):
    if y not in pdf: return
    fig = px.line(pdf, x="Date", y=y, title=title, color_discrete_sequence=[color], markers=True)
    fig.update_layout(template="simple_white")
    col.plotly_chart(fig, use_container_width=True)

with left_col:
    line(left_col, "Systolic Blood Pressure (mm[Hg])", "Systolic BP Trend", "#1d3557")
    line(left_col, "Heart rate (/min)", "Heart Rate Trend", "#008b8b")

with right_col:
    line(right_col, "Glucose (mg/dL)", "Glucose Trend", "#6a4c93")
    line(right_col, "Left ventricular Ejection fraction (%)", "Ejection Fraction Trend", "#2a9d8f")

# ------------------------------------------------------------
# CONDITIONS & NOTES — Redesigned (NO Tables)
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Conditions & Notes</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

# Conditions as chips
if "Condition_display" in pdf:
    c1.markdown("### Conditions")
    unique_conditions = pdf["Condition_display"].dropna().unique()
    chip_html = "".join([f"<span class='chip'>{c}</span>" for c in unique_conditions])
    c1.markdown(chip_html, unsafe_allow_html=True)

# Notes as bubbles
if "Note" in pdf:
    c2.markdown("### Clinical Notes")
    notes_df = pdf[["Date", "Note"]].dropna()
    for _, row in notes_df.iterrows():
        c2.markdown(
            f"<div class='note-bubble'><b>{row['Date'].date()}</b><br>{row['Note']}</div>",
            unsafe_allow_html=True
        )
