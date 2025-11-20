import streamlit as st
import pandas as pd
import json
import plotly.express as px

# ------------------------------ PAGE CONFIG ------------------------------
st.set_page_config(
    page_title="RehabAiQ Demo",
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

# ------------------------------ SIDEBAR NAVIGATION ------------------------------
st.sidebar.title("RehabAiQ Navigation")

menu = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Landing Page",
        "🧑‍⚕️ Patient Selection",
        "📋 Patient Profile",
        "🏥 Facility Allocation"
    ]
)

# ------------------------------ PAGE 1: LANDING PAGE ------------------------------
if menu == "🏠 Landing Page":
    st.title("RehabAiQ Platform")
    st.subheader("Smart Rehabilitation Intelligence for Clinical Decision Support")

    st.write(
        """
        Welcome to the RehabAiQ Demo Application.  
        
        Use the sidebar to navigate between:
        - Patient selection  
        - Patient profile  
        - Facility allocation analytics
        """
    )

# ------------------------------ PAGE 2: PATIENT SELECTION ------------------------------
elif menu == "🧑‍⚕️ Patient Selection":
    st.title("🧑‍⚕️ Patient Selection")

    patients = json_df["patientId"].unique().tolist()

    selected = st.multiselect(
        "Select Patient(s):",
        patients,
        placeholder="Choose from patient list"
    )

    if "selected_patients" not in st.session_state:
        st.session_state.selected_patients = []

    st.session_state.selected_patients = selected

    st.info(f"{len(selected)} patient(s) selected")

# ------------------------------ PAGE 3: PATIENT PROFILE ------------------------------
elif menu == "📋 Patient Profile":

    st.title("📋 Patient Profile Viewer")

    if "selected_patients" not in st.session_state or len(st.session_state.selected_patients) == 0:
        st.warning("Please select at least one patient from the Patient Selection page.")
        st.stop()

    patient_id = st.selectbox("Select patient:", st.session_state.selected_patients)

    pdata = json_df[json_df["patientId"] == patient_id].iloc[0]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Demographics")
        st.write(f"**Patient ID:** {pdata['patientId']}")
        st.write(f"**Age:** {pdata['patientAge']}")
        st.write(f"**Primary Payor:** {pdata['patientPrimaryPayor']}")

        st.subheader("Facility Recommendation")
        st.success(f"{pdata['potentialFacilitySetting']}")

        st.subheader("Stability Risk")
        st.info(f"{pdata['patientStabilityConditionRiskScore']}")

    with col2:
        st.subheader("Model Output Summary")
        st.json({
            "Participation Ability": pdata["patientParticipationAbility"],
            "Functional Deficits": pdata["patientFunctionalDeficitsTypes"],
            "Rehab Goals": pdata["patientRehabGoalCategories"]
        })

    st.divider()
    st.write("### Raw Clinical Data (CSV Preview)")
    st.dataframe(csv_df.head(50))

# ------------------------------ PAGE 4: FACILITY ALLOCATION ------------------------------
elif menu == "🏥 Facility Allocation":

    st.title("🏥 Facility Allocation Matrix (Simplified Fast Version)")

    # Convert participation ability → numeric
    ability_map = {
        "High Ability": 3,
        "Medium Ability": 2,
        "Low Ability": 1
    }

    df = json_df.copy()
    df["ability_score"] = df["patientParticipationAbility"].map(lambda x: ability_map.get(x, 1))

    # Convert stability → numeric
    stability_map = {
        "Low Risk": 30,
        "Medium Risk": 60,
        "High Risk": 90
    }
    df["stability_score"] = df["patientStabilityConditionRiskScore"].map(lambda x: stability_map.get(x, 50))

    st.subheader("Adjust Weighting (Interactive)")

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
