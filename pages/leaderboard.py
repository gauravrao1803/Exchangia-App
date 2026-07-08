import streamlit as st

from database import users_collection

from utils.styles import load_css
from utils.sidebar import render_sidebar
from utils.auth import check_login

check_login()

st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
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

    with st.container(border=True):

        col1, col2, col3 = st.columns(
            [1,4,2]
        )

        with col1:

            st.markdown(
                f"## #{rank}"
            )

        with col2:

            st.subheader(
                user["username"]
            )

            st.write(
                user.get(
                    "badge",
                    "🌱 Beginner"
                )
            )

        with col3:

            st.metric(
                "Points",
                user.get(
                    "points",
                    0
                )
            )

    rank += 1