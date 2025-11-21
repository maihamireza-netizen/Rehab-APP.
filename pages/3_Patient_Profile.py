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
# STYLING — Hybrid Blue + Teal + Professional Dividers
# ------------------------------------------------------------
st.markdown("""
<style>

html,body,[class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* PAGE TITLE */
.page-title {
    font-size: 34px;
    font-weight: 900;
    color: #1d3557;
    margin-bottom: 10px;
}

/* SECTION TITLE */
.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #1d3557;
    margin-top: 35px;
    margin-bottom: 6px;
}

/* Divider (Style E) */
.divider-line {
    height: 1px;
    background: #dce3eb;
    margin-top: 4px;
    margin-bottom: 18px;
}

/* Summary body text */
.summary-text {
    font-size: 16px;
    color: #2f3b52;
    line-height: 1.45;
    margin-bottom: 10px;
}

/* KPI CARDS */
.kpi-card {
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    color: white;
    background: linear-gradient(135deg, #1d3557 0%, #008b8b 100%);
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    margin-bottom: 16px;
}

.kpi-value { font-size: 26px; font-weight: 800; }
.kpi-label { font-size: 14px; opacity:0.9; }

.kpi-good { background: linear-gradient(135deg, #2a9d8f, #1d7874); }
.kpi-warn { background: linear-gradient(135deg, #ffb703, #fb8500); }
.kpi-bad  { background: linear-gradient(135deg, #e63946, #b4161b); }

/* CONDITIONS (chips) */
.chip {
    display:inline-block;
    background:#e8f2ff;
    color:#1d3557;
    padding:6px 14px;
    border-radius:12px;
    margin:4px;
    font-size:13px;
    border:1px solid #ccdff7;
}

/* NOTES (bubble style) */
.note-bubble {
    background:#f7faff;
    padding:12px 15px;
    border-radius:10px;
    margin-bottom:10px;
    border-left:4px solid #457b9d;
    font-size:14px;
    color:#2f3b52;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# PATIENT SELECTION
# ------------------------------------------------------------
patient_list = sorted(json_df["patientId"].unique())
selected_patient = st.selectbox("Choose patient", patient_list)

st.markdown(f"<div class='page-title'>Patient Profile — {selected_patient}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# DATA FILTERING
# ------------------------------------------------------------
pdata = json_df[json_df["patientId"] == selected_patient].iloc[0]
pdf = csv_df[csv_df["file_name"] == selected_patient].copy()

if "Date" in pdf.columns:
    pdf["Date"] = pd.to_datetime(pdf["Date"], errors="coerce")
    pdf = pdf.sort_values("Date")

# Basic info
age = pdata.get("patientAge", "N/A")
payor = pdata.get("patientPrimaryPayor", "N/A")
stability = pdata.get("patientStabilityConditionRiskScore", "N/A")
ability = pdata.get("patientParticipationAbility", "N/A")

# ------------------------------------------------------------
# KPI VALUES
# ------------------------------------------------------------
def avg(col):
    try:
        return round(pdf[col].astype(float).dropna().mean(), 1)
    except:
        return None

heart = avg("Heart rate (/min)")
sys   = avg("Systolic Blood Pressure (mm[Hg])")
dia   = avg("Diastolic Blood Pressure (mm[Hg])")
glu   = avg("Glucose (mg/dL)")
a1c   = avg("Hemoglobin A1c/Hemoglobin.total in Blood (%)")
ef    = avg("Left ventricular Ejection fraction (%)")

# KPI styles
def kpi_style(vital, val):
    if val is None: return "kpi-card"
    if vital == "sys":
        if val >=140: return "kpi-card kpi-bad"
        if val >=130: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "dia":
        if val >=90: return "kpi-card kpi-bad"
        if val >=85: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "hr":
        if val>110: return "kpi-card kpi-bad"
        if val>100: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "glu":
        if val>180: return "kpi-card kpi-bad"
        if val>140: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "a1c":
        if val>6.5: return "kpi-card kpi-bad"
        if val>6: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    if vital == "ef":
        if val<40: return "kpi-card kpi-bad"
        if val<50: return "kpi-card kpi-warn"
        return "kpi-card kpi-good"
    return "kpi-card"

# ------------------------------------------------------------
# CLINICAL SUMMARY (NOW BEFORE KPI)
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Clinical Summary</div>", unsafe_allow_html=True)
st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

summary_text = f"""
<div class='summary-text'>
<strong>Age:</strong> {age} <br>
<strong>Primary Payor:</strong> {payor} <br>
<strong>Stability Risk:</strong> {stability} <br>
<strong>Participation Ability:</strong> {ability} <br><br>

<strong>Vitals Overview</strong> <br>
• BP: <strong>{sys}/{dia}</strong> mmHg <br>
• Heart Rate: <strong>{heart} bpm</strong> <br>
• Glucose: <strong>{glu} mg/dL</strong> <br>
• A1C: <strong>{a1c}%</strong> <br>
• Ejection Fraction: <strong>{ef}%</strong>
</div>
"""
st.markdown(summary_text, unsafe_allow_html=True)

# ------------------------------------------------------------
# KPI CARDS
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Clinical KPIs</div>", unsafe_allow_html=True)
st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

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
        st.markdown(
            f"<div class='{kpi_style(code, val)}'>"
            f"<div class='kpi-value'>{val if val else 'N/A'}</div>"
            f"<div class='kpi-label'>{label}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

# ------------------------------------------------------------
# CLINICAL FINGERPRINT — LARGER + 2 COLUMN
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Overall Clinical Fingerprint</div>", unsafe_allow_html=True)
st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

radar_left, radar_right = st.columns([1.5, 1])

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
    width=650,
    height=550
)

radar_left.plotly_chart(fig_radar, use_container_width=True)

radar_right.markdown("""
<div class='summary-text'>
The radar chart summarizes how this patient's core vitals compare  
to each other. Wide areas indicate elevated values, while narrow  
areas indicate stable or lower ranges. This provides a concise  
snapshot of physiological balance.
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# CLINICAL TRENDS — CHARTS (2 COLUMNS)
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Clinical Trends</div>", unsafe_allow_html=True)
st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

left_col, right_col = st.columns(2)

def line(col, y, title, color):
    if y not in pdf:
        return
    fig = px.line(pdf, x="Date", y=y, title=title, 
                  color_discrete_sequence=[color], markers=True)
    fig.update_layout(template="simple_white")
    col.plotly_chart(fig, use_container_width=True)

with left_col:
    line(left_col, "Systolic Blood Pressure (mm[Hg])", "Systolic BP Trend", "#1d3557")
    line(left_col, "Heart rate (/min)", "Heart Rate Trend", "#008b8b")

with right_col:
    line(right_col, "Glucose (mg/dL)", "Glucose Trend", "#6a4c93")
    line(right_col, "Left ventricular Ejection fraction (%)", "Ejection Fraction Trend", "#2a9d8f")

# ------------------------------------------------------------
# CONDITIONS & NOTES — ORGANIZED & CLEAN
# ------------------------------------------------------------
st.markdown("<div class='section-title'>Conditions & Notes</div>", unsafe_allow_html=True)
st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

if "Condition_display" in pdf:
    c1.markdown("### Conditions")
    unique_conditions = pdf["Condition_display"].dropna().unique()
    chips = "".join([f"<span class='chip'>{c}</span>" for c in unique_conditions])
    c1.markdown(chips, unsafe_allow_html=True)

if "Note" in pdf:
    c2.markdown("### Clinical Notes")
    notes_df = pdf[["Date", "Note"]].dropna()
    for _, row in notes_df.iterrows():
        c2.markdown(
            f"<div class='note-bubble'><b>{row['Date'].date()}</b><br>{row['Note']}</div>",
            unsafe_allow_html=True
        )
