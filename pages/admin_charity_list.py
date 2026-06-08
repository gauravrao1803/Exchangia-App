import streamlit as st
import os

from database import (
    charity_collection,
    notification_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# ==========================================
# AUTH
# ==========================================

check_role("Admin")

st.set_page_config(
    page_title="Charity Approval",
    page_icon="❤️",
    layout="wide"
)

load_css()
render_sidebar()

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
<h2>❤️ Charity Approval Center</h2>
<p>Review and manage donation listings submitted by users.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# STATS
# ==========================================

pending = charity_collection.count_documents(
    {"status": "Pending"}
)

approved = charity_collection.count_documents(
    {"status": "Approved"}
)

rejected = charity_collection.count_documents(
    {"status": "Rejected"}
)

total = charity_collection.count_documents({})

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Donations", total)
c2.metric("Pending", pending)
c3.metric("Approved", approved)
c4.metric("Rejected", rejected)

st.divider()

# ==========================================
# FILTER
# ==========================================

search = st.text_input(
    "🔍 Search by Category"
)

status_filter = st.selectbox(
    "Filter Status",
    [
        "All",
        "Pending",
        "Approved",
        "Rejected"
    ]
)

# ==========================================
# DATA
# ==========================================

items = charity_collection.find()

for item in items:

    category = item.get("category", "")

    if search:

        if search.lower() not in category.lower():
            continue

    if status_filter != "All":

        if item["status"] != status_filter:
            continue

    with st.container(border=True):

        col1, col2 = st.columns([1, 2])

        with col1:

            try:

                if os.path.exists(item["image"]):

                    st.image(
                        item["image"],
                        use_container_width=True
                    )

            except:
                pass

        with col2:

            st.subheader(category)

            st.write(
                f"👤 User : {item['posted_by']}"
            )

            st.write(
                f"📍 Location : {item['location']}"
            )

            status = item["status"]

            if status == "Pending":

                st.warning(
                    "⏳ Pending Approval"
                )

            elif status == "Approved":

                st.success(
                    "✅ Approved"
                )

            elif status == "Rejected":

                st.error(
                    "❌ Rejected"
                )

            # ==================================
            # ACTIONS
            # ==================================

            if status == "Pending":

                a, b = st.columns(2)

                with a:

                    if st.button(
                        "✅ Approve",
                        key=f"approve_{item['_id']}",
                        use_container_width=True
                    ):

                        charity_collection.update_one(
                            {"_id": item["_id"]},
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
                                "Your donation listing has been approved.",

                                "read":
                                False
                            }
                        )

                        st.success(
                            "Approved Successfully"
                        )

                        st.rerun()

                with b:

                    if st.button(
                        "❌ Reject",
                        key=f"reject_{item['_id']}",
                        use_container_width=True
                    ):

                        charity_collection.update_one(
                            {"_id": item["_id"]},
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
                                "Your donation listing has been rejected.",

                                "read":
                                False
                            }
                        )

                        st.rerun()

            st.divider()

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