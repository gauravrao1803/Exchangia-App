import streamlit as st

from database import (
    exchange_collection,
    charity_collection,
    volunteer_collection,
    users_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

check_role("Admin")

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛡️",
    layout="wide"
)

load_css()
render_sidebar()

st.title("🛡️ Admin Dashboard")

# =====================================
# COUNTS
# =====================================

pending_exchange = exchange_collection.count_documents(
    {"status": "Pending"}
)

pending_charity = charity_collection.count_documents(
    {"status": "Pending"}
)

pending_volunteer = volunteer_collection.count_documents(
    {"status": "Pending"}
)

total_users = users_collection.count_documents({})

# =====================================
# STATS
# =====================================

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Exchange Approval",
    pending_exchange
)

c2.metric(
    "Charity Approval",
    pending_charity
)

c3.metric(
    "Volunteer Requests",
    pending_volunteer
)

c4.metric(
    "Total Users",
    total_users
)

st.divider()

# =====================================
# ACTIONS
# =====================================

col1,col2,col3 = st.columns(3)

with col1:

    if st.button(
        "🔄 Manage Exchange",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_exchange_list.py"
        )

with col2:

    if st.button(
        "❤️ Manage Charity",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_charity_list.py"
        )

with col3:

    if st.button(
        "🤝 Volunteer Requests",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_volunteer_requests.py"
        )