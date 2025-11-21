import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

st.set_page_config(page_title="Facility Allocation", layout="wide")

# -------------------------
# Load JSON Data
# -------------------------
@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df = load_json()

# Ensure categories are ordered
ability_order = ["Low Ability", "Medium Ability", "High Ability"]
stability_order = ["Low Risk", "Medium Risk", "High Risk"]

df["patientParticipationAbility"] = pd.Categorical(df["patientParticipationAbility"], categories=ability_order, ordered=True)
df["patientStabilityConditionRiskScore"] = pd.Categorical(df["patientStabilityConditionRiskScore"], categories=stability_order, ordered=True)

# NUMERIC mapping for plotting
ability_map = {"Low Ability": 0.5, "Medium Ability": 1.5, "High Ability": 2.5}
stability_map = {"Low Risk": 0.5, "Medium Risk": 1.5, "High Risk": 2.5}

df["ability_num"] = df["patientParticipationAbility"].map(ability_map)
df["stability_num"] = df["patientStabilityConditionRiskScore"].map(stability_map)

# -------------------------
# Layout
# -------------------------
st.markdown("<h1 style='margin-bottom:0px;'>🏥 Facility Allocation</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top:0px;'>Interactive mock sliders + real patient allocation matrix.</p>", unsafe_allow_html=True)

left, right = st.columns([0.40, 0.60])

# -------------------------
# LEFT COLUMN (Mock UI)
# -------------------------
with left:
    st.markdown("""
    <div style="padding:12px; background-color:#f9fafc; border-radius:10px; border:1px solid #e5e7eb;">
    <h3 style="color:#1F2937; margin-top:0px;">⚙️ Allocation Model Settings (Mock)</h3>
    <p style="color:#6b7280;">These controls are placeholders and do not affect model output.</p>
    </div>
    """, unsafe_allow_html=True)

    # Cardiovascular
    with st.expander("❤️ Cardiovascular KPI Thresholds", expanded=True):
        st.number_input("Systolic BP Threshold", 90, 200, 170)
        st.number_input("Diastolic BP Threshold", 50, 120, 90)
        st.number_input("Heart Rate Threshold", 40, 200, 110)
        st.number_input("Ejection Fraction Threshold", 10, 80, 40)

        st.slider("Priority Weight (Cardio)", 1, 10, 5)

    # Diabetes
    with st.expander("🩸 Diabetes KPI Thresholds", expanded=True):
        st.number_input("Glucose Threshold", 50, 400, 200)
        st.number_input("Hemoglobin A1C Threshold", 4, 15, 9)
        st.slider("Priority Weight (Diabetes)", 1, 10, 5)

    # Neurological
    with st.expander("🧠 Neurological Factors", expanded=True):
        st.checkbox("Indicate Stroke History")
        st.slider("Priority Weight (Neuro)", 1, 10, 5)

    # Participation Ability
    with st.expander("🏃 Participation Ability Factors", expanded=True):
        st.checkbox("Physical Limitation")
        st.checkbox("Cognitive Impairment")
        st.checkbox("Behavioral Challenges")
        st.slider("Priority Weight (Participation)", 1, 10, 5)


# -------------------------
# RIGHT COLUMN (REAL MATRIX)
# -------------------------
with right:
    st.markdown("<h3 style='margin-top:0px;'>📊 Facility Allocation Matrix</h3>", unsafe_allow_html=True)

    # Quadrant shading
    fig = go.Figure()

    # Create shaded background regions
    colors = {
        "ALF": "rgba(34,197,94,0.25)",   # green
        "ARF": "rgba(59,130,246,0.25)",  # blue
        "SNF": "rgba(168,85,247,0.25)",  # purple
        "ACH": "rgba(239,68,68,0.25)"    # red
    }

    # Quadrant grid coordinates
    regions = [
        ("ALF", 1, 3, 1, 2),   # Medium/High Ability + Low Risk
        ("ARF", 1, 3, 2, 3),   # Medium/High Ability + Medium/High Risk
        ("SNF", 0, 1, 0, 3),   # Low Ability across all risks
        ("ACH", 2, 3, 2, 3),   # High Risk + High Ability
    ]

    for name, y0, y1, x0, x1 in regions:
        fig.add_shape(
            type="rect",
            x0=x0, x1=x1,
            y0=y0, y1=y1,
            fillcolor=colors[name],
            line=dict(width=0),
            layer="below"
        )

    # Scatter plot of patients
    fig.add_trace(go.Scatter(
        x=df["stability_num"],
        y=df["ability_num"],
        mode="markers",
        marker=dict(size=12, color="yellow", line=dict(color="black", width=1)),
        text=df["patientid"] if "patientid" in df.columns else df.index,
        hovertemplate="<b>Patient:</b> %{text}<br>Ability: %{y}<br>Stability: %{x}<extra></extra>"
    ))

    # Add quadrant labels
    labels = {
        "ALF": (0.5, 2.5),
        "ARF": (2.0, 2.5),
        "SNF": (1.0, 0.5),
        "ACH": (2.5, 2.5)
    }

    for lbl, (x, y) in labels.items():
        fig.add_annotation(
            x=x,
            y=y,
            text=f"<b>{lbl}</b>",
            showarrow=False,
            font=dict(size=22, color="#111"),
            opacity=0.8
        )

    fig.update_layout(
        xaxis=dict(
            tickvals=[0.5, 1.5, 2.5],
            ticktext=["Low Risk", "Medium Risk", "High Risk"],
            title="Stability Condition Risk",
            range=[0, 3]
        ),
        yaxis=dict(
            tickvals=[0.5, 1.5, 2.5],
            ticktext=["Low Ability", "Medium Ability", "High Ability"],
            title="Participation Ability",
            range=[0, 3]
        ),
        height=650,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)
