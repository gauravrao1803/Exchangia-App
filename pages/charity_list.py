import streamlit as st
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Charity Listings",
    page_icon="📋",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0f172a;
    color: white;
}

/* Card */
.item-card {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.05);
}

/* Title */
.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: white;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<p class="title">📋 Charity Listings</p>',
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ----------------
with open("data/charity_data.json", "r") as file:
    data = json.load(file)

# ---------------- EMPTY LIST ----------------
if len(data) == 0:

    st.warning("No charity items posted yet.")

# ---------------- SHOW ITEMS ----------------
else:

    for index, item in enumerate(data):

        with st.container():

            st.markdown(
                '<div class="item-card">',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([3, 1])

            # ----------------------------------
            # LEFT SIDE
            # ----------------------------------
            with col1:

                st.image(
                    item["image"],
                    width=300
                )

                st.subheader(
                    f"📦 {item['category']}"
                )

                st.write(
                    f"📍 {item['location']}"
                )

                # Status
                status = item.get(
                    "status",
                    "Pending"
                )

                if status == "Approved":

                    st.success(
                        f"✅ Status: {status}"
                    )

                elif status == "Denied":

                    st.error(
                        f"❌ Status: {status}"
                    )

                else:

                    st.warning(
                        f"⏳ Status: {status}"
                    )

            # ----------------------------------
            # RIGHT SIDE
            # ----------------------------------
            with col2:

                st.subheader("Admin")

                # APPROVE
                if st.button(
                    "✅ Approve",
                    key=f"approve_{index}"
                ):

                    data[index]["status"] = "Approved"

                    with open(
                        "data/charity_data.json",
                        "w"
                    ) as file:

                        json.dump(
                            data,
                            file,
                            indent=4
                        )

                    st.rerun()

                # DENY
                if st.button(
                    "❌ Deny",
                    key=f"deny_{index}"
                ):

                    data[index]["status"] = "Denied"

                    with open(
                        "data/charity_data.json",
                        "w"
                    ) as file:

                        json.dump(
                            data,
                            file,
                            indent=4
                        )

                    st.rerun()

                # DELETE
                if st.button(
                    "🗑 Delete",
                    key=f"delete_{index}"
                ):

                    st.session_state[
                        f"confirm_delete_{index}"
                    ] = True

                # CONFIRM DELETE
                if st.session_state.get(
                    f"confirm_delete_{index}",
                    False
                ):

                    st.warning(
                        "Are you sure?"
                    )

                    yes_col, no_col = st.columns(2)

                    # YES
                    with yes_col:

                        if st.button(
                            "Yes",
                            key=f"yes_{index}"
                        ):

                            data.pop(index)

                            with open(
                                "data/charity_data.json",
                                "w"
                            ) as file:

                                json.dump(
                                    data,
                                    file,
                                    indent=4
                                )

                            st.rerun()

                    # NO
                    with no_col:

                        if st.button(
                            "No",
                            key=f"no_{index}"
                        ):

                            st.session_state[
                                f"confirm_delete_{index}"
                            ] = False

                            st.rerun()

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )