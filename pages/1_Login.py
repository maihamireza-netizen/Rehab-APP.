import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="RehabAiQ Login", layout="wide")

# ------------------------------------------------
# BACKGROUND IMAGE
# ------------------------------------------------
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
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("LoginBG.png")

# ------------------------------------------------
# TITLE
# ------------------------------------------------
st.markdown(
    """
    <h1 style="color:#0f172a; font-weight:700; margin-top:40px; margin-left:40px;">
        RehabAiQ Access Portal
    </h1>

    <p style="margin-left:40px; margin-top:-10px; color:#0f172a;">
        Select your access type to continue
    </p>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# PERFECTLY CENTERED BUTTONS (via st.components.html)
# ------------------------------------------------

html_code = """
<html>
<head>
<style>
.center-wrapper {
    position: fixed;
    top: 55%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    gap: 40px;
    z-index: 9999;
}

.btn {
    background-color: #4fb7dd;
    color: white;
    padding: 16px 34px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.25);
    transition: 0.25s;
}

.btn:hover {
    background-color: #3aa6c8;
    transform: scale(1.06);
}
</style>
</head>

<body>

<div class="center-wrapper">

    <form action="/Patient_Selection">
        <button class="btn">⚙️ Administrative Access</button>
    </form>

    <form action="/Patient_Selection">
        <button class="btn">👩‍⚕️ Clinician Access</button>
    </form>

</div>

</body>
</html>
"""

components.html(html_code, height=500)
