import streamlit as st

from database import users_collection
from utils.styles import load_css

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Exchangia Login",
    page_icon="♻️",
    layout="centered"
)

load_css()

# ====================================
# SESSION
# ====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ====================================
# AUTO REDIRECT
# ====================================

if st.session_state.get("logged_in"):

    role = st.session_state.get("role")

    if role == "Admin":
        st.switch_page("pages/admin_dashboard.py")

    elif role == "Volunteer":
        st.switch_page("pages/volunteer_dashboard.py")

    else:
        st.switch_page("pages/dashboard.py")

# ====================================
# HERO
# ====================================

st.markdown("""
<div class="hero-card">
    <h1>♻️ Exchangia</h1>
    <p>
        Exchange Items • Donate Goods • Build Communities
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ====================================
# LOGIN FORM
# ====================================

st.subheader("🔐 Login")

with st.form("login_form"):

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    st.write("")

    login_btn = st.form_submit_button(
        "🚀 Login",
        use_container_width=True
    )

# ====================================
# LOGIN PROCESS
# ====================================

if login_btn:

    if not username.strip() or not password.strip():

        st.warning(
            "Please fill all fields."
        )

    else:

        user = users_collection.find_one(
            {
                "username": username,
                "password": password
            }
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            st.success(
                f"Welcome back {user['username']} 👋"
            )

            if user["role"] == "Admin":

                st.switch_page(
                    "pages/admin_dashboard.py"
                )

            elif user["role"] == "Volunteer":

                st.switch_page(
                    "pages/volunteer_dashboard.py"
                )

            else:

                st.switch_page(
                    "pages/dashboard.py"
                )

        else:

            st.error(
                "Invalid username or password"
            )

# ====================================
# SIGNUP SECTION
# ====================================

st.divider()

st.markdown(
    "<center><b>New to Exchangia?</b></center>",
    unsafe_allow_html=True
)

if st.button(
    "📝 Create Account",
    use_container_width=True
):

    st.switch_page(
        "pages/signup.py"
    )