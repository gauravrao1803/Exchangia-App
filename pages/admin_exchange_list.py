import streamlit as st
import os

from database import (
    exchange_collection,
    notification_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Exchange Approvals",
    page_icon="🛡️",
    layout="wide"
)

# =====================================
# AUTH
# =====================================

check_role("Admin")

load_css()
render_sidebar()

# =====================================
# HEADER
# =====================================

st.title("🔄 Exchange Listings Approval")

st.caption(
    "Approve, reject or remove exchange listings."
)

# =====================================
# STATS
# =====================================

pending_count = exchange_collection.count_documents(
    {"status": "Pending"}
)

approved_count = exchange_collection.count_documents(
    {"status": "Approved"}
)

rejected_count = exchange_collection.count_documents(
    {"status": "Rejected"}
)

c1, c2, c3 = st.columns(3)

c1.metric("Pending", pending_count)
c2.metric("Approved", approved_count)
c3.metric("Rejected", rejected_count)

st.divider()

# =====================================
# ITEMS
# =====================================

items = exchange_collection.find().sort(
    "_id",
    -1
)

for item in items:

    with st.container(border=True):

        col1, col2 = st.columns([2, 1])

        with col1:

            try:

                if os.path.exists(item["image"]):

                    st.image(
                        item["image"],
                        width=250
                    )

            except:
                pass

            st.subheader(
                item.get(
                    "category",
                    "Unknown"
                )
            )

            st.write(
                f"📍 Location: {item.get('location', 'N/A')}"
            )

            st.write(
                f"👤 Posted By: {item.get('posted_by', 'Unknown')}"
            )

            status = item.get(
                "status",
                "Pending"
            )

            if status == "Pending":
                st.warning("⏳ Pending")

            elif status == "Approved":
                st.success("✅ Approved")

            elif status == "Rejected":
                st.error("❌ Rejected")

        with col2:

            st.write("")

            if st.button(
                "✅ Approve",
                key=f"approve_{item['_id']}",
                use_container_width=True
            ):

                exchange_collection.update_one(
                    {
                        "_id": item["_id"]
                    },
                    {
                        "$set": {
                            "status": "Approved"
                        }
                    }
                )

                notification_collection.insert_one(
                    {
                        "username": item["posted_by"],
                        "message":
                        f"Your exchange item '{item['category']}' was approved.",
                        "read": False
                    }
                )

                st.rerun()

            if st.button(
                "❌ Reject",
                key=f"reject_{item['_id']}",
                use_container_width=True
            ):

                exchange_collection.update_one(
                    {
                        "_id": item["_id"]
                    },
                    {
                        "$set": {
                            "status": "Rejected"
                        }
                    }
                )

                notification_collection.insert_one(
                    {
                        "username": item["posted_by"],
                        "message":
                        f"Your exchange item '{item['category']}' was rejected.",
                        "read": False
                    }
                )

                st.rerun()

            if st.button(
                "🗑 Delete",
                key=f"delete_{item['_id']}",
                use_container_width=True
            ):

                exchange_collection.delete_one(
                    {
                        "_id": item["_id"]
                    }
                )

                st.rerun()