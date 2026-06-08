import streamlit as st

def load_css():

    st.markdown("""
    <style>

    /* =========================
       GOOGLE FONT
    ========================= */

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    *{
        font-family:'Poppins',sans-serif;
    }

    /* =========================
       MAIN APP
    ========================= */

    .stApp{
        background:#F5F7FB;
    }

    .block-container{
        padding-top:1.5rem;
        padding-bottom:2rem;
        max-width:1400px;
    }

    /* =========================
       TEXT COLORS
    ========================= */

    p,
    span,
    label,
    div{
        color:#111827;
    }

    h1{
        color:#0F172A !important;
        font-weight:700 !important;
    }

    h2,h3,h4,h5{
        color:#1E293B !important;
    }

    /* =========================
       MAIN TITLE
    ========================= */

    .main-title{
        font-size:42px;
        font-weight:700;
        text-align:center;
        color:#2563EB !important;
        margin-bottom:25px;
    }

    /* =========================
       LOGIN / SIGNUP CARD
    ========================= */

    .login-card{
        background:white;
        padding:35px;
        border-radius:20px;
        box-shadow:0px 8px 30px rgba(0,0,0,0.08);
        border:1px solid #E5E7EB;
    }

    /* =========================
       HERO SECTION
    ========================= */

    .hero-card{
        background:linear-gradient(
            135deg,
            #2563EB,
            #1D4ED8
        );

        padding:35px;
        border-radius:22px;

        box-shadow:
        0 8px 30px rgba(37,99,235,.25);

        margin-bottom:25px;
    }

    .hero-card h1{
        color:white !important;
        margin-bottom:10px;
    }

    .hero-card p{
        color:white !important;
        font-size:17px;
    }

    /* =========================
       DASHBOARD CARDS
    ========================= */

    .feature-card{
        background:white;
        padding:25px;
        border-radius:18px;

        border:1px solid #E5E7EB;

        box-shadow:
        0 4px 15px rgba(0,0,0,.08);

        min-height:160px;

        transition:0.3s ease;
    }

    .feature-card:hover{
        transform:translateY(-5px);
        box-shadow:
        0 10px 25px rgba(0,0,0,.15);
    }

    .feature-card h3{
        color:#2563EB !important;
        margin-bottom:10px;
    }

    .feature-card p{
        color:#6B7280 !important;
    }

    /* =========================
       INPUT BOXES
    ========================= */

    .stTextInput input{
        background:white !important;
        color:#111827 !important;

        border:2px solid #D1D5DB !important;

        border-radius:12px !important;

        padding:10px !important;
    }

    .stTextInput input:focus{
        border:2px solid #2563EB !important;
        box-shadow:0 0 0 2px rgba(37,99,235,.20);
    }

    .stTextArea textarea{
        background:white !important;
        color:#111827 !important;

        border:2px solid #D1D5DB !important;

        border-radius:12px !important;
    }

    div[data-baseweb="select"]{
        background:white !important;
        color:#111827 !important;

        border-radius:12px !important;
    }

    /* =========================
       BUTTONS
    ========================= */

    .stButton > button{

        width:100%;

        border:none;

        height:48px;

        border-radius:12px;

        background:#2563EB;

        color:white !important;

        font-weight:600;

        transition:0.3s;
    }

    .stButton > button:hover{

        background:#1D4ED8;

        transform:translateY(-2px);
    }

    /* =========================
       METRICS
    ========================= */

    div[data-testid="stMetric"]{

        background:white;

        border-radius:15px;

        padding:15px;

        border-left:5px solid #2563EB;

        box-shadow:
        0 4px 15px rgba(0,0,0,.08);
    }

    /* =========================
       SIDEBAR
    ========================= */

    section[data-testid="stSidebar"]{

        background:
        linear-gradient(
            180deg,
            #0F172A,
            #1E3A8A
        );
    }

    section[data-testid="stSidebar"] *{

        color:white !important;
    }

    /* =========================
       MARKETPLACE CARDS
    ========================= */

    div[data-testid="stVerticalBlockBorderWrapper"]{

        border-radius:18px !important;

        border:1px solid #E5E7EB !important;

        background:white !important;

        box-shadow:
        0 4px 15px rgba(0,0,0,.08);
    }

    /* =========================
       SUCCESS
    ========================= */

    div[data-testid="stAlert"]{

        border-radius:12px;
    }

    /* =========================
       IMAGE
    ========================= */

    img{
        border-radius:15px;
    }

    /* =========================
       HIDE STREAMLIT MENU
    ========================= */

    #MainMenu{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    header{
        visibility:hidden;
    }

    </style>
    """,
    unsafe_allow_html=True)