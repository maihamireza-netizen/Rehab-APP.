import streamlit as st
import base64

st.set_page_config(page_title="RehabAiQ Access Portal", layout="wide")

# -----------------------------
# Add Background Image
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
# PAGE CONTENT
# -----------------------------

# Title (kept the same)
st.markdown("""
<div style="margin-top: 30px; padding-left: 10px;">
    <h1 style="color:#0a2b33;">RehabAiQ Access Portal</h1>
    <p style="font-size:18px; color:#0a2b33;">Select your access type to continue</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------
# CENTER BUTTONS
# -----------------------------
center = st.container()
with center:
    colA, colB, colC = st.columns([2, 1, 2])   # center col wider

    with colB:
        st.button("🔧 Administrative Access", key="admin", use_container_width=True)
        st.write("")
        st.button("🩺 Clinician Access", key="clin", use_container_width=True)

# Spacing
st.write("")
st.write("")


# -----------------------------
# CONTINUE BUTTON (RIGHT SIDE)
# -----------------------------
st.markdown("""
<div style="text-align:right; padding-right:40px; margin-top:20px;">
    <a href="/?page=2">
        <button style="
            background-color:#0c6e7f;
            color:white;
            padding:10px 22px;
            border-radius:8px;
            border:none;
            font-size:16px;
        ">Continue →</button>
    </a>
</div>
""", unsafe_allow_html=True)
