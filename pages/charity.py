import os
import uuid

import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_js_eval import get_geolocation

from database import charity_collection
from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Donate Item",
    page_icon="❤️",
    layout="wide"
)

# =====================================
# AUTH
# =====================================

check_role("User")

load_css()
render_sidebar()

# =====================================
# HERO
# =====================================

st.markdown("""
<div class="hero-card">
<h1>❤️ Donate an Item</h1>
<p>
Help your community by donating items you no longer use.
</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# CREATE UPLOAD FOLDER
# =====================================

os.makedirs(
    "uploads",
    exist_ok=True
)

# =====================================
# LOCATION
# =====================================

full_location = "Unknown Location"

latitude = None
longitude = None

location_data = get_geolocation()

if location_data:

    try:

        latitude = location_data["coords"]["latitude"]
        longitude = location_data["coords"]["longitude"]

        geolocator = Nominatim(
            user_agent="exchangia"
        )

        location = geolocator.reverse(
            f"{latitude},{longitude}"
        )

        if location:

            address = location.raw["address"]

            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or "Unknown City"
            )

            state = address.get(
                "state",
                ""
            )

            country = address.get(
                "country",
                ""
            )

            full_location = (
                f"{city}, {state}, {country}"
            )

    except Exception:

        pass

# =====================================
# DONATION FORM
# =====================================

with st.form("donation_form"):

    st.subheader("📦 Donation Details")

    uploaded_file = st.file_uploader(
        "Upload Item Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            width=300
        )

    col1, col2 = st.columns(2)

    with col1:

        category = st.selectbox(
            "Category",
            [
                "Electronics",
                "Books",
                "Clothes",
                "Furniture",
                "Sports",
                "Other"
            ]
        )

    with col2:

        condition = st.selectbox(
            "Condition",
            [
                "New",
                "Like New",
                "Good",
                "Used"
            ]
        )

    custom_category = ""

    if category == "Other":

        custom_category = st.text_input(
            "Custom Category"
        )

    item_name = st.text_input(
        "Item Name"
    )

    description = st.text_area(
        "Description"
    )

    st.subheader("📍 Donation Location")

    st.info(full_location)

    submitted = st.form_submit_button(
        "❤️ Submit Donation",
        use_container_width=True
    )

# =====================================
# SAVE DONATION
# =====================================

if submitted:

    if uploaded_file is None:

        st.error(
            "Please upload an image."
        )

        st.stop()

    if item_name.strip() == "":

        st.error(
            "Item name is required."
        )

        st.stop()

    if category == "Other":

        if custom_category.strip() == "":

            st.error(
                "Please enter custom category."
            )

            st.stop()

        category = custom_category

    extension = uploaded_file.name.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join(
        "uploads",
        filename
    )

    with open(
        filepath,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    charity_collection.insert_one(
        {

            "item_name": item_name,

            "description": description,

            "condition": condition,

            "category": category,

            "image": filepath,

            "location": full_location,

            "latitude": latitude,

            "longitude": longitude,

            "posted_by": st.session_state.username,

            "status": "Pending",

            # future reward system
            "reward_given": False,

            # volunteer pickup
            "picked_up": False,

            # ngo received
            "completed": False,

            "created_at": str(
                st.session_state.get(
                    "login_time",
                    ""
                )
            )

        }
    )

    st.success(
        "🎉 Donation submitted successfully!"
    )

    st.info(
        "Your donation is waiting for admin approval."
    )

    st.balloons()

    st.switch_page(
        "pages/charity_list.py"
    )