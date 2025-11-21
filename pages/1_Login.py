import streamlit as st
from PIL import Image

st.set_page_config(page_title="RehabAiQ Access Portal", layout="wide")

# --------------------------
# Load Logo
# --------------------------
logo = Image.open("Logo.png")

# --------------------------
# Custom CSS Styling
# --------------------------
page_bg = """
<style>
/* Background Gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f6f7fb 0%, #eef3fa 100%);
}

/* Center Main Content */
.main-container {
    max-width: 900px;
    margin: auto;
    padding-top: 40px;
}

/* Card Style */
.access-card {
    background-color: #ffffff;
    padding: 22px 30px;
    border-radius: 12px;
    border: 1px solid #e7e7e7;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}

.access-card:hover {
    border: 1px solid #3a8ddf;
    transform: scale(1.02);
    box-shadow: 0px 5px 14px rgba(58,141,223,0.25);
}

/* Continue Button */
.continue-btn {
    background-color: #3a8ddf;
    color: white !important;
    padding: 0.6em 1.4em;
    border-radius: 8px;
}

.continue-btn:hover {
    background-color: #276bb0 !important;
}

/* Title styling */
.login-title {
    font-size: 36px;
    font-weight: 700;
    color: #2e466c;
}

.sub-text {
    margin-top: -12px;
    font-size: 17px;
    color: #4b5b73;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# --------------------------
# Layout
# --------------------------

st.image(logo, width=220)

st.markdown(
    """
    <div class="main-container">
        <div class="login-title">RehabAiQ Access Portal</div>
        <div class="sub-text">Select your access type to continue</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.write("")

# Two-column layout for access options
col_admin, col_clin = st.columns(2)

with col_admin:
    admin_box = st.button("🛠️ Administrative Access", key="admin_access", use_container_width=True)
    st.markdown(
        """
        <div style='text-align:center; color:#5a5a5a; margin-top:-10px;'>
            Manage KPIs, configurations, and system dashboards.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_clin:
    clin_box = st.button("🩺 Clinician Access", key="clin_access", use_container_width=True)
    st.markdown(
        """
        <div style='text-align:center; color:#5a5a5a; margin-top:-10px;'>
            Access patients, scores, and rehab recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

# Continue button (bottom-right aligned)
right_col = st.columns([6, 1])[1]
with right_col:
    if st.button("Continue ➜", key="continue", use_container_width=True):
        st.switch_page("pages/2_Patient_Selection.py")
