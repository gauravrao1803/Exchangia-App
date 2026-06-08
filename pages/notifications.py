import streamlit as st

from database import notification_collection

from utils.auth import check_login
from utils.sidebar import render_sidebar
from utils.styles import load_css

check_login()

load_css()
render_sidebar()

st.title("🔔 Notifications")

notifications = notification_collection.find(
    {
        "username":
        st.session_state.username
    }
).sort(
    "timestamp",
    -1
)

found = False

for notif in notifications:

    found = True

    with st.container(border=True):

        st.write(
            notif["message"]
        )

        if not notif.get("read",False):

            if st.button(
                "Mark Read",
                key=str(notif["_id"])
            ):

                notification_collection.update_one(
                    {
                        "_id": notif["_id"]
                    },
                    {
                        "$set":
                        {
                            "read": True
                        }
                    }
                )

                st.rerun()

if not found:

    st.info(
        "No notifications yet."
    )