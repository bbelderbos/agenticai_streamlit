"""
Build `add_expense.py` with a `render(client, user_id: int)` function that renders a form with:
- Call `st.header("Add Expense")` first, before the form
- `st.text_input` for the expense description inside `with st.form("add_expense_form")`
- Check `if submitted and description.strip()` after the form block (not inside it)
- Call `client.classify_expense(description, user_id)` inside `st.spinner` and display the result with `st.success(...)` — the message must include the category name (e.g. `"Food"`) since the test asserts `"Food" in at.success[0].value`
- Show `st.warning(...)` when the description is empty
- On `RequestError`, show `st.error(...)` containing "Cannot connect" — the test asserts on that substring
"""

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
