import streamlit as st
import os
import json
from streamlit_js_eval import get_geolocation
from geopy.geocoders import Nominatim

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Exchange Goods",
    page_icon="🔄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0f172a;
    color: white;
}

/* Main Card */
.main-card {
    background-color: #1e293b;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(255,255,255,0.08);
}

/* Title */
.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: white;
}

/* Button */
div.stButton > button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    border: none;
}

/* Inputs */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* Upload */
section[data-testid="stFileUploader"] {
    background-color: #334155;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<p class="title">🔄 Exchange Goods</p>',
    unsafe_allow_html=True
)

# ---------------- CREATE FOLDERS ----------------
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ---------------- MAIN CARD ----------------
with st.container():

    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.subheader("1.1 - Post Your Goods")

    # ------------------------------------------------------
    # Upload Photo
    # ------------------------------------------------------
    uploaded_file = st.file_uploader(
        "📸 Upload Product Photo",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            width=300
        )

    # ------------------------------------------------------
    # Category
    # ------------------------------------------------------
    category = st.selectbox(
        "📦 Select Category",
        [
            "Electronics",
            "Books",
            "Clothes",
            "Furniture",
            "Sports",
            "Other"
        ]
    )

    custom_category = ""

    if category == "Other":

        custom_category = st.text_input(
            "Enter Custom Category"
        )

    # ------------------------------------------------------
    # Live Location
    # ------------------------------------------------------
    st.subheader("📍 Device Location")

    location_data = get_geolocation()

    if location_data:

        latitude = location_data["coords"]["latitude"]
        longitude = location_data["coords"]["longitude"]

        geolocator = Nominatim(
            user_agent="goods_exchange_app"
        )

        location = geolocator.reverse(
            f"{latitude}, {longitude}"
        )

        address = location.raw["address"]

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("county")
            or "Unknown City"
        )

        state = address.get("state")

        country = address.get("country")

        full_location = (
            f"{city}, {state}, {country}"
        )

        st.success(full_location)

    else:

        st.warning(
            "Please allow browser location permission."
        )

    # ------------------------------------------------------
    # Post Button
    # ------------------------------------------------------
    if st.button("🚀 Post Item"):

        if uploaded_file is None:

            st.error("Please upload image.")

        elif not location_data:

            st.error("Location is required.")

        else:

            file_path = os.path.join(
                "uploads",
                uploaded_file.name
            )

            with open(file_path, "wb") as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            final_category = category

            if category == "Other":

                final_category = custom_category

            # Store Data
            item_data = {
                "image": file_path,
                "category": final_category,
                "location": full_location,
                "status": "Pending"
            }

            with open(
                "data/exchange_data.json",
                "r"
            ) as file:

                data = json.load(file)

            data.append(item_data)

            with open(
                "data/exchange_data.json",
                "w"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            st.success(
                "Item Posted Successfully ✅"
            )

            st.switch_page(
                "pages/exchange_list.py"
            )

    st.markdown('</div>', unsafe_allow_html=True)