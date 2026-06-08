import streamlit as st

from database import (
    charity_requests_collection
)

from utils.auth import check_login
from utils.sidebar import render_sidebar
from utils.styles import load_css
from utils.notifications import create_notification

# =====================================
# AUTH
# =====================================

check_login()

st.set_page_config(
    page_title="Charity Requests",
    page_icon="❤️",
    layout="wide"
)

load_css()
render_sidebar()

# =====================================
# PAGE HEADER
# =====================================

st.title("❤️ Charity Requests")
st.caption(
    "Manage volunteer pickup requests for your donations."
)

# =====================================
# FETCH REQUESTS
# =====================================

requests = list(
    charity_requests_collection.find(
        {
            "donor": st.session_state.username
        }
    )
)

# =====================================
# STATS
# =====================================

pending_count = charity_requests_collection.count_documents(
    {
        "donor": st.session_state.username,
        "status": "Pending"
    }
)

accepted_count = charity_requests_collection.count_documents(
    {
        "donor": st.session_state.username,
        "status": "Accepted"
    }
)

completed_count = charity_requests_collection.count_documents(
    {
        "donor": st.session_state.username,
        "status": "Completed"
    }
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "⏳ Pending",
        pending_count
    )

with c2:
    st.metric(
        "✅ Accepted",
        accepted_count
    )

with c3:
    st.metric(
        "🎁 Completed",
        completed_count
    )

st.divider()

# =====================================
# NO REQUESTS
# =====================================

if not requests:

    st.info(
        "No volunteer requests received yet."
    )

# =====================================
# REQUEST CARDS
# =====================================

for req in requests:

    with st.container(border=True):

        col1, col2 = st.columns([4,1])

        with col1:

            st.subheader(
                req["item_name"]
            )

            st.write(
                f"🤝 Volunteer: **{req['volunteer']}**"
            )

        with col2:

            status = req["status"]

            if status == "Pending":

                st.warning(
                    "⏳ Pending"
                )

            elif status == "Accepted":

                st.success(
                    "✅ Accepted"
                )

            elif status == "Rejected":

                st.error(
                    "❌ Rejected"
                )

            elif status == "Completed":

                st.info(
                    "🎁 Completed"
                )

        # =====================================
        # ACTIONS
        # =====================================

        if status == "Pending":

            colA, colB = st.columns(2)

            with colA:

                if st.button(
                    "✅ Accept Volunteer",
                    key=f"accept_{req['_id']}",
                    use_container_width=True
                ):

                    charity_requests_collection.update_one(
                        {
                            "_id": req["_id"]
                        },
                        {
                            "$set":
                            {
                                "status": "Accepted"
                            }
                        }
                    )

                    create_notification(
                        req["volunteer"],
                        "Your donation pickup request was accepted."
                    )

                    st.success(
                        "Volunteer Accepted"
                    )

                    st.rerun()

            with colB:

                if st.button(
                    "❌ Reject Volunteer",
                    key=f"reject_{req['_id']}",
                    use_container_width=True
                ):

                    charity_requests_collection.update_one(
                        {
                            "_id": req["_id"]
                        },
                        {
                            "$set":
                            {
                                "status": "Rejected"
                            }
                        }
                    )

                    create_notification(
                        req["volunteer"],
                        "Your donation pickup request was rejected."
                    )

                    st.error(
                        "Volunteer Rejected"
                    )

                    st.rerun()

        elif status == "Accepted":

            st.success(
                "Donation pickup is currently in progress."
            )

            st.page_link(
                "pages/chat.py",
                label="💬 Chat With Volunteer"
            )

        elif status == "Completed":

            st.success(
                "Donation successfully collected."
            )