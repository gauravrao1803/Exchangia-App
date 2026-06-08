import streamlit as st

from database import (
    exchange_collection,
    exchange_requests_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# =========================================
# AUTH
# =========================================

check_role("User")

load_css()
render_sidebar()

# =========================================
# PAGE
# =========================================

st.title("📦 My Exchange Listings")

my_items = list(
    exchange_collection.find(
        {
            "posted_by":
            st.session_state.username
        }
    )
)

if not my_items:

    st.info(
        "You have not posted any item yet."
    )

# =========================================
# SHOW ITEMS
# =========================================

for item in my_items:

    with st.container(border=True):

        col1, col2 = st.columns([1,2])

        with col1:

            try:

                st.image(
                    item["image"],
                    width=220
                )

            except:

                st.warning(
                    "Image Missing"
                )

        with col2:

            st.subheader(
                item["category"]
            )

            st.write(
                f"📍 {item['location']}"
            )

            status = item.get(
                "status",
                "Pending"
            )

            if status == "Pending":

                st.warning(
                    "⏳ Waiting For Admin Approval"
                )

            elif status == "Approved":

                st.success(
                    "✅ Approved"
                )

            elif status == "Rejected":

                st.error(
                    "❌ Rejected"
                )

            # ==========================
            # REQUEST COUNT
            # ==========================

            request_count = exchange_requests_collection.count_documents(
                {
                    "requested_item_id":
                    str(item["_id"])
                }
            )

            st.info(
                f"📩 Exchange Requests: {request_count}"
            )

            # ==========================
            # DELETE
            # ==========================

            if st.button(
                "🗑 Delete Item",
                key=f"delete_{item['_id']}"
            ):

                exchange_collection.delete_one(
                    {
                        "_id":
                        item["_id"]
                    }
                )

                st.success(
                    "Item Deleted"
                )

                st.rerun()