import streamlit as st
from database import notification_collection


def render_sidebar():

    role = st.session_state.get(
        "role",
        ""
    )

    username = st.session_state.get(
        "username",
        "Guest"
    )

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
        <div style="
        text-align:center;
        padding:15px;
        ">
            <h2>♻️ Exchangia</h2>
            <p>Exchange • Donate • Help</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.success(
        f"👤 {username}"
    )

    # ======================================
    # ROLE BADGES
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

        st.sidebar.markdown(
            "### 🏠 Main"
        )

        st.page_link(
            "pages/dashboard.py",
            label="Dashboard"
        )

        st.page_link(
            "pages/profile.py",
            label="Profile"
        )

        st.sidebar.markdown(
            "### 🔄 Exchange"
        )

        st.page_link(
            "pages/exchange.py",
            label="Create Exchange"
        )

        st.page_link(
            "pages/exchange_list.py",
            label="Marketplace"
        )

        st.page_link(
            "pages/my_exchange_posts.py",
            label="My Listings"
        )

        st.page_link(
            "pages/my_requests.py",
            label="Exchange Requests"
        )

        st.sidebar.markdown(
            "### ❤️ Charity"
        )

        st.page_link(
            "pages/charity.py",
            label="Donate Item"
        )

        st.page_link(
            "pages/charity_requests.py",
            label="Donation Requests"
        )

        st.sidebar.markdown(
            "### 💬 Communication"
        )

        st.page_link(
            "pages/chat.py",
            label="Chats"
        )

        st.page_link(
            "pages/notifications.py",
            label=f"Notifications ({unread})"
        )

        st.sidebar.markdown(
            "### 🤝 Volunteer"
        )

        st.page_link(
            "pages/apply_volunteer.py",
            label="Become Volunteer"
        )

    # ======================================
    # VOLUNTEER MENU
    # ======================================

    elif role == "Volunteer":

        st.sidebar.markdown(
            "### 🤝 Volunteer"
        )

        st.page_link(
            "pages/volunteer_dashboard.py",
            label="Dashboard"
        )

        st.page_link(
            "pages/charity_list.py",
            label="Available Donations"
        )

        st.page_link(
            "pages/volunteer_requests.py",
            label="My Pickups"
        )

        st.sidebar.markdown(
            "### 💬 Communication"
        )

        st.page_link(
            "pages/chat.py",
            label="Chats"
        )

        st.page_link(
            "pages/notifications.py",
            label=f"Notifications ({unread})"
        )

        st.page_link(
            "pages/profile.py",
            label="Profile"
        )

    # ======================================
    # ADMIN MENU
    # ======================================

    elif role == "Admin":

        st.sidebar.markdown(
            "### 🛡 Admin Panel"
        )

        st.page_link(
            "pages/admin_dashboard.py",
            label="Dashboard"
        )

        st.page_link(
            "pages/admin_exchange_list.py",
            label="Exchange Approvals"
        )

        st.page_link(
            "pages/admin_charity_list.py",
            label="Charity Approvals"
        )

        st.page_link(
            "pages/admin_volunteer_requests.py",
            label="Volunteer Requests"
        )

    st.sidebar.divider()

    # ======================================
    # FOOTER
    # ======================================

    st.sidebar.caption(
        "Exchangia v1.0"
    )

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "login.py"
        )