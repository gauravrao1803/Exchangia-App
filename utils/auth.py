import streamlit as st

def check_login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "role" not in st.session_state:
        st.session_state.role = ""

    if not st.session_state.logged_in:

        st.warning(
            "Please Login First"
        )

        st.switch_page(
            "login.py"
        )


def check_role(role_name):

    check_login()

    if st.session_state.role != role_name:

        st.error(
            "Access Denied"
        )

        st.stop()