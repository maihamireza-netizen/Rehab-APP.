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

    fig = go.Figure()

    # Stronger quadrant colors (clean healthcare palette)
    colors = {
        "ALF": "rgba(16,185,129,0.40)",   # Strong Emerald Green
        "ARF": "rgba(59,130,246,0.40)",   # Bright Clinical Blue
        "SNF": "rgba(168,85,247,0.40)",   # Rich Purple
        "ACH": "rgba(239,68,68,0.40)"     # Strong Red
    }

    # Quadrant regions (corrected layout)
    regions = [
        ("SNF", 0, 1, 0, 3),   # Low Ability across all risks
        ("ALF", 1, 2, 0, 1),   # Medium Ability + Low Risk
        ("ARF", 1, 2, 1, 3),   # Medium Ability + Med/High Risk
        ("ALF", 2, 3, 0, 1),   # High Ability + Low Risk
        ("ARF", 2, 3, 1, 2),   # High Ability + Medium Risk
        ("ACH", 2, 3, 2, 3),   # High Ability + High Risk
    ]

    # Add shaded rectangles
    for name, y0, y1, x0, x1 in regions:
        fig.add_shape(
            type="rect",
            x0=x0, x1=x1, y0=y0, y1=y1,
            fillcolor=colors[name],
            line=dict(color="white", width=3),
            layer="below"
        )

    # Scatter plot — enhanced styling
    fig.add_trace(go.Scatter(
        x=df["stability_num"],
        y=df["ability_num"],
        mode="markers",
        marker=dict(
            size=16,
            color="yellow",
            line=dict(color="black", width=2),
            opacity=0.9,
            symbol="circle"
        ),
        text=df["patientid"] if "patientid" in df.columns else df.index,
        hovertemplate="<b>Patient:</b> %{text}<br>Ability: %{y}<br>Stability: %{x}<extra></extra>"
    ))

    # Improved quadrant labels
    labels = {
        "ALF": (0.5, 2.5),
        "ARF": (2.0, 2.5),
        "SNF": (1.0, 0.5),
        "ACH": (2.5, 2.5)
    }

    for lbl, (x, y) in labels.items():
        fig.add_annotation(
            x=x, y=y,
            text=f"<b>{lbl}</b>",
            showarrow=False,
            font=dict(size=28, color="#111", family="Arial Black"),
            opacity=0.9
        )

    # Axes, layout, style
    fig.update_layout(
        xaxis=dict(
            tickvals=[0.5, 1.5, 2.5],
            ticktext=["Low Risk", "Medium Risk", "High Risk"],
            title="<b>Stability Condition Risk</b>",
            range=[0, 3],
            zeroline=False,
            gridcolor="#e5e7eb",
            showgrid=True
        ),
        yaxis=dict(
            tickvals=[0.5, 1.5, 2.5],
            ticktext=["Low Ability", "Medium Ability", "High Ability"],
            title="<b>Participation Ability</b>",
            range=[0, 3],
            zeroline=False,
            gridcolor="#e5e7eb",
            showgrid=True
        ),
        height=700,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)

