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
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)

load_css()
render_sidebar()

# ==========================================
# USER DATA
# ==========================================

username = st.session_state.username

user = users_collection.find_one(
    {
        "username": username
    }
)

# ==========================================
# USER INFO
# ==========================================

points = user.get("points", 0)

badge = user.get(
    "badge",
    "🌱 Beginner"
)

role = user.get(
    "role",
    "User"
)

# ==========================================
# COUNTS
# ==========================================

exchange_posts = exchange_collection.count_documents(
    {
        "posted_by": username
    }
)

charity_posts = charity_collection.count_documents(
    {
        "posted_by": username
    }
)

exchange_requests = exchange_requests_collection.count_documents(
    {
        "$or": [
            {
                "owner": username
            },
            {
                "requested_by": username
            }
        ]
    }
)

notifications = notification_collection.count_documents(
    {
        "username": username
    }
)

# ==========================================
# HEADER
# ==========================================

st.markdown(f"""
<div class="hero-card">
    <h1>👤 {username}</h1>
    <p>Your Exchangia Community Profile</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PROFILE CARD
# ==========================================

with st.container(border=True):

    col1, col2 = st.columns([1,3])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/149/149071.png",
            width=140
        )

    with col2:

        st.subheader(username)

        st.write(f"📧 {user.get('email','No Email')}")

        st.write(f"🎖 Badge : **{badge}**")

        st.metric(
            "⭐ Reward Points",
            points
        )

        if role == "Admin":

            st.success("🛡️ Admin")

        elif role == "Volunteer":

            st.info("🤝 Volunteer")

        else:

            st.warning("👤 User")

# ==========================================
# BADGE PROGRESS
# ==========================================

st.subheader("🏅 Badge Progress")

levels = [
    (0, "🌱 Beginner"),
    (200, "🥉 Bronze"),
    (500, "🥈 Silver"),
    (1000, "🥇 Gold"),
    (2000, "🏆 Legend")
]

next_points = None

for p, name in levels:

    if points < p:

        next_points = p

        break

if next_points:

    progress = points / next_points

    st.progress(
        min(progress, 1.0)
    )

    st.caption(
        f"{next_points-points} points remaining to reach the next badge."
    )

else:

    st.success(
        "🏆 Congratulations! You have achieved the highest badge."
    )

# ==========================================
# STATISTICS
# ==========================================

st.subheader("📊 Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Exchange Posts",
    exchange_posts
)

c2.metric(
    "Donation Posts",
    charity_posts
)

c3.metric(
    "Exchange Requests",
    exchange_requests
)

c4.metric(
    "Notifications",
    notifications
)

# ==========================================
# COMMUNITY IMPACT
# ==========================================

st.subheader("🌍 Community Impact")

impact = charity_posts * 5 + exchange_posts * 2

st.metric(
    "Impact Score",
    impact
)

if impact >= 100:

    st.success(
        "Amazing! You are making a huge community impact."
    )

elif impact >= 50:

    st.info(
        "Great work! Keep helping the community."
    )

else:

    st.warning(
        "Start donating and exchanging more items to increase your impact."
    )

# ==========================================
# ACCOUNT SUMMARY
# ==========================================

st.subheader("📌 Account Summary")

st.write(f"👤 Username : **{username}**")

st.write(f"🎖 Badge : **{badge}**")

st.write(f"⭐ Total Reward Points : **{points}**")

st.write(f"🔄 Exchange Posts : **{exchange_posts}**")

st.write(f"❤️ Donation Posts : **{charity_posts}**")

st.write(f"📩 Requests : **{exchange_requests}**")

st.write(f"🔔 Notifications : **{notifications}**")

st.success(
    "Your account is active and verified."
)