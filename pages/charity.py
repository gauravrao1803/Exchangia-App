import streamlit as st
import os
from streamlit_js_eval import get_geolocation
import json
from geopy.geocoders import Nominatim
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Charity Goods",
    page_icon="❤️",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("❤️ Charity / Give Away")

# ---------------- CREATE UPLOAD FOLDER ----------------
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ======================================================
# 2.1 - GIVE AWAY GOODS
# ======================================================

st.header("2.1 - Give Away Goods")

# ------------------------------------------------------
# 2.1.1 - Upload Photo
# ------------------------------------------------------
uploaded_file = st.file_uploader(
    "2.1.1 - Upload Photo",
    type=["jpg", "jpeg", "png"]
)

# Preview Image
if uploaded_file:
    st.image(
        uploaded_file,
        caption="Uploaded Product Image",
        width=250
    )

# ------------------------------------------------------
# 2.1.2 - Category (Optional)
# ------------------------------------------------------
category = st.selectbox(
    "2.1.2 - Category (Optional)",
    [
        "Electronics",
        "Books",
        "Clothes",
        "Furniture",
        "Sports",
        "Other"
    ]
)

# If Other selected
custom_category = ""

if category == "Other":

    custom_category = st.text_input(
        "Enter Custom Category"
    )

# ------------------------------------------------------
# 2.1.3 - Browser Live Location
# ------------------------------------------------------

# ------------------------------------------------------
# 1.1.3 - Browser Live Location
# ------------------------------------------------------
st.subheader("Device Location")

location_data = get_geolocation()

if location_data:

    # Coordinates
    latitude = location_data["coords"]["latitude"]
    longitude = location_data["coords"]["longitude"]

    # Reverse Geocoding
    geolocator = Nominatim(
        user_agent="goods_exchange_app"
    )

    location = geolocator.reverse(
        f"{latitude}, {longitude}"
    )

    # Address Data
    address = location.raw["address"]

    # Better City Detection
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
        or address.get("county")
        or "Unknown City"
    )

    # State & Country
    state = address.get(
        "state",
        "Unknown State"
    )

    country = address.get(
        "country",
        "Unknown Country"
    )

    # Final Location
    full_location = (
        f"{city}, {state}, {country}"
    )

    # Show Location
    st.success(full_location)

else:

    st.warning(
        "Please allow browser location permission."
    )

# ------------------------------------------------------
# 2.1.4 - Post Button
# ------------------------------------------------------
if st.button("Post"):

    if uploaded_file is None:
        st.error("Please upload a photo.")

    elif not location_data:
        st.error("Location is required.")

    else:

        # Save Uploaded Image
        file_path = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # Final Category
        final_category = category

        if category == "Other":
            final_category = custom_category

        # Store Data
        item_data = {
            "image": file_path,
            "category": final_category,
            "latitude": latitude,
            "longitude": longitude
        }

        # Read Existing Data
        with open("data/charity_data.json", "r") as file:
            data = json.load(file)

        # Add New Item
        data.append(item_data)

        # Save Updated Data
        with open("data/charity_data.json", "w") as file:
            json.dump(data, file, indent=4)

        st.success("Charity Item Posted Successfully ✅")

        # Redirect
        st.switch_page("pages/charity_list.py")

        # --------------------------------------------------
        # 2.1.5 - Redirect to Charity Listing Page
        # --------------------------------------------------
        st.switch_page("pages/charity_list.py")