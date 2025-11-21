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

set_bg("LoginBG.png")

# ------------------------------------------------
# PAGE TITLE (top-left)
# ------------------------------------------------
st.markdown(
    """
    <h1 style="
        color:#0f172a;
        font-weight:700;
        margin-top:40px;
        margin-left:40px;
        position:relative;
        z-index:5;">
        RehabAiQ Access Portal
    </h1>

    <p style="
        margin-left:40px;
        margin-top:-10px;
        font-size:16px;
        color:#0f172a;
        position:relative;
        z-index:5;">
        Select your access type to continue
    </p>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# PERFECT CENTERED BUTTONS (Independent Layer)
# ------------------------------------------------
st.markdown(
    """
    <style>
        /* Absolute centered container */
        .center-wrapper {
            position: fixed;
            top: 58%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: row;
            gap: 50px;
            z-index: 10;
        }

        /* Button style */
        .access-btn {
            background-color: #4fb7dd;
            color: white !important;
            padding: 16px 34px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            box-shadow: 0px 5px 12px rgba(0,0,0,0.25);
            transition: 0.25s ease-in-out;
        }

        .access-btn:hover {
            background-color: #3aa6c8;
            transform: scale(1.05);
        }

        .access-btn:active {
            transform: scale(0.97);
        }
    </style>

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
