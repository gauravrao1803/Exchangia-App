# import streamlit as st
# import os

# from database import charity_collection

# from utils.auth import check_login
# from utils.styles import load_css
# from utils.sidebar import sidebar_menu

# # ---------------- AUTH ----------------
# check_login()

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="Charity Listings",
#     page_icon="❤️",
#     layout="wide"
# )

# # ---------------- LOAD CSS ----------------
# load_css()

# # ---------------- SIDEBAR ----------------
# sidebar_menu()

# # ---------------- TITLE ----------------
# st.markdown(
#     '<p class="main-title">❤️ Charity Listings</p>',
#     unsafe_allow_html=True
# )

# # ---------------- FETCH ITEMS ----------------
# items = list(
#     charity_collection.find()
# )

# # ---------------- SHOW ITEMS ----------------
# for item in items:

#     st.markdown(
#         '<div class="card">',
#         unsafe_allow_html=True
#     )

#     col1, col2 = st.columns([1, 2])

#     with col1:

#         if os.path.exists(item["image"]):

#             st.image(
#                 item["image"],
#                 width=250
#             )

#         else:

#             st.warning(
#                 "Image not found"
#             )

#     with col2:

#         st.subheader(
#             item["category"]
#         )

#         st.write(
#             f"📍 {item['location']}"
#         )

#         st.write(
#             f"👤 Posted By: {item['posted_by']}"
#         )

#         if item["status"] == "Approved":

#             st.success(
#                 "Approved ✅"
#             )

#         elif item["status"] == "Denied":

#             st.error(
#                 "Denied ❌"
#             )

#         else:

#             st.warning(
#                 "Pending ⏳"
#             )

#     st.markdown(
#         '</div>',
#         unsafe_allow_html=True
#     )


#new flow

from utils.sidebar import render_sidebar
from utils.styles import load_css
from utils.auth import check_role

check_role("User")
load_css()
render_sidebar()
import streamlit as st

from database import (
    charity_collection,
    charity_requests_collection
)

from utils.auth import check_login
from utils.notifications import create_notification

check_login()

st.title("❤️ Charity Listings")

# ======================================================
# FETCH ALL ITEMS
# ======================================================

items = charity_collection.find()

for item in items:

    st.markdown("---")

    # ======================================================
    # IMAGE
    # ======================================================

    try:

        st.image(
            item["image"],
            width=250
        )

    except:

        st.warning("Image not found")

    # ======================================================
    # ITEM DETAILS
    # ======================================================

    st.subheader(
        item["category"]
    )

    st.write(
        f"📍 {item['location']}"
    )

    st.write(
        f"👤 Donor: {item['posted_by']}"
    )

    # ======================================================
    # STATUS
    # ======================================================

    if item["status"] == "Pending":

        st.warning(
            "⏳ Status: Pending Approval"
        )

    elif item["status"] == "Approved":

        st.success(
            "✅ Status: Approved"
        )

    elif item["status"] == "Rejected":

        st.error(
            "❌ Status: Rejected"
        )

    # ======================================================
    # ONLY VOLUNTEER + APPROVED
    # ======================================================

    if (
        st.session_state.role == "Volunteer"
        and item["status"] == "Approved"
    ):

        existing = charity_requests_collection.find_one(
            {
                "charity_id": str(item["_id"]),
                "volunteer": st.session_state.username
            }
        )

        # ======================================================
        # EXISTING REQUEST
        # ======================================================

        if existing:

            if existing["status"] == "Pending":

                st.warning(
                    "⏳ Donation Request Pending"
                )

            elif existing["status"] == "Accepted":

                st.success(
                    "✅ Donation Request Accepted"
                )

            elif existing["status"] == "Rejected":

                st.error(
                    "❌ Donation Request Rejected"
                )

            elif existing["status"] == "Completed":

                st.success(
                    "✔ Donation Collected"
                )

        else:

            # ======================================================
            # ACCEPT DONATION
            # ======================================================

            if st.button(
                "❤️ Accept Donation",
                key=str(item["_id"])
            ):

                request_data = {

                    "charity_id": str(item["_id"]),

                    "donor": item["posted_by"],

                    "volunteer": st.session_state.username,

                    "item_name": item["category"],

                    "status": "Pending"
                }

                charity_requests_collection.insert_one(
                    request_data
                )

                # ======================================================
                # NOTIFICATION
                # ======================================================

                create_notification(
                    item["posted_by"],
                    f"{st.session_state.username} wants to collect your donation."
                )

                st.success(
                    "Donation Request Sent Successfully"
                )