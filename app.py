import streamlit as st
import pandas as pd
import json
import plotly.express as px

# ------------------------------ PAGE CONFIG ------------------------------
st.set_page_config(
    page_title="RehabAiQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------ LOAD DATA ------------------------------
@st.cache_data
def load_csv():
    return pd.read_csv("merged_data_RehabAiQ_Demo.csv")

@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        data = json.load(f)
    return pd.DataFrame(data)

csv_df = load_csv()
json_df = load_json()

# ------------------------------ GLOBAL CSS STYLING ------------------------------
st.markdown(
    """
    <style>
        /* Global font and color palette */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Header style */
        .header-title {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: #1A3C7C;
            padding-top: 10px;
            padding-bottom: 5px;
        }

        .subheader {
            font-size: 18px !important;
            color: #5A5A5A;
            padding-bottom: 0px;
        }

        /* Card container */
        .card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 20px;
        }

        /* KPI Card */
        .kpi-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }

        /* Badge */
        .badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 10px;
            font-size: 14px;
            color: white;
            font-weight: 600;
        }

        .risk-low { background-color: #2ECC71; }
        .risk-medium { background-color: #F1C40F; }
        .risk-high { background-color: #E74C3C; }

        .payor-badge {
            background-color: #3498DB;
        }

        /* Section Divider */
        .section-title {
            font-size: 22px;
            font-weight: 600;
            color: #1A3C7C;
            margin-top: 20px;
            margin-bottom: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------ SIDEBAR ------------------------------
st.sidebar.image("Logo.png", use_container_width=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Landing Page",
        "🧑‍⚕️ Patient Selection",
        "📋 Patient Profile",
        "🏥 Facility Allocation",
        "📊 Analytics Dashboard"
    ]
)
# Auto-navigation after clicking Continue
if "force_menu_switch" in st.session_state:
    menu = st.session_state["force_menu_switch"]
    del st.session_state["force_menu_switch"]


# ------------------------------ PAGE 1: LANDING PAGE ------------------------------
if menu == "🏠 Landing Page":

    # Title
    st.markdown("<div class='header-title'>RehabAiQ Access Portal</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subheader'>Select your access type to continue</div>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.write("## Choose Access Type")

    # Initialize session state
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

    colA, colB = st.columns([1, 1])

    # ------------------- ADMINISTRATIVE ACCESS -------------------
    with colA:
        if st.button("🛠️  Administrative Access", use_container_width=True):
            st.session_state.user_role = "Administrative"

        st.markdown(
            """
            <div style="
                background-color: #ffffff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.07);
                margin-top: 10px;
            ">
                Manage system settings, organizational KPIs, reports, and global configuration.
            </div>
            """,
            unsafe_allow_html=True
        )

    # ------------------- CLINICIAN ACCESS -------------------
    with colB:
        if st.button("🧑‍⚕️  Clinician Access", use_container_width=True):
            st.session_state.user_role = "Clinician"

        st.markdown(
            """
            <div style="
                background-color: #ffffff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.07);
                margin-top: 10px;
            ">
                Access patient data, risk scores, rehabilitation recommendations, and insights.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ------------------- CONTINUE BUTTON -------------------
    cont_col = st.columns([6, 1])

    with cont_col[1]:
        if st.session_state.user_role:
            if st.button("Continue ➜", use_container_width=True):
                st.session_state["force_menu_switch"] = "🧑‍⚕️ Patient Selection"
                st.experimental_rerun()
        else:
            st.button("Continue ➜", disabled=True, use_container_width=True)


# ------------------------------ PAGE 3: PATIENT PROFILE ------------------------------
elif menu == "📋 Patient Profile":

    if "selected_patients" not in st.session_state or len(st.session_state.selected_patients) == 0:
        st.error("Please select patients first.")
        st.stop()

    patient_id = st.selectbox("Select Patient:", st.session_state.selected_patients)
    pdata = json_df[json_df["patientId"] == patient_id].iloc[0]

    st.markdown("<div class='header-title'>Patient Profile</div>", unsafe_allow_html=True)

    # COLUMN LAYOUT
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Demographics")
        st.write(f"**Patient ID:** {pdata['patientId']}")
        st.write(f"**Age:** {pdata['patientAge']}")
        st.write(f"**Primary Payor:** {pdata['patientPrimaryPayor']}")
        st.write(f"**Stability Risk:** {pdata['patientStabilityConditionRiskScore']}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Rehab Information")
        st.write(f"**Participation Ability:** {pdata['patientParticipationAbility']}")
        st.write(f"**Facility Recommendation:** {pdata['potentialFacilitySetting']}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Additional Clinical Data")
    st.dataframe(csv_df.head(50))

# ------------------------------ PAGE 4: FACILITY ALLOCATION ------------------------------
elif menu == "🏥 Facility Allocation":

    st.markdown("<div class='header-title'>Intelligent Facility Allocation</div>", unsafe_allow_html=True)

    # Mapping
    ability_map = {"High Ability": 3, "Medium Ability": 2, "Low Ability": 1}
    stability_map = {"Low Risk": 30, "Medium Risk": 60, "High Risk": 90}

    df = json_df.copy()
    df["ability_score"] = df["patientParticipationAbility"].map(ability_map)
    df["stability_score"] = df["patientStabilityConditionRiskScore"].map(stability_map)

    st.subheader("Weight Adjustments")
    ability_w = st.slider("Participation Weight", 0.0, 1.0, 0.5)
    stability_w = 1 - ability_w

    df["adj_ability"] = df["ability_score"] * ability_w
    df["adj_stability"] = df["stability_score"] * stability_w

    st.caption(f"Stability Weight = {stability_w:.2f}")

    st.subheader("Allocation Matrix")

    fig = px.scatter(
        df,
        x="adj_stability",
        y="adj_ability",
        color="potentialFacilitySetting",
        hover_name="patientId",
        labels={
            "adj_stability": "Stability (weighted)",
            "adj_ability": "Ability (weighted)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------ PAGE 5: ANALYTICS DASHBOARD ------------------------------
elif menu == "📊 Analytics Dashboard":

    st.markdown("<div class='header-title'>Analytics Dashboard</div>", unsafe_allow_html=True)

    st.subheader("Patient Distribution by Facility Recommendation")
    fig1 = px.pie(json_df, names="potentialFacilitySetting")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Age Distribution")
    fig2 = px.histogram(json_df, x="patientAge", nbins=10)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Payor Mix")
    fig3 = px.histogram(json_df, x="patientPrimaryPayor")
    st.plotly_chart(fig3, use_container_width=True)
