import streamlit as st

from database import (
    exchange_requests_collection,
    notification_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# =====================================
# AUTH
# =====================================

check_role("User")

st.set_page_config(
    page_title="Exchange Requests",
    page_icon="📩",
    layout="wide"
)

load_css()
render_sidebar()

# =====================================
# PAGE HEADER
# =====================================

st.title("📩 Exchange Requests")
st.caption("Track and manage all your exchange offers.")

# =====================================
# FETCH REQUESTS
# =====================================

incoming_requests = list(
    exchange_requests_collection.find(
        {
            "owner": st.session_state.username
        }
    )
)

outgoing_requests = list(
    exchange_requests_collection.find(
        {
            "requested_by": st.session_state.username
        }
    )
)

accepted_count = exchange_requests_collection.count_documents(
    {
        "$or": [
            {"owner": st.session_state.username},
            {"requested_by": st.session_state.username}
        ],
        "status": "Accepted"
    }
)

pending_count = exchange_requests_collection.count_documents(
    {
        "$or": [
            {"owner": st.session_state.username},
            {"requested_by": st.session_state.username}
        ],
        "status": "Pending"
    }
)

# =====================================
# STATS
# =====================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📥 Incoming",
        len(incoming_requests)
    )

with c2:
    st.metric(
        "📤 Outgoing",
        len(outgoing_requests)
    )

with c3:
    st.metric(
        "✅ Accepted",
        accepted_count
    )

with c4:
    st.metric(
        "⏳ Pending",
        pending_count
    )

st.divider()

# =====================================
# TABS
# =====================================

incoming_tab, outgoing_tab = st.tabs(
    [
        "📥 Incoming Requests",
        "📤 Sent Requests"
    ]
)

# =====================================
# INCOMING
# =====================================

with incoming_tab:

    if not incoming_requests:
        st.info("No incoming exchange requests.")

    for request in incoming_requests:

        with st.container(border=True):

            col1, col2 = st.columns([4,1])

            with col1:

                st.subheader(
                    request["requested_item_name"]
                )

                st.write(
                    f"👤 Request From: **{request['requested_by']}**"
                )

                st.write(
                    f"🎁 Offering: **{request['offered_item_name']}**"
                )

            with col2:

                status = request["status"]

                if status == "Pending":
                    st.warning("⏳ Pending")

                elif status == "Accepted":
                    st.success("✅ Accepted")

                elif status == "Rejected":
                    st.error("❌ Rejected")

                elif status == "Completed":
                    st.info("✔ Completed")

            # =====================================
            # ACTIONS
            # =====================================

            if status == "Pending":

                a, b = st.columns(2)

                with a:

                    if st.button(
                        "✅ Accept",
                        key=f"accept_{request['_id']}",
                        use_container_width=True
                    ):

                        exchange_requests_collection.update_one(
                            {"_id": request["_id"]},
                            {
                                "$set":
                                {
                                    "status": "Accepted"
                                }
                            }
                        )

                        notification_collection.insert_one(
                            {
                                "username":
                                request["requested_by"],

                                "message":
                                f"{st.session_state.username} accepted your exchange request.",

                                "read":
                                False
                            }
                        )

                        st.rerun()

                with b:

                    if st.button(
                        "❌ Reject",
                        key=f"reject_{request['_id']}",
                        use_container_width=True
                    ):

                        exchange_requests_collection.update_one(
                            {"_id": request["_id"]},
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
                                request["requested_by"],

                                "message":
                                f"{st.session_state.username} rejected your exchange request.",

                                "read":
                                False
                            }
                        )

                        st.rerun()

            elif status == "Accepted":

                st.page_link(
                    "pages/chat.py",
                    label="💬 Open Chat"
                )

# =====================================
# OUTGOING
# =====================================

with outgoing_tab:

    if not outgoing_requests:
        st.info("No outgoing requests.")

    for request in outgoing_requests:

        with st.container(border=True):

            col1, col2 = st.columns([4,1])

            with col1:

                st.subheader(
                    request["requested_item_name"]
                )

                st.write(
                    f"👤 Owner: **{request['owner']}**"
                )

                st.write(
                    f"🎁 Offered Item: **{request['offered_item_name']}**"
                )

            with col2:

                status = request["status"]

                if status == "Pending":
                    st.warning("⏳ Pending")

                elif status == "Accepted":
                    st.success("✅ Accepted")

                elif status == "Rejected":
                    st.error("❌ Rejected")

                elif status == "Completed":
                    st.info("✔ Completed")

            if status == "Accepted":

                st.page_link(
                    "pages/chat.py",
                    label="💬 Open Chat"
                )