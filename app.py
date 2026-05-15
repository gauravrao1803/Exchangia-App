import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title=" welcome to Exchangia App",
    page_icon="📦",
    layout="centered"
)

# ---------------- MAIN PAGE ----------------
st.title("📦welcome to Exchangia App")

st.write("Select an option:")

# Radio Buttons
option = st.radio(
    "Choose Section",
    (
        "Exchange",
        "Charity"
    )
)

# ---------------- NAVIGATION ----------------
if option == "Exchange":

    st.subheader("🔄 Exchange Goods")

    if st.button("Open Exchange Page"):
        st.switch_page("pages/exchange.py")

elif option == "Charity":

    st.subheader("❤️ Charity / Give Away")

    if st.button("Open Charity Page"):
        st.switch_page("pages/charity.py")