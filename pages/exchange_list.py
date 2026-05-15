import streamlit as st
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Exchange Listings",
    page_icon="📋",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📋 Exchange Listings")

# ---------------- RED BUTTON CSS ----------------
st.markdown("""
<style>
div.stButton > button {
    background-color: red;
    color: white;
    border-radius: 8px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
with open("data/exchange_data.json", "r") as file:
    data = json.load(file)

# ---------------- EMPTY LIST ----------------
if len(data) == 0:

    st.warning("No exchange items posted yet.")

# ---------------- SHOW ITEMS ----------------
else:

    for index, item in enumerate(data):

        col1, col2 = st.columns([4, 1])

        # --------------------------------------
        # ITEM DETAILS
        # --------------------------------------
        with col1:

            st.image(item["image"], width=250)

            st.write(f"Category: {item['category']}")

            st.write(
                f"Location: {item['latitude']}, {item['longitude']}"
            )

        # --------------------------------------
        # DELETE SECTION
        # --------------------------------------
        with col2:

            # Delete Button
            if st.button(
                "Delete",
                key=f"delete_{index}"
            ):

                st.session_state[
                    f"confirm_delete_{index}"
                ] = True

            # Confirmation Box
            if st.session_state.get(
                f"confirm_delete_{index}",
                False
            ):

                st.warning("Are you sure?")

                yes_col, no_col = st.columns(2)

                # YES
                with yes_col:

                    if st.button(
                        "Yes",
                        key=f"yes_{index}"
                    ):

                        data.pop(index)

                        with open(
                            "data/exchange_data.json",
                            "w"
                        ) as file:

                            json.dump(
                                data,
                                file,
                                indent=4
                            )

                        st.success("Item Deleted ✅")

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

        st.divider()