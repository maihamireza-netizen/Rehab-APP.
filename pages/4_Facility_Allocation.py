import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Facility Allocation", layout="wide")

# -------------------------
# Load JSON Data
# -------------------------
@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df = load_json()

# Ensure correct patient name column
df["patientName"] = df["patientName"].astype(str)

# Ordered clinical categories
ability_order = ["Low Ability", "Medium Ability", "High Ability"]
stability_order = ["Low Risk", "Medium Risk", "High Risk"]

df["patientParticipationAbility"] = pd.Categorical(
    df["patientParticipationAbility"], categories=ability_order, ordered=True
)
df["patientStabilityConditionRiskScore"] = pd.Categorical(
    df["patientStabilityConditionRiskScore"], categories=stability_order, ordered=True
)

ability_map = {"Low Ability": 0.5, "Medium Ability": 1.5, "High Ability": 2.5}
stability_map = {"Low Risk": 0.5, "Medium Risk": 1.5, "High Risk": 2.5}

df["ability_num"] = df["patientParticipationAbility"].map(ability_map)
df["stability_num"] = df["patientStabilityConditionRiskScore"].map(stability_map)

df["label"] = df["patientName"]  # use full patient name everywhere

# -------------------------
# Page Header
# -------------------------
st.markdown("<h1 style='margin-bottom:0px;'>🏥 Facility Allocation</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top:0px;'>Mock KPI sliders + dynamic visualization of patient placement.</p>", unsafe_allow_html=True)

left, right = st.columns([0.45, 0.55])

# -------------------------
# LEFT COLUMN — KPI CONTROLS
# -------------------------
with left:
    st.markdown("""
        <div style="padding:12px; background-color:#f9fafc; border-radius:10px; border:1px solid #e5e7eb;">
        <h3 style="color:#1F2937; margin-top:0px;">⚙️ Allocation Model Settings (Mock)</h3>
        <p style="color:#6b7280;">These sliders visually reorganize the matrix but do not run the real model.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### ❤️ Cardiovascular KPI Weights")
    cardio_w1 = st.slider("Priority Weight — Systolic BP", 1, 10, 5)
    cardio_w2 = st.slider("Priority Weight — Diastolic BP", 1, 10, 5)
    cardio_w3 = st.slider("Priority Weight — Heart Rate", 1, 10, 5)
    cardio_w4 = st.slider("Priority Weight — Ejection Fraction", 1, 10, 5)

    st.markdown("### 🩸 Diabetes KPI Weights")
    diab_w1 = st.slider("Priority Weight — Glucose", 1, 10, 5)
    diab_w2 = st.slider("Priority Weight — Hemoglobin A1C", 1, 10, 5)

    st.markdown("### 🧠 Neurological Weight")
    neuro_w = st.slider("Priority Weight — Stroke Risk", 1, 10, 5)

    st.markdown("### 🏃 Participation Ability Weights")
    part_w1 = st.slider("Priority Weight — Cognitive Impairment", 1, 10, 5)
    part_w2 = st.slider("Priority Weight — Physical Limitation", 1, 10, 5)
    part_w3 = st.slider("Priority Weight — Behavioral Challenges", 1, 10, 5)
    part_w4 = st.slider("Priority Weight — Lifestyle Limitation", 1, 10, 5)

    # Combine slider values to apply jitter
    total_weight = (
        cardio_w1 + cardio_w2 + cardio_w3 + cardio_w4 +
        diab_w1 + diab_w2 + neuro_w +
        part_w1 + part_w2 + part_w3 + part_w4
    )

    noise_strength = total_weight / 300
    np.random.seed(42)

    df["ability_perturbed"] = df["ability_num"] + np.random.uniform(-noise_strength, noise_strength, len(df))
    df["stability_perturbed"] = df["stability_num"] + np.random.uniform(-noise_strength, noise_strength, len(df))


# -------------------------
# RIGHT COLUMN — MATRIX + SUMMARY + TABLE
# -------------------------
with right:

    # ---------------------------------------------
    # FACILITY SUMMARY
    # ---------------------------------------------
    st.markdown("### 📌 Facility Summary")

    def assign_facility(a, s):
        if a < 1:  # Low Ability → always SNF
            return "SNF"
        if a < 2 and s < 1:
            return "ALF"
        if a < 2 and s >= 1:
            return "ARF"
        if a >= 2 and s < 1:
            return "ALF"
        if a >= 2 and s < 2:
            return "ARF"
        return "ACH"

    df["Assigned Facility"] = df.apply(
        lambda x: assign_facility(x["ability_perturbed"], x["stability_perturbed"]),
        axis=1
    )

    facility_counts = df["Assigned Facility"].value_counts().reindex(["SNF", "ALF", "ARF", "ACH"]).fillna(0)
    total = len(df)

    snf, alf, arf, ach = facility_counts["SNF"], facility_counts["ALF"], facility_counts["ARF"], facility_counts["ACH"]

    colA, colB, colC, colD = st.columns(4)
    colA.metric("🏥 SNF", f"{snf}", f"{(snf/total)*100:.1f}%")
    colB.metric("🏡 ALF", f"{alf}", f"{(alf/total)*100:.1f}%")
    colC.metric("🛏 ARF", f"{arf}", f"{(arf/total)*100:.1f}%")
    colD.metric("🏨 ACH", f"{ach}", f"{(ach/total)*100:.1f}%")


    # ---------------------------------------------
    # ALLOCATION MATRIX
    # ---------------------------------------------
    st.markdown("### 📊 Allocation Matrix")

    quadrant_colors = {
        "ALF": "rgba(0,200,83,0.35)",
        "ARF": "rgba(30,144,255,0.35)",
        "SNF": "rgba(147,51,234,0.35)",
        "ACH": "rgba(255,48,48,0.35)"
    }

    regions = [
        ("SNF", 0, 1, 0, 3),
        ("ALF", 1, 2, 0, 1),
        ("ARF", 1, 2, 1, 3),
        ("ALF", 2, 3, 0, 1),
        ("ARF", 2, 3, 1, 2),
        ("ACH", 2, 3, 2, 3),
    ]

    fig = go.Figure()

    for name, y0, y1, x0, x1 in regions:
        fig.add_shape(
            type="rect",
            x0=x0, x1=x1,
            y0=y0, y1=y1,
            fillcolor=quadrant_colors[name],
            line=dict(width=2, color="white"),
            layer="below"
        )

    fig.add_trace(go.Scatter(
        x=df["stability_perturbed"],
        y=df["ability_perturbed"],
        mode="markers+text",
        marker=dict(size=14, color="yellow", line=dict(color="black", width=1)),
        text=df["patientName"],
        textposition="top center",
        hovertemplate="<b>%{text}</b><br>Ability: %{y:.2f}<br>Stability: %{x:.2f}<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(
            tickvals=[0.5, 1.5, 2.5],
            ticktext=["Low Risk", "Medium Risk", "High Risk"],
            title="<b>Stability Condition Risk</b>",
            range=[0, 3]
        ),
        yaxis=dict(
            tickvals=[0.5, 1.5, 2.5],
            ticktext=["Low Ability", "Medium Ability", "High Ability"],
            title="<b>Participation Ability</b>",
            range=[0, 3]
        ),
        height=650,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)


    # ---------------------------------------------
    # PATIENT ALLOCATION TABLE
    # ---------------------------------------------
    st.markdown("### 📋 Patient Allocation Table")

    allocation_df = df[[
        "patientName",
        "patientParticipationAbility",
        "patientStabilityConditionRiskScore",
        "Assigned Facility"
    ]].sort_values("Assigned Facility")

    st.dataframe(allocation_df, use_container_width=True)


    # ---------------------------------------------
    # CLICK-TO-OPEN PATIENT PROFILE (Option A)
    # ---------------------------------------------
    st.markdown("### 👉 Open Patient Profile")

    for idx, row in allocation_df.iterrows():
        if st.button(f"Open {row['patientName']}", key=f"open_{idx}"):
            st.session_state.selected_patient = row["patientName"]
            st.switch_page("pages/3_Patient_Profile.py")
