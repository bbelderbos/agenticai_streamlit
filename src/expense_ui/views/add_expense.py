import streamlit as st
from httpx import RequestError


def render(client, user_id: int):
    st.header("Add Expense")

    with st.form("add_expense_form"):
        description = st.text_input("Expense Description")
        submitted = st.form_submit_button("Classify Expense")

    if submitted:
        if not description.strip():
            st.warning("Please enter an expense description.")
            return

        with st.spinner("Classifying expense..."):
            try:
                result = client.classify_expense(description, user_id)
                category = result.get("category", "Unknown")
                st.success(f"Expense classified as: {category}")
            except RequestError as e:
                print(f"[API] RequestError in classify_expense: {e}")
                st.error("Cannot connect to the classification service.")
