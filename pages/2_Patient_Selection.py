import streamlit as st
import pandas as pd
import json
import base64

st.set_page_config(page_title="Patient Selection", layout="wide")

# ------------------------------------
# Background Image Loader
# ------------------------------------
def set_bg(png_file):
    with open(png_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")   # SAME BACKGROUND AS LOGIN PAGE


# --------------------------
# Load Data
# --------------------------
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df = load_json()
patient_list = df["patientId"].tolist()


# --------------------------
# Custom CSS
# --------------------------
st.markdown("""
<style>

.page-card {
    background: rgba(255, 255, 255, 0.80);
    padding: 30px;
    border-radius: 15px;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.page-title {
    font-size: 34px;
    font-weight: 800;
    color: #1f2e4d;
}

.page-subtitle {
    font-size: 18px;
    color: #3d4c63;
    margin-top: -8px;
    margin-bottom: 25px;
}

.btn-green {
    background-color: #2ECC71 !important;
    color: white !important;
    border-radius: 6px;
    padding: 6px 14px;
}

.btn-red {
    background-color: #E74C3C !important;
    color: white !important;
    border-radius: 6px;
    padding: 6px 14px;
}

.continue-btn {
    background-color: #5DADE2 !important;   /* LIGHT BLUE */
    color: white !important;
    padding: 0.75em 1.6em;
    border-radius: 8px;
    font-size: 16px;
}

.continue-btn:hover {
    background-color: #3498DB !important;
}

</style>
""", unsafe_allow_html=True)



# ------------------------------------
# PAGE CONTENT
# ------------------------------------
st.write("")
st.write("")

center = st.columns([0.15, 0.70, 0.15])[1]

with center:
    st.markdown("<div class='page-card'>", unsafe_allow_html=True)

    st.markdown("<div class='page-title'>Patient Selection</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Select one or multiple patients to continue.</div>",
        unsafe_allow_html=True,
    )

    # Selection UI
    col_left, col_right = st.columns([3, 1])

    # -----------------------------------------
    # LEFT SIDE: MULTISELECT
    # -----------------------------------------
    with col_left:
        st.write("**Choose Patients:**")

        if "selected_patients" not in st.session_state:
            st.session_state.selected_patients = []

        selected = st.multiselect(
            "Search or pick patients...",
            options=patient_list,
            default=st.session_state.selected_patients,
            label_visibility="collapsed",
        )

        st.session_state.selected_patients = selected

    # -----------------------------------------
    # RIGHT SIDE: SELECT / DESELECT in ONE ROW
    # -----------------------------------------
    with col_right:
        st.write("**Quick Actions:**")
        b1, b2 = st.columns(2)

        with b1:
            if st.button("Select All", key="select_all", help="Select all patients",
                         type="primary"):
                st.session_state.selected_patients = patient_list
                st.experimental_rerun()

        with b2:
            if st.button("Deselect All", key="deselect_all", help="Clear all patients"):
                st.session_state.selected_patients = []
                st.experimental_rerun()

        # Inject CSS for button colors (Streamlit buttons require after creation)
        st.markdown("""
            <style>
            div[data-testid="column"] div.stButton button[kind="primary"] {
                background-color: #2ECC71 !important;
            }
            div[data-testid="column"] div.stButton:nth-child(2) button {
                background-color: #E74C3C !important;
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------------
    # Continue Button
    # -----------------------------------------
    c = st.columns([0.70, 0.30])[1]
    with c:
        if st.button("Continue ➜", use_container_width=True, key="continue_btn"):
            st.switch_page("pages/3_Patient_Profile.py")

        st.markdown("""
            <style>
            div.stButton > button {
                background-color: #5DADE2 !important; 
                color:white !important; 
                border-radius:8px; 
                padding:0.6em; 
                font-size:16px;
            }
            </style>
        """, unsafe_allow_html=True)


    st.markdown("</div>", unsafe_allow_html=True)
