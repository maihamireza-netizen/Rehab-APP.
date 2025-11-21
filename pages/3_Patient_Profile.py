import streamlit as st
import pandas as pd
import json
import base64

st.set_page_config(page_title="Patient Profile", layout="wide")

# -----------------------------------------------------
# Background (same as Login)
# -----------------------------------------------------
def set_bg(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}

        .profile-card {{
            background: rgba(255, 255, 255, 0.85);
            padding: 25px;
            border-radius: 14px;
            box-shadow: 0px 3px 12px rgba(0,0,0,0.15);
        }}

        .summary-card {{
            background: rgba(255, 255, 255, 0.92);
            padding: 25px;
            border-radius: 14px;
            margin-top: 20px;
        }}

        .section-title {{
            font-size: 28px;
            font-weight: 700;
            color: #183153;
            margin-bottom: 10px;
        }}

        .metric-label {{
            font-size: 16px;
            font-weight: 600;
            color: #2e466c;
        }}

        .metric-value {{
            font-size: 18px;
            font-weight: 700;
            color: #111;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------
@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_csv():
    return pd.read_csv("merged_data_RehabAiQ_Demo.csv")

df_json = load_json()
df_csv = load_csv()

# -----------------------------------------------------
# Patient Selector
# -----------------------------------------------------
patient_ids = df_json["patientId"].tolist()

st.markdown("<h1 style='color:#183153;'>Patient Profile</h1>", unsafe_allow_html=True)
selected_id = st.selectbox("Choose patient", patient_ids)

# -----------------------------------------------------
# Merge JSON + CSV
# -----------------------------------------------------
p_json = df_json[df_json["patientId"] == selected_id].iloc[0]
p_csv = df_csv[df_csv["patientId"] == selected_id].iloc[0] if "patientId" in df_csv.columns else None

# Extract info
name = p_json.get("patientName", selected_id)
age = p_json.get("patientAge", "N/A")
payor = p_json.get("patientPrimaryPayor", "N/A")
risk = p_json.get("patientStabilityConditionRiskScore", "N/A")
ability = p_json.get("patientParticipationAbility", "N/A")
setting = p_json.get("potentialFacilitySetting", "N/A")

# Vitals from CSV
bp_sys = p_csv.get("Systolic Blood Pressure (mmHg)", "N/A") if p_csv is not None else "N/A"
bp_dia = p_csv.get("Diastolic Blood Pressure (mmHg)", "N/A") if p_csv is not None else "N/A"
hr = p_csv.get("Heart rate (/min)", "N/A") if p_csv is not None else "N/A"
glucose = p_csv.get("Glucose (mg/dL)", "N/A") if p_csv is not None else "N/A"
a1c = p_csv.get("Hemoglobin A1C", "N/A") if p_csv is not None else "N/A"
ef = p_csv.get("Left ventricular Ejection fraction (%)", "N/A") if p_csv is not None else "N/A"

# -----------------------------------------------------
# Header Card
# -----------------------------------------------------
st.markdown("<div class='profile-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([0.3, 0.7])

with col1:
    st.image("Logo.png", width=120)

with col2:
    st.markdown(f"<h2 style='margin:0; color:#183153;'>{name}</h2>", unsafe_allow_html=True)
    st.write(f"**Age:** {age}")
    st.write(f"**Primary Payor:** {payor}")
    st.write(f"**Stability Risk:** {risk}")
    st.write(f"**Participation Ability:** {ability}")
    st.write(f"**Recommended Setting:** {setting}")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# Clinical Summary
# -----------------------------------------------------
st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Clinical Summary</div>", unsafe_allow_html=True)

st.write(f"**Age:** {age}")
st.write(f"**Primary Payor:** {payor}")
st.write(f"**Stability Risk:** {risk}")
st.write(f"**Participation Ability:** {ability}")

st.markdown("---")

# -----------------------------------------------------
# Vitals Overview
# -----------------------------------------------------
st.markdown("### Vitals Overview")

st.write(f"- **BP:** {bp_sys}/{bp_dia} mmHg")
st.write(f"- **Heart Rate:** {hr} bpm")
st.write(f"- **Glucose:** {glucose} mg/dL")
st.write(f"- **A1C:** {a1c}%")
st.write(f"- **Ejection Fraction:** {ef}%")

st.markdown("</div>", unsafe_allow_html=True)
