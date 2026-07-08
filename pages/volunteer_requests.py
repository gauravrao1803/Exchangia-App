import streamlit as st
from utils.rewards import add_points
from utils.badges import update_badge
from database import (
    charity_requests_collection,
    charity_collection
)

from utils.auth import (
    check_login,
    check_role
)

from utils.sidebar import render_sidebar
from utils.styles import load_css
from utils.rewards import add_points

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Volunteer Pickup Requests",
    page_icon="🚚",
    layout="wide"
)

# ==========================================
# AUTH
# ==========================================

check_login()
check_role("Volunteer")

# ==========================================
# LOAD UI
# ==========================================

load_css()
render_sidebar()

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero-card">
    <h1>🚚 Volunteer Pickup Requests</h1>
    <p>
        Manage your assigned donation pickups and earn reward points.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# FETCH REQUESTS
# ==========================================

requests = charity_requests_collection.find(
    {
        "volunteer": st.session_state.username
    }
)

# ==========================================
# SHOW REQUESTS
# ==========================================

found = False

for req in requests:

    found = True

    with st.container(border=True):

        st.subheader(req["item_name"])

        st.write(f"👤 Donor : {req['donor']}")

        st.write(f"📌 Status : {req['status']}")

        # =====================================
        # ACCEPTED
        # =====================================

        if req["status"] == "Accepted":

            st.success(
                "Pickup Assigned To You"
            )

            if st.button(
                "✅ Mark Donation Collected",
                key=f"complete_{req['_id']}",
                use_container_width=True
            ):

                # -------------------------------
                # COMPLETE REQUEST
                # -------------------------------

                charity_requests_collection.update_one(
                    {
                        "_id": req["_id"]
                    },
                    {
                        "$set":
                        {
                            "status": "Completed"
                        }
                    }
                )

                # -------------------------------
                # GET DONATION
                # -------------------------------

                donation = charity_collection.find_one(
                    {
                        "_id": req["donation_id"]
                    }
                )

                if donation:

                    # Prevent duplicate rewards

                    if not donation.get(
                        "reward_given",
                        False
                    ):

                        # Reward Donor

                        add_points(
                            donation["posted_by"],
                            50,
                            "Donation Completed"
                        )

                        # Reward Volunteer

                        add_points(
                            st.session_state.username,
                            60,
                            "Donation Pickup"
                        )

                        charity_collection.update_one(
                            {
                                "_id": donation["_id"]
                            },
                            {
                                "$set":
                                {
                                    "reward_given": True,
                                    "completed": True
                                }
                            }
                        )

                st.success(
                    "Donation completed successfully 🎉"
                )

                st.balloons()

                st.rerun()

        # =====================================
        # COMPLETED
        # =====================================

        elif req["status"] == "Completed":

            st.success(
                "✅ Donation Already Collected"
            )

        # =====================================
        # PENDING
        # =====================================

        elif req["status"] == "Pending":

            st.warning(
                "Waiting for NGO confirmation."
            )

        # =====================================
        # REJECTED
        # =====================================

        elif req["status"] == "Rejected":

            st.error(
                "Pickup Request Rejected"
            )

# ==========================================
# EMPTY STATE
# ==========================================

if not found:

    st.info(
        "No pickup requests assigned yet."
    )

add_points(
    donation["posted_by"],
    50,
    "Donation Completed"
)

update_badge(
    donation["posted_by"]
)

add_points(
    st.session_state.username,
    60,
    "Donation Pickup"
)

update_badge(
    st.session_state.username
)