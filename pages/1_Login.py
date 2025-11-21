import streamlit as st
import base64

st.set_page_config(page_title="RehabAiQ Login", layout="wide")

# Background image
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
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")

# Title
st.markdown(
    """
    <h1 style='margin-top:40px; margin-left:40px;'>RehabAiQ Access Portal</h1>
    <p style='margin-left:40px;'>Select your access type to continue</p>
    """,
    unsafe_allow_html=True
)

# Center buttons
st.write("")
st.write("")
col1, col2, col3 = st.columns([1,1,1])

with col2:
    admin = st.button("⚙️ Administrative Access", use_container_width=True)
    clinician = st.button("👩‍⚕️ Clinician Access", use_container_width=True)

# ✔ Modern Streamlit navigation
if admin or clinician:
    st.experimental_set_query_params(page="Patient_Selection")
    st.experimental_rerun()
