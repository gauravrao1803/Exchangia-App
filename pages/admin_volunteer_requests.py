import streamlit as st

from database import (
    volunteer_collection,
    users_collection,
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
    page_title="Volunteer Requests",
    page_icon="🤝",
    layout="wide"
)

load_css()
render_sidebar()

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
<h2>🤝 Volunteer Applications</h2>
<p>Review and approve community volunteers.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# STATS
# ==========================================

total = volunteer_collection.count_documents({})

pending = volunteer_collection.count_documents(
    {"status": "Pending"}
)

approved = volunteer_collection.count_documents(
    {"status": "Approved"}
)

rejected = volunteer_collection.count_documents(
    {"status": "Rejected"}
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Applications", total)
c2.metric("Pending", pending)
c3.metric("Approved", approved)
c4.metric("Rejected", rejected)

st.divider()

# ==========================================
# FILTERS
# ==========================================

search = st.text_input(
    "🔍 Search Username"
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

requests = volunteer_collection.find()

for req in requests:

    username = req["username"]

    if search:

        if search.lower() not in username.lower():

            continue

    if status_filter != "All":

        if req["status"] != status_filter:

            continue

    with st.container(border=True):

        st.subheader(
            req["ngo_name"]
        )

        st.write(
            f"👤 Username : {username}"
        )

        st.write(
            f"📍 Location : {req['location']}"
        )

        st.write(
            f"📞 Contact : {req['contact']}"
        )

        st.write(
            f"📝 Requirements : {req['requirements']}"
        )

        status = req["status"]

        if status == "Pending":

            st.warning(
                "⏳ Pending Review"
            )

        elif status == "Approved":

            st.success(
                "✅ Approved"
            )

        elif status == "Rejected":

            st.error(
                "❌ Rejected"
            )

        # ======================================
        # ACTIONS
        # ======================================

        if status == "Pending":

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Approve",
                    key=f"approve_{req['_id']}",
                    use_container_width=True
                ):

                    volunteer_collection.update_one(
                        {"_id": req["_id"]},
                        {
                            "$set":
                            {
                                "status":
                                "Approved"
                            }
                        }
                    )

                    users_collection.update_one(
                        {
                            "username":
                            username
                        },
                        {
                            "$set":
                            {
                                "role":
                                "Volunteer"
                            }
                        }
                    )

                    notification_collection.insert_one(
                        {
                            "username":
                            username,

                            "message":
                            "Your volunteer application has been approved.",

                            "read":
                            False
                        }
                    )

                    st.success(
                        "Volunteer Approved"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Reject",
                    key=f"reject_{req['_id']}",
                    use_container_width=True
                ):

                    volunteer_collection.update_one(
                        {"_id": req["_id"]},
                        {
                            "$set":
                            {
                                "status":
                                "Rejected"
                            }
                        }
                    )

                    notification_collection.insert_one(
                        {
                            "username":
                            username,

                            "message":
                            "Your volunteer application has been rejected.",

                            "read":
                            False
                        }
                    )

                    st.error(
                        "Application Rejected"
                    )

                    st.rerun()