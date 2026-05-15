import streamlit as st
import os
from streamlit_js_eval import get_geolocation
import json
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Exchange Goods",
    page_icon="🔄",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("🔄 Exchange Goods")

# ---------------- CREATE UPLOAD FOLDER ----------------
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ======================================================
# 1.1 - POST YOUR GOODS
# ======================================================

st.header("1.1 - Post Your Goods")

# ------------------------------------------------------
# 1.1.1 - Upload Photo
# ------------------------------------------------------
uploaded_file = st.file_uploader(
    "1.1.1 - Upload Photo",
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
# 1.1.2 - Category (Optional)
# ------------------------------------------------------
category = st.selectbox(
    "1.1.2 - Category (Optional)",
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
# 1.1.3 - Browser Live Location
# ------------------------------------------------------
st.subheader("1.1.3 - Device Location")

location_data = get_geolocation()

if location_data:

    latitude = location_data["coords"]["latitude"]
    longitude = location_data["coords"]["longitude"]

    st.success(f"Latitude: {latitude}")
    st.success(f"Longitude: {longitude}")

else:
    st.warning("Please allow browser location permission.")

# ------------------------------------------------------
# 1.1.4 - Post Button
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
        with open("data/exchange_data.json", "r") as file:
            data = json.load(file)

        # Add New Item
        data.append(item_data)

        # Save Updated Data
        with open("data/exchange_data.json", "w") as file:
            json.dump(data, file, indent=4)

        st.success("Goods Posted Successfully ✅")

        # Redirect
        st.switch_page("pages/exchange_list.py")

        # --------------------------------------------------
        # 1.1.5 - Redirect to Main Listing Page
        # --------------------------------------------------
        st.switch_page("pages/exchange_list.py")