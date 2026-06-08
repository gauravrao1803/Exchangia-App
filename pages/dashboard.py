import streamlit as st

from database import (
    exchange_collection,
    exchange_requests_collection,
    notification_collection,
    charity_collection
)

from utils.auth import check_login
from utils.sidebar import render_sidebar
from utils.styles import load_css

# ======================================
# AUTH
# ======================================

check_login()

st.set_page_config(
    page_title="Exchangia",
    page_icon="♻️",
    layout="wide"
)

load_css()
render_sidebar()

username = st.session_state.username

# ======================================
# COUNTS
# ======================================

my_posts = exchange_collection.count_documents(
    {
        "posted_by": username
    }
)

my_requests = exchange_requests_collection.count_documents(
    {
        "requested_by": username
    }
)

my_donations = charity_collection.count_documents(
    {
        "posted_by": username
    }
)

unread_notifications = notification_collection.count_documents(
    {
        "username": username,
        "read": False
    }
)

# ======================================
# HERO
# ======================================

st.markdown(f"""
<div class="hero-card">
    <h1>♻️ Welcome Back, {username}</h1>
    <p>
        Exchange items, donate goods and help your community.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ======================================
# STATS
# ======================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 My Posts",
        my_posts
    )

with col2:
    st.metric(
        "📩 Requests",
        my_requests
    )

with col3:
    st.metric(
        "❤️ Donations",
        my_donations
    )

with col4:
    st.metric(
        "🔔 Notifications",
        unread_notifications
    )

st.write("")
st.subheader("⚡ Quick Actions")

# ======================================
# ROW 1
# ======================================

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="feature-card">
        <h3>🔄 Exchange Item</h3>
        <p>
        Upload an item and exchange it with
        nearby community members.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Create Exchange",
        key="exchange",
        use_container_width=True
    ):
        st.switch_page(
            "pages/exchange.py"
        )

with c2:

    st.markdown("""
    <div class="feature-card">
        <h3>❤️ Donate Item</h3>
        <p>
        Give away unused items and
        support people in need.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Donate Item",
        key="donate",
        use_container_width=True
    ):
        st.switch_page(
            "pages/charity.py"
        )

with c3:

    st.markdown("""
    <div class="feature-card">
        <h3>🛒 Marketplace</h3>
        <p>
        Browse available exchange
        listings from other users.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Browse Marketplace",
        key="market",
        use_container_width=True
    ):
        st.switch_page(
            "pages/exchange_list.py"
        )

st.write("")

# ======================================
# ROW 2
# ======================================

c4, c5, c6 = st.columns(3)

with c4:

    st.markdown("""
    <div class="feature-card">
        <h3>📦 My Listings</h3>
        <p>
        View and manage all items
        you have posted.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "View Listings",
        key="myposts",
        use_container_width=True
    ):
        st.switch_page(
            "pages/my_exchange_posts.py"
        )

with c5:

    st.markdown("""
    <div class="feature-card">
        <h3>📩 Requests</h3>
        <p>
        Track incoming and outgoing
        exchange requests.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Open Requests",
        key="requests",
        use_container_width=True
    ):
        st.switch_page(
            "pages/my_requests.py"
        )

with c6:

    st.markdown("""
    <div class="feature-card">
        <h3>💬 Chats</h3>
        <p>
        Communicate directly with
        exchange partners.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Open Chats",
        key="chat",
        use_container_width=True
    ):
        st.switch_page(
            "pages/chat.py"
        )

st.write("")
st.divider()

# ======================================
# MARKETPLACE PREVIEW
# ======================================

st.subheader("🔥 Latest Marketplace Items")

latest_items = list(
    exchange_collection.find(
        {
            "status": "Approved"
        }
    ).sort(
        "_id",
        -1
    ).limit(4)
)

if latest_items:

    cols = st.columns(4)

    for i, item in enumerate(latest_items):

        with cols[i]:

            try:
                st.image(
                    item["image"],
                    use_container_width=True
                )
            except:
                pass

            st.markdown(
                f"**{item['category']}**"
            )

            st.caption(
                item.get(
                    "location",
                    "Unknown Location"
                )
            )

else:

    st.info(
        "No approved marketplace items yet."
    )

st.write("")

if st.button(
    "View Full Marketplace",
    use_container_width=True
):
    st.switch_page(
        "pages/exchange_list.py"
    )