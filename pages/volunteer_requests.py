import streamlit as st
from utils.sidebar import render_sidebar
from utils.styles import load_css
from utils.auth import check_role

check_role("Volunteer")
load_css()
render_sidebar()
from database import (
    charity_requests_collection
)

from utils.auth import check_login

check_login()

# ONLY VOLUNTEER
if st.session_state.role != "Volunteer":

    st.error("Access Denied")

    st.stop()

st.title("🚚 Volunteer Pickup Requests")

requests = charity_requests_collection.find(
    {
        "volunteer": st.session_state.username
    }
)

for req in requests:

    st.markdown("---")

    st.subheader(
        req["item_name"]
    )

    st.write(
        f"👤 Donor: {req['donor']}"
    )

    st.write(
        f"📌 Status: {req['status']}"
    )

    # ---------------- ACCEPTED ----------------

    if req["status"] == "Accepted":

        if st.button(
            "✔ Mark Donation Collected",
            key=f"complete_{req['_id']}"
        ):

            charity_requests_collection.update_one(
                {
                    "_id": req["_id"]
                },
                {
                    "$set": {
                        "status": "Completed"
                    }
                }
            )

            st.success(
                "Donation Marked Completed"
            )

            st.rerun()

    # ---------------- COMPLETED ----------------

    elif req["status"] == "Completed":

        st.success(
            "Donation Already Collected"
        )