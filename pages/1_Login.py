import streamlit as st
import base64

st.set_page_config(page_title="RehabAiQ Login", layout="wide")

# ------------------------------------------------
# SET BACKGROUND IMAGE
# ------------------------------------------------
def set_bg(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# IMPORTANT — your file must be named EXACTLY this:
set_bg("LoginBG.png")

# ------------------------------------------------
# PAGE TITLE
# ------------------------------------------------
st.markdown(
    """
    <h1 style="
        color:#0f172a;
        font-weight:700;
        margin-top:40px;
        margin-left:40px;">
        RehabAiQ Access Portal
    </h1>

    <p style='margin-left:40px; margin-top:-10px; color:#0f172a;'>
        Select your access type to continue
    </p>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# BUTTON CENTERING + STYLING
# ------------------------------------------------
st.markdown(
    """
    <style>
        .center-wrapper {
            position: fixed;
            top: 55%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: row;
            gap: 40px;
            z-index: 1000;
        }

        .access-btn {
            background-color: #4fb7dd;
            color: white !important;
            padding: 15px 34px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            box-shadow: 0px 5px 12px rgba(0,0,0,0.2);
            transition: 0.25s;
        }

        .access-btn:hover {
            background-color: #3aa6c8;
            transform: scale(1.06);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# BUTTONS (No escaped HTML — Correct)
# ------------------------------------------------
st.markdown(
    """
    <div class="center-wrapper">

        <form action="/Patient_Selection">
            <button class="access-btn">⚙️ Administrative Access</button>
        </form>

        <form action="/Patient_Selection">
            <button class="access-btn">👩‍⚕️ Clinician Access</button>
        </form>

    </div>
    """,
    unsafe_allow_html=True
)
