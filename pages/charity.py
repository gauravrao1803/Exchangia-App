import streamlit as st
import os
import uuid

from streamlit_js_eval import get_geolocation
from geopy.geocoders import Nominatim

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
# HERO SECTION
# =====================================

st.markdown("""
<div class="hero-card">
    <h1>❤️ Donate an Item</h1>
    <p>
        Give your unused items a second life and help people in need.
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
# LOCATION DETECTION
# =====================================

full_location = "Unknown Location"

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

    except:

        pass

# =====================================
# DONATION FORM
# =====================================

with st.form(
    "charity_form",
    clear_on_submit=False
):

    st.markdown(
        "### 📦 Donation Information"
    )

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
        "Description",
        placeholder="Describe item condition, age, accessories, etc."
    )

    st.markdown("### 📍 Location")

    st.info(full_location)

    submitted = st.form_submit_button(
        "❤️ Post Donation",
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

    elif not item_name.strip():

        st.error(
            "Please enter item name."
        )

    else:

        final_category = category

        if category == "Other":

            if not custom_category.strip():

                st.error(
                    "Please enter custom category."
                )

                st.stop()

            final_category = custom_category

        extension = uploaded_file.name.split(".")[-1]

        unique_filename = (
            f"{uuid.uuid4()}.{extension}"
        )

        file_path = os.path.join(
            "uploads",
            unique_filename
        )

        with open(
            file_path,
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
                "category": final_category,
                "image": file_path,
                "location": full_location,
                "posted_by": st.session_state.username,
                "status": "Pending"
            }
        )

        st.success(
            "✅ Donation submitted successfully. Waiting for admin approval."
        )

        st.balloons()

        st.switch_page(
            "pages/charity_list.py"
        )