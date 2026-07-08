import os
import streamlit as st

from database import (
    charity_collection,
    notification_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css
from utils.ngo_notifications import notify_nearby_ngos
from utils.volunteer_notifications import notify_nearby_volunteers

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Charity Approval",
    page_icon="❤️",
    layout="wide"
)

# ==========================================
# AUTH
# ==========================================

check_role("Admin")

load_css()
render_sidebar()

# ==========================================
# HEADER
# ==========================================

st.title("❤️ Charity Approval Center")

st.caption(
    "Approve or reject donation listings submitted by users."
)

# ==========================================
# DASHBOARD STATS
# ==========================================

total = charity_collection.count_documents({})

pending = charity_collection.count_documents(
    {
        "status": "Pending"
    }
)

approved = charity_collection.count_documents(
    {
        "status": "Approved"
    }
)

rejected = charity_collection.count_documents(
    {
        "status": "Rejected"
    }
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Donations",
    total
)

c2.metric(
    "Pending",
    pending
)

c3.metric(
    "Approved",
    approved
)

c4.metric(
    "Rejected",
    rejected
)

st.divider()

# ==========================================
# SEARCH + FILTER
# ==========================================

col1, col2 = st.columns([3, 1])

with col1:

    search = st.text_input(
        "🔍 Search Category"
    )

with col2:

    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "Pending",
            "Approved",
            "Rejected"
        ]
    )

st.write("")

# ==========================================
# FETCH DATA
# ==========================================

items = charity_collection.find().sort(
    "_id",
    -1
)

# ==========================================
# DISPLAY ITEMS
# ==========================================

for item in items:

    category = item.get(
        "category",
        ""
    )

    if search:

        if search.lower() not in category.lower():

            continue

    if status_filter != "All":

        if item["status"] != status_filter:

            continue

    with st.container(border=True):

        img_col, info_col = st.columns([1, 2])

        # ==================================
        # IMAGE
        # ==================================

        with img_col:

            image_path = item.get("image")

            if image_path and os.path.exists(image_path):

                st.image(
                    image_path,
                    use_container_width=True
                )

            else:

                st.warning(
                    "Image not available"
                )

        # ==================================
        # DETAILS
        # ==================================

        with info_col:

            st.subheader(
                item.get(
                    "item_name",
                    category
                )
            )

            st.write(
                f"**Category:** {category}"
            )

            st.write(
                f"**Condition:** {item.get('condition','N/A')}"
            )

            st.write(
                item.get(
                    "description",
                    ""
                )
            )

            st.write(
                f"📍 {item.get('location','Unknown')}"
            )

            st.write(
                f"👤 Donor : {item['posted_by']}"
            )

            status = item["status"]

            if status == "Pending":

                st.warning(
                    "Pending Approval"
                )

            elif status == "Approved":

                st.success(
                    "Approved"
                )

            else:

                st.error(
                    "Rejected"
                )

            # ==================================
            # ACTION BUTTONS
            # ==================================

            if status == "Pending":

                colA, colB = st.columns(2)

                with colA:

                    if st.button(
                        "✅ Approve",
                        key=f"approve_{item['_id']}",
                        use_container_width=True
                    ):

                        charity_collection.update_one(
                            {
                                "_id": item["_id"]
                            },
                            {
                                "$set":
                                {
                                    "status": "Approved"
                                }
                            }
                        )

                        notification_collection.insert_one(
                            {
                                "username":
                                item["posted_by"],

                                "message":
                                "🎉 Your donation has been approved.",

                                "read":
                                False
                            }
                        )

                        if (
                            item.get("latitude") is not None
                            and
                            item.get("longitude") is not None
                        ):

                            notify_nearby_ngos(item)

                            notify_nearby_volunteers(item)

                        st.success(
                            "Donation Approved Successfully"
                        )

                        st.rerun()

                with colB:

                    if st.button(
                        "❌ Reject",
                        key=f"reject_{item['_id']}",
                        use_container_width=True
                    ):

                        charity_collection.update_one(
                            {
                                "_id": item["_id"]
                            },
                            {
                                "$set":
                                {
                                    "status": "Rejected"
                                }
                            }
                        )

                        notification_collection.insert_one(
                            {
                                "username":
                                item["posted_by"],

                                "message":
                                "❌ Your donation has been rejected.",

                                "read":
                                False
                            }
                        )

                        st.error(
                            "Donation Rejected"
                        )

                        st.rerun()

            st.write("")

            if st.button(
                "🗑 Delete Listing",
                key=f"delete_{item['_id']}",
                use_container_width=True
            ):

                charity_collection.delete_one(
                    {
                        "_id": item["_id"]
                    }
                )

                st.warning(
                    "Listing Deleted"
                )

                st.rerun()