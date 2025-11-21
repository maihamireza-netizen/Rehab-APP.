import streamlit as st
import pandas as pd
import json
import plotly.express as px

@st.cache_data
def load_json():
    with open("idx_vw_rehab_recruitment_DEV.json") as f:
        return pd.DataFrame(json.load(f))

df = load_json()

st.markdown("<div class='header-title'>Analytics Dashboard</div>", unsafe_allow_html=True)

st.subheader("Facility Recommendation Breakdown")
st.plotly_chart(px.pie(df, names="potentialFacilitySetting"), use_container_width=True)

st.subheader("Age Distribution")
st.plotly_chart(px.histogram(df, x="patientAge"), use_container_width=True)

st.subheader("Payor Mix")
st.plotly_chart(px.histogram(df, x="patientPrimaryPayor"), use_container_width=True)

