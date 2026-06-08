import streamlit as st

from database import (
    users_collection,
    exchange_collection,
    charity_collection,
    exchange_requests_collection,
    notification_collection
)

from utils.auth import check_login
from utils.sidebar import render_sidebar
from utils.styles import load_css

# ==========================================
# AUTH
# ==========================================

check_login()

st.set_page_config(
    page_title="Profile",
    page_icon="👤",
    layout="wide"
)

load_css()
render_sidebar()

# ==========================================
# USER DATA
# ==========================================

user = users_collection.find_one(
    {
        "username": st.session_state.username
    }
)

# ==========================================
# COUNTS
# ==========================================

exchange_posts = exchange_collection.count_documents(
    {
        "posted_by": st.session_state.username
    }
)

charity_posts = charity_collection.count_documents(
    {
        "posted_by": st.session_state.username
    }
)

exchange_requests = exchange_requests_collection.count_documents(
    {
        "$or": [
            {"owner": st.session_state.username},
            {"requested_by": st.session_state.username}
        ]
    }
)

notifications = notification_collection.count_documents(
    {
        "username": st.session_state.username
    }
)

# ==========================================
# HEADER
# ==========================================

st.title("👤 My Profile")

# ==========================================
# PROFILE CARD
# ==========================================

with st.container(border=True):

    col1, col2 = st.columns([1,3])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/149/149071.png",
            width=120
        )

    with col2:

        st.subheader(user["username"])

        st.write(
            f"📧 {user.get('email','No Email')}"
        )

        role = user.get("role", "User")

        if role == "Admin":
            st.success(f"🛡️ {role}")

        elif role == "Volunteer":
            st.info(f"🤝 {role}")

        else:
            st.warning(f"👤 {role}")

# ==========================================
# STATS
# ==========================================

st.markdown("## 📊 Account Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Exchange Posts",
        exchange_posts
    )

with col2:
    st.metric(
        "Charity Posts",
        charity_posts
    )

with col3:
    st.metric(
        "Requests",
        exchange_requests
    )

with col4:
    st.metric(
        "Notifications",
        notifications
    )

# ==========================================
# ACCOUNT STATUS
# ==========================================

st.markdown("## 🔐 Account Status")

st.success(
    "Your account is active and verified."
)

# ==========================================
# ACTIVITY SUMMARY
# ==========================================

st.markdown("## 📌 Activity Summary")

st.write(
    f"🔄 You have posted **{exchange_posts}** exchange item(s)."
)

st.write(
    f"❤️ You have posted **{charity_posts}** donation item(s)."
)

st.write(
    f"📩 You have participated in **{exchange_requests}** exchange request(s)."
)

st.write(
    f"🔔 You have received **{notifications}** notification(s)."
)