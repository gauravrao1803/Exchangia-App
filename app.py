import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Goods Exchange App",
    page_icon="📦",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0f172a;
    color: white;
}

/* Title */
.main-title {
    font-size: 55px;
    font-weight: bold;
    text-align: center;
    color: white;
    margin-top: 20px;
}

/* Subtitle */
.sub-text {
    text-align: center;
    font-size: 20px;
    color: #cbd5e1;
    margin-bottom: 40px;
}

/* Card */
.card {
    background-color: #1e293b;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.1);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.03);
}

/* Buttons */
div.stButton > button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    border: none;
}

/* Radio */
.stRadio label {
    color: white !important;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<p class="main-title">📦 Goods Exchange App</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-text">Exchange goods or donate items to help others</p>',
    unsafe_allow_html=True
)

# ---------------- SECTIONS ----------------
col1, col2 = st.columns(2)

# ======================================================
# EXCHANGE CARD
# ======================================================
with col1:

    st.markdown("""
    <div class="card">
        <h2>🔄 Exchange Goods</h2>
        <p>
            Exchange your unused products with nearby users.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("Open Exchange Section"):

        st.switch_page("pages/exchange.py")

# ======================================================
# CHARITY CARD
# ======================================================
with col2:

    st.markdown("""
    <div class="card">
        <h2>❤️ Charity / Give Away</h2>
        <p>
            Donate items to people who really need them.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("Open Charity Section"):

        st.switch_page("pages/charity.py")

# ---------------- FOOTER ----------------
st.write("")
st.write("")
st.markdown(
    "<center>Stay Connected with us And Helps others ❤️ </center>",
    unsafe_allow_html=True
)