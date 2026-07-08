import streamlit as st

from database import (
    users_collection,
    notification_collection
)


def render_sidebar():

    # ======================================
    # SESSION
    # ======================================

    username = st.session_state.get(
        "username",
        "Guest"
    )

    role = st.session_state.get(
        "role",
        ""
    )

    # ======================================
    # USER INFO
    # ======================================

    user = users_collection.find_one(
        {
            "username": username
        }
    )

    if user:

        points = user.get(
            "points",
            0
        )

        badge = user.get(
            "badge",
            "🌱 Beginner"
        )

    else:

        points = 0
        badge = "🌱 Beginner"

    unread = notification_collection.count_documents(
        {
            "username": username,
            "read": False
        }
    )

    # ======================================
    # HEADER
    # ======================================

    st.sidebar.markdown(
        """
        <div style="text-align:center;padding:10px;">
            <h2>♻️ Exchangia</h2>
            <p>Exchange • Donate • Help</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.success(
        f"👤 {username}"
    )

    st.sidebar.write(
        f"🏅 {badge}"
    )

    st.sidebar.write(
        f"⭐ {points} Points"
    )

    progress = min(points / 500, 1.0)

    st.sidebar.progress(progress)

    st.sidebar.caption(
        f"{points}/500 Points to next level"
    )

    # ======================================
    # ROLE
    # ======================================

    if role == "Admin":

        st.sidebar.error(
            "🛡 Administrator"
        )

    elif role == "Volunteer":

        st.sidebar.warning(
            "🤝 Volunteer"
        )

    else:

        st.sidebar.info(
            "👤 Community User"
        )

    st.sidebar.divider()

    # ======================================
    # USER MENU
    # ======================================

    if role == "User":

        st.sidebar.subheader("🏠 Dashboard")

        st.sidebar.page_link(
            "pages/dashboard.py",
            label="Dashboard"
        )

        st.sidebar.page_link(
            "pages/profile.py",
            label="Profile"
        )

        st.sidebar.divider()

        st.sidebar.subheader("🔄 Exchange")

        st.sidebar.page_link(
            "pages/exchange.py",
            label="Create Exchange"
        )

        st.sidebar.page_link(
            "pages/exchange_list.py",
            label="Marketplace"
        )

        st.sidebar.page_link(
            "pages/my_exchange_posts.py",
            label="My Listings"
        )

        st.sidebar.page_link(
            "pages/my_requests.py",
            label="Exchange Requests"
        )

        st.sidebar.divider()

        st.sidebar.subheader("❤️ Charity")

        st.sidebar.page_link(
            "pages/charity.py",
            label="Donate Item"
        )

        st.sidebar.page_link(
            "pages/charity_requests.py",
            label="Donation Requests"
        )

        st.sidebar.divider()

        st.sidebar.subheader("💬 Communication")

        st.sidebar.page_link(
            "pages/chat.py",
            label="Chats"
        )

        st.sidebar.page_link(
            "pages/notifications.py",
            label=f"Notifications ({unread})"
        )

        st.sidebar.divider()

        st.sidebar.subheader("🌟 Community")

        st.sidebar.page_link(
            "pages/leaderboard.py",
            label="Leaderboard"
        )

        st.sidebar.page_link(
            "pages/apply_volunteer.py",
            label="Become Volunteer"
        )

    # ======================================
    # VOLUNTEER MENU
    # ======================================

    elif role == "Volunteer":

        st.sidebar.subheader("🤝 Volunteer")

        st.sidebar.page_link(
            "pages/volunteer_dashboard.py",
            label="Dashboard"
        )

        st.sidebar.page_link(
            "pages/charity_list.py",
            label="Available Donations"
        )

        st.sidebar.page_link(
            "pages/volunteer_requests.py",
            label="My Pickups"
        )

        st.sidebar.divider()

        st.sidebar.subheader("💬 Communication")

        st.sidebar.page_link(
            "pages/chat.py",
            label="Chats"
        )

        st.sidebar.page_link(
            "pages/notifications.py",
            label=f"Notifications ({unread})"
        )

        st.sidebar.page_link(
            "pages/profile.py",
            label="Profile"
        )

        st.sidebar.page_link(
            "pages/leaderboard.py",
            label="Leaderboard"
        )

    # ======================================
    # ADMIN MENU
    # ======================================

    elif role == "Admin":

        st.sidebar.subheader("🛡 Admin Panel")

        st.sidebar.page_link(
            "pages/admin_dashboard.py",
            label="Dashboard"
        )

        st.sidebar.page_link(
            "pages/admin_exchange_list.py",
            label="Exchange Approvals"
        )

        st.sidebar.page_link(
            "pages/admin_charity_list.py",
            label="Charity Approvals"
        )

        st.sidebar.page_link(
            "pages/admin_volunteer_requests.py",
            label="Volunteer Requests"
        )

        st.sidebar.page_link(
            "pages/profile.py",
            label="Profile"
        )

    # ======================================
    # FOOTER
    # ======================================

    st.sidebar.divider()

    st.sidebar.caption(
        "Exchangia v2.0 🚀"
    )

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "login.py"
        )