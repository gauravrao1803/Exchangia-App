import streamlit as st

from database import volunteer_collection

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Become Volunteer",
    page_icon="🤝",
    layout="wide"
)

# =====================================
# AUTH
# =====================================

check_role("User")

load_css()
render_sidebar()

# =====================================
# HERO SECTION
# =====================================

st.markdown("""
<div class="hero-card">
    <h1>🤝 Become a Volunteer</h1>
    <p>
        Help collect donations and support people in need
        within your community.
    </p>
</div>
""", unsafe_allow_html=True)

username = st.session_state.username

# =====================================
# CHECK EXISTING REQUEST
# =====================================

existing_request = volunteer_collection.find_one(
    {
        "username": username
    }
)

if existing_request:

    status = existing_request.get(
        "status",
        "Pending"
    )

    if status == "Pending":

        st.warning(
            "⏳ Your volunteer application is under review."
        )

    elif status == "Approved":

        st.success(
            "✅ You are already an approved volunteer."
        )

    elif status == "Denied":

        st.error(
            "❌ Your previous application was denied."
        )

    st.stop()

# =====================================
# APPLICATION FORM
# =====================================

with st.form("volunteer_form"):

    st.subheader("Volunteer Information")

    ngo_name = st.text_input(
        "NGO Name"
    )

    requirements = st.text_area(
        "Requirements / Purpose",
        placeholder="Describe the NGO mission and volunteer requirements."
    )

    contact = st.text_input(
        "Contact Number"
    )

    location = st.text_input(
        "Location"
    )

    submitted = st.form_submit_button(
        "🤝 Submit Application",
        use_container_width=True
    )

# =====================================
# SAVE APPLICATION
# =====================================

if submitted:

    if (
        not ngo_name.strip()
        or not requirements.strip()
        or not contact.strip()
        or not location.strip()
    ):

        st.error(
            "Please fill all fields."
        )

    else:

        volunteer_collection.insert_one(
            {
                "username": username,
                "ngo_name": ngo_name,
                "requirements": requirements,
                "contact": contact,
                "location": location,
                "status": "Pending"
            }
        )

        st.success(
            "✅ Volunteer application submitted successfully."
        )

        st.balloons()

        st.rerun()