import streamlit as st

from database import users_collection
from utils.styles import load_css

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Create Account",
    page_icon="📝",
    layout="centered"
)

load_css()

# ====================================
# ALREADY LOGGED IN
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
# HERO SECTION
# ====================================

st.markdown("""
<div class="hero-card">
    <h1>♻️ Join Exchangia</h1>
    <p>
        Create your account and start exchanging,
        donating and helping your community.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ====================================
# SIGNUP FORM
# ====================================

st.subheader("📝 Create Account")

with st.form("signup_form"):

    username = st.text_input(
        "Username",
        placeholder="Choose a username"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Confirm password"
    )

    st.write("")

    signup_btn = st.form_submit_button(
        "🚀 Create Account",
        use_container_width=True
    )

# ====================================
# CREATE ACCOUNT
# ====================================

if signup_btn:

    username = username.strip()
    email = email.strip()

    if not username or not email or not password:

        st.error(
            "Please fill all fields."
        )

    elif len(username) < 3:

        st.error(
            "Username must be at least 3 characters."
        )

    elif len(password) < 6:

        st.error(
            "Password must be at least 6 characters."
        )

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    else:

        existing_user = users_collection.find_one(
            {
                "$or": [
                    {"username": username},
                    {"email": email}
                ]
            }
        )

        if existing_user:

            st.error(
                "Username or Email already exists."
            )

        else:

            users_collection.insert_one(
    {
        "username": username,
        "email": email,
        "password": password,
        "role": "User",

        "points": 0,

        "badge": "🌱 Beginner"
    }
)

            st.success(
                "Account created successfully ✅"
            )

            st.info(
                "Redirecting to login..."
            )

            st.switch_page(
                "login.py"
            )

# ====================================
# LOGIN LINK
# ====================================

st.divider()

st.markdown(
    "<center><b>Already have an account?</b></center>",
    unsafe_allow_html=True
)

if st.button(
    "🔐 Login",
    use_container_width=True
):

    st.switch_page(
        "login.py"
    )