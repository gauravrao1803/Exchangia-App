import streamlit as st

from database import users_collection

from utils.auth import check_login
from utils.sidebar import render_sidebar
from utils.styles import load_css

check_login()

st.set_page_config(
    page_title="Leaderboard",
    layout="wide"
)

load_css()
render_sidebar()

st.title("🏆 Community Leaderboard")

users = users_collection.find().sort(
    "points",
    -1
)

rank = 1

for user in users:

    st.markdown(
        f"""
### {rank}. {user['username']}

⭐ {user.get('points',0)} Points

🏅 {user.get('badge','Bronze')}
"""
    )

    rank += 1