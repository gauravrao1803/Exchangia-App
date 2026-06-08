import streamlit as st

from database import (
    charity_requests_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# =====================================
# AUTH
# =====================================

check_role("Volunteer")

st.set_page_config(
    page_title="Volunteer Dashboard",
    page_icon="🤝",
    layout="wide"
)

load_css()
render_sidebar()

# =====================================
# DATA
# =====================================

username = st.session_state.username

total_requests = charity_requests_collection.count_documents(
    {
        "volunteer": username
    }
)

accepted_requests = charity_requests_collection.count_documents(
    {
        "volunteer": username,
        "status": "Accepted"
    }
)

completed_requests = charity_requests_collection.count_documents(
    {
        "volunteer": username,
        "status": "Completed"
    }
)

pending_requests = charity_requests_collection.count_documents(
    {
        "volunteer": username,
        "status": "Pending"
    }
)

# =====================================
# HEADER
# =====================================

st.title("🤝 Volunteer Dashboard")

st.markdown(
    f"""
Welcome **{username}**

Help collect donations and support local communities.
"""
)

# =====================================
# STATS
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Pickup Requests",
        total_requests
    )

with col2:
    st.metric(
        "Pending",
        pending_requests
    )

with col3:
    st.metric(
        "Accepted",
        accepted_requests
    )

with col4:
    st.metric(
        "Completed",
        completed_requests
    )

st.divider()

# =====================================
# QUICK ACTIONS
# =====================================

st.subheader("⚡ Quick Actions")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    ### ❤️ Browse Donations

    View approved donation listings
    and volunteer for pickup.
    """)

    if st.button(
        "Browse Donations",
        use_container_width=True
    ):
        st.switch_page(
            "pages/charity_list.py"
        )

with col2:

    st.markdown("""
    ### 🚚 Pickup Requests

    Manage your assigned
    donation pickups.
    """)

    if st.button(
        "Open Requests",
        use_container_width=True
    ):
        st.switch_page(
            "pages/volunteer_requests.py"
        )

st.divider()

# =====================================
# RECENT REQUESTS
# =====================================

st.subheader("📋 Recent Donation Requests")

recent = charity_requests_collection.find(
    {
        "volunteer": username
    }
).sort(
    "_id",
    -1
).limit(5)

found = False

for req in recent:

    found = True

    with st.container(border=True):

        st.write(
            f"📦 Item: {req['item_name']}"
        )

        st.write(
            f"👤 Donor: {req['donor']}"
        )

        status = req["status"]

        if status == "Pending":
            st.warning("Pending")

        elif status == "Accepted":
            st.success("Accepted")

        elif status == "Completed":
            st.info("Completed")

        elif status == "Rejected":
            st.error("Rejected")

if not found:

    st.info(
        "No donation requests yet."
    )