import streamlit as st

st.markdown("<div class='header-title'>RehabAiQ Access Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Select your access type to continue</div>", unsafe_allow_html=True)
st.markdown("---")

# Initialize role
if "user_role" not in st.session_state:
    st.session_state.user_role = None

colA, colB = st.columns(2)

# ------------------- ADMIN ACCESS -------------------
with colA:
    if st.button("🛠️ Administrative Access", use_container_width=True):
        st.session_state.user_role = "Admin"
    st.markdown(
        """
        <div class='card'>
            Manage KPIs, settings, and system-wide dashboards.
        </div>
        """, unsafe_allow_html=True
    )

# ------------------- CLINICIAN ACCESS -------------------
with colB:
    if st.button("🧑‍⚕️ Clinician Access", use_container_width=True):
        st.session_state.user_role = "Clinician"
    st.markdown(
        """
        <div class='card'>
            Access patients, risk scores, and rehab recommendations.
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")

# Continue button
cols = st.columns([6, 1])
with cols[1]:
    if st.session_state.user_role:
        if st.button("Continue ➜", use_container_width=True):
            st.switch_page("pages/2_Patient_Selection.py")
    else:
        st.button("Continue ➜", disabled=True, use_container_width=True)
