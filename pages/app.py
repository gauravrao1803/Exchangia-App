import streamlit as st

from database import (
    exchange_collection,
    charity_collection,
    exchange_requests_collection
)

from utils.auth import check_role
from utils.sidebar import render_sidebar
from utils.styles import load_css

# =====================================
# AUTH
# =====================================

check_role("User")

st.set_page_config(
    page_title="Exchangia",
    page_icon="♻️",
    layout="wide"
)

load_css()
render_sidebar()

# =====================================
# USER DATA
# =====================================

username = st.session_state.username

total_posts = exchange_collection.count_documents(
    {
        "posted_by": username
    }
)

total_donations = charity_collection.count_documents(
    {
        "posted_by": username
    }
)

total_requests = exchange_requests_collection.count_documents(
    {
        "$or": [
            {"owner": username},
            {"requested_by": username}
        ]
    }
)

# =====================================
# HERO SECTION
# =====================================

st.markdown("""
# ♻️ Welcome to Exchangia

### Exchange • Donate • Help Communities

A community-driven platform where people can:

✅ Exchange unused items

✅ Donate useful products

✅ Connect with volunteers

✅ Reduce waste and help society
""")

st.divider()

# =====================================
# USER STATS
# =====================================

st.subheader("📊 Your Activity")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Exchange Posts",
        total_posts
    )

with col2:
    st.metric(
        "Donations",
        total_donations
    )

with col3:
    st.metric(
        "Requests",
        total_requests
    )

st.divider()

# =====================================
# QUICK ACTIONS
# =====================================

st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.markdown("""
        ### 🔄 Exchange Item

        Upload an item and exchange it
        with another community member.
        """)

        if st.button(
            "Create Exchange",
            use_container_width=True
        ):
            st.switch_page(
                "pages/exchange.py"
            )

with col2:

    with st.container(border=True):

        st.markdown("""
        ### ❤️ Donate Item

        Donate useful products
        to help others.
        """)

        if st.button(
            "Donate Item",
            use_container_width=True
        ):
            st.switch_page(
                "pages/charity.py"
            )

with col3:

    with st.container(border=True):

        st.markdown("""
        ### 🛒 Marketplace

        Browse approved exchange items.
        """)

        if st.button(
            "Browse Marketplace",
            use_container_width=True
        ):
            st.switch_page(
                "pages/exchange_list.py"
            )

st.divider()

# =====================================
# MANAGEMENT SECTION
# =====================================

st.subheader("📦 Manage Your Activity")

col4, col5, col6 = st.columns(3)

with col4:

    if st.button(
        "📦 My Posts",
        use_container_width=True
    ):
        st.switch_page(
            "pages/my_exchange_posts.py"
        )

with col5:

    if st.button(
        "📩 My Requests",
        use_container_width=True
    ):
        st.switch_page(
            "pages/my_requests.py"
        )

with col6:

    if st.button(
        "💬 Chats",
        use_container_width=True
    ):
        st.switch_page(
            "pages/chat.py"
        )

st.divider()

# =====================================
# RECENT MARKETPLACE ITEMS
# =====================================

st.subheader("🔥 Latest Exchange Items")

latest_items = list(
    exchange_collection.find(
        {
            "status": "Approved"
        }
    ).limit(5)
)

if latest_items:

    cols = st.columns(len(latest_items))

    for index, item in enumerate(latest_items):

        with cols[index]:

            try:
                st.image(
                    item["image"]
                )
            except:
                pass

            st.write(
                item["category"]
            )

            st.caption(
                item["location"]
            )

else:

    st.info(
        "No approved listings available."
    )

st.divider()

# =====================================
# VOLUNTEER SECTION
# =====================================

st.subheader("🤝 Become a Volunteer")

st.write(
    """
Help collect donated items and support NGOs.

Volunteers can connect donors with communities
that need assistance.
"""
)

if st.button(
    "Apply As Volunteer",
    use_container_width=True
):

    st.switch_page(
        "pages/apply_volunteer.py"
    )

st.divider()

st.success(
    "🌱 Together we can reduce waste and help communities."
)