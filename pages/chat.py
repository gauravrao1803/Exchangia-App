import streamlit as st
from datetime import datetime

from database import (
    exchange_requests_collection,
    charity_requests_collection,
    chat_collection
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
    page_title="Chats",
    page_icon="💬",
    layout="wide"
)

load_css()
render_sidebar()

# =====================================
# HEADER
# =====================================

st.title("💬 Messages")

col1, col2 = st.columns([8, 1])

with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

# =====================================
# EXCHANGE CHATS
# =====================================

st.markdown("## 🔄 Exchange Chats")

exchange_requests = list(
    exchange_requests_collection.find(
        {
            "$or": [
                {"owner": st.session_state.username},
                {"requested_by": st.session_state.username}
            ],
            "status": "Accepted"
        }
    )
)

if not exchange_requests:
    st.info("No active exchange chats.")

for req in exchange_requests:

    room_id = f"exchange_{req['_id']}"

    if st.session_state.username == req["owner"]:
        other_user = req["requested_by"]
    else:
        other_user = req["owner"]

    with st.container(border=True):

        st.subheader(
            f"{req['requested_item_name']} ↔ {req['offered_item_name']}"
        )

        st.caption(f"Chat with {other_user}")

        # =====================================
        # MESSAGES
        # =====================================

        messages = list(
            chat_collection.find(
                {
                    "room_id": room_id
                }
            ).sort(
                "timestamp",
                1
            )
        )

        chat_box = st.container(height=300)

        with chat_box:

            if not messages:
                st.info("Start the conversation.")

            for msg in messages:

                if msg["sender"] == st.session_state.username:

                    st.markdown(
                        f"""
                        <div style="
                        text-align:right;
                        margin:8px;
                        padding:10px;
                        background:#DCF8C6;
                        border-radius:10px;">
                        <b>You</b><br>
                        {msg['message']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div style="
                        text-align:left;
                        margin:8px;
                        padding:10px;
                        background:#F1F0F0;
                        border-radius:10px;">
                        <b>{msg['sender']}</b><br>
                        {msg['message']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # =====================================
        # SEND MESSAGE
        # =====================================

        col1, col2 = st.columns([5, 1])

        with col1:

            message = st.text_input(
                "Type message",
                key=f"exchange_msg_{room_id}"
            )

        with col2:

            send = st.button(
                "Send",
                key=f"exchange_send_{room_id}"
            )

        if send and message.strip():

            chat_collection.insert_one(
                {
                    "room_id": room_id,
                    "sender": st.session_state.username,
                    "receiver": other_user,
                    "message": message,
                    "timestamp": datetime.now()
                }
            )

            create_notification(
                other_user,
                f"New message from {st.session_state.username}"
            )

            st.rerun()

# =====================================
# CHARITY CHATS
# =====================================

st.markdown("---")
st.markdown("## ❤️ Charity Chats")

charity_requests = list(
    charity_requests_collection.find(
        {
            "$or": [
                {"donor": st.session_state.username},
                {"volunteer": st.session_state.username}
            ],
            "status": "Accepted"
        }
    )
)

if not charity_requests:
    st.info("No active charity chats.")

for req in charity_requests:

    room_id = f"charity_{req['_id']}"

    if st.session_state.username == req["donor"]:
        other_user = req["volunteer"]
    else:
        other_user = req["donor"]

    with st.container(border=True):

        st.subheader(req["item_name"])

        st.caption(f"Chat with {other_user}")

        # =====================================
        # MESSAGES
        # =====================================

        messages = list(
            chat_collection.find(
                {
                    "room_id": room_id
                }
            ).sort(
                "timestamp",
                1
            )
        )

        chat_box = st.container(height=300)

        with chat_box:

            if not messages:
                st.info("Start the conversation.")

            for msg in messages:

                if msg["sender"] == st.session_state.username:

                    st.markdown(
                        f"""
                        <div style="
                        text-align:right;
                        margin:8px;
                        padding:10px;
                        background:#DCF8C6;
                        border-radius:10px;">
                        <b>You</b><br>
                        {msg['message']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div style="
                        text-align:left;
                        margin:8px;
                        padding:10px;
                        background:#F1F0F0;
                        border-radius:10px;">
                        <b>{msg['sender']}</b><br>
                        {msg['message']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # =====================================
        # SEND MESSAGE
        # =====================================

        col1, col2 = st.columns([5, 1])

        with col1:

            message = st.text_input(
                "Type message",
                key=f"charity_msg_{room_id}"
            )

        with col2:

            send = st.button(
                "Send",
                key=f"charity_send_{room_id}"
            )

        if send and message.strip():

            chat_collection.insert_one(
                {
                    "room_id": room_id,
                    "sender": st.session_state.username,
                    "receiver": other_user,
                    "message": message,
                    "timestamp": datetime.now()
                }
            )

            create_notification(
                other_user,
                f"New message from {st.session_state.username}"
            )

            st.rerun()