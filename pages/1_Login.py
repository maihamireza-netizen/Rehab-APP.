import streamlit as st
import base64

st.set_page_config(page_title="RehabAiQ Access Portal", layout="wide")

# -----------------------------
# 🔹 Add Background Image
# -----------------------------
def add_bg(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{data}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("pages/background.jpg")

# -----------------------------
# 🔹 Hide the sidebar (optional)
# -----------------------------
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 3rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🔹 ORIGINAL PAGE UI (unchanged)
# -----------------------------

st.title("RehabAiQ Access Portal")
st.write("Select your access type to continue")

col1, col2 = st.columns(2)

with col1:
    st.button("🔧 Administrative Access", key="admin")

with col2:
    st.button("🩺 Clinician Access", key="clin")

st.write("")
st.write("")
st.write("")

# Continue button aligned to the right
st.markdown(
    """
    <div style="text-align:right; padding-right:20px;">
        <a href="/?page=2">
            <button style="
                background-color:#1F7A8C;
                color:white;
                padding:10px 22px;
                border-radius:8px;
                border:none;
                font-size:16px;
            ">Continue →</button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
