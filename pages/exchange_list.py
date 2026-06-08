
import streamlit as st

from database import (
    exchange_collection,
    exchange_requests_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css
from utils.notifications import create_notification


# ==========================================
# AUTH
# ==========================================

check_role("User")

st.set_page_config(
    page_title="Marketplace",
    page_icon="🔄",
    layout="wide"
)

load_css()
render_sidebar()

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero-card">
    <h1>🔄 Exchange Marketplace</h1>
    <p>Browse approved items and exchange with community members.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SEARCH + FILTER
# ==========================================

col1, col2 = st.columns([3, 1])

with col1:

    search = st.text_input(
        "🔍 Search Item"
    )

with col2:

    category_filter = st.selectbox(
        "Category",
        [
            "All",
            "Electronics",
            "Books",
            "Clothes",
            "Furniture",
            "Sports",
            "Other"
        ]
    )

st.write("")

# ==========================================
# FETCH ITEMS
# ==========================================

items = exchange_collection.find().sort(
    "_id",
    -1
)

# ==========================================
# LOOP ITEMS
# ==========================================

for item in items:

    category = item.get(
        "category",
        ""
    )

    description = item.get(
        "description",
        "No description available."
    )

    owner = item.get(
        "posted_by",
        ""
    )

    status = item.get(
        "status",
        "Pending"
    )

    # ======================================
    # SEARCH FILTER
    # ======================================

    if search:

        if search.lower() not in category.lower():

            continue

    # ======================================
    # CATEGORY FILTER
    # ======================================

    if category_filter != "All":

        if category != category_filter:

            continue

    # ======================================
    # HIDE REJECTED ITEMS FROM OTHERS
    # ======================================

    if (
        status == "Rejected"
        and owner != st.session_state.username
    ):
        continue

    # ======================================
    # CARD
    # ======================================

    with st.container(border=True):

        col1, col2 = st.columns([1, 2])

        # ==============================
        # IMAGE
        # ==============================

        with col1:

            try:

                st.image(
                    item["image"],
                    use_container_width=True
                )

            except:

                st.warning(
                    "Image not available"
                )

        # ==============================
        # DETAILS
        # ==============================

        with col2:

            st.subheader(category)

            st.caption(
                f"📍 {item.get('location','N/A')}"
            )

            st.write(
                f"👤 Owner: {owner}"
            )

            st.write(
                description
            )

            # ==========================
            # STATUS
            # ==========================

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

            # ==========================
            # MY OWN ITEM
            # ==========================

            if owner == st.session_state.username:

                st.info(
                    "📦 This is your item."
                )

                continue

            # ==========================
            # ONLY APPROVED ITEMS
            # ==========================

            if status != "Approved":

                continue

            # ==========================
            # MY APPROVED ITEMS
            # ==========================

            my_items = list(
                exchange_collection.find(
                    {
                        "posted_by":
                        st.session_state.username,

                        "status":
                        "Approved"
                    }
                )
            )

            if not my_items:

                st.warning(
                    "Post an approved item before sending exchange requests."
                )

                continue

            # ==========================
            # ITEM OPTIONS
            # ==========================

            item_options = {

                i["category"]:
                str(i["_id"])

                for i in my_items
            }

            selected_item = st.selectbox(
                "Choose Item To Offer",
                list(item_options.keys()),
                key=f"offer_{item['_id']}"
            )

            # ==========================
            # EXISTING REQUEST
            # ==========================

            existing_request = exchange_requests_collection.find_one(
                {
                    "requested_item_id":
                    str(item["_id"]),

                    "requested_by":
                    st.session_state.username
                }
            )

            if existing_request:

                request_status = existing_request["status"]

                if request_status == "Pending":

                    st.warning(
                        "⏳ Request Pending"
                    )

                elif request_status == "Accepted":

                    st.success(
                        "✅ Request Accepted"
                    )

                    st.page_link(
                        "pages/chat.py",
                        label="💬 Open Chat"
                    )

                elif request_status == "Rejected":

                    st.error(
                        "❌ Request Rejected"
                    )

                elif request_status == "Completed":

                    st.success(
                        "✔ Exchange Completed"
                    )

            else:

                # ======================
                # SEND REQUEST
                # ======================

                if st.button(
                    "🔄 Send Exchange Offer",
                    key=f"request_{item['_id']}"
                ):

                    exchange_requests_collection.insert_one(
                        {
                            "requested_item_id":
                            str(item["_id"]),

                            "requested_item_name":
                            item["category"],

                            "offered_item_id":
                            item_options[selected_item],

                            "offered_item_name":
                            selected_item,

                            "owner":
                            owner,

                            "requested_by":
                            st.session_state.username,

                            "status":
                            "Pending"
                        }
                    )

                    create_notification(
                        owner,
                        f"{st.session_state.username} sent an exchange offer for your item."
                    )

                    st.success(
                        "Exchange request sent successfully."
                    )

                    st.rerun()