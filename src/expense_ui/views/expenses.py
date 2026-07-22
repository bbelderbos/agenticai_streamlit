"""
Build `expenses.py` with a `render(client, user_id: int)` function that fetches `client.get_expenses(user_id)` and renders a row per expense using `st.columns`:
- Call `st.header("Expenses")` first, before the `try` block
- Left column: category, amount, currency, description
- Right column: `st.button("Delete", key=f"del_{item['id']}")` that calls `client.delete_expense(item["id"])` then `st.rerun()` to refresh the list
- Show `st.info(...)` when the list is empty
- Wrap in `try/except RequestError` and include "Cannot connect" in the `st.error(...)` message — the test asserts on that substring
"""

import streamlit as st
from httpx import RequestError


def render(client, user_id):
    st.header("Expenses")

    try:
        expenses = client.get_expenses(user_id)
    except RequestError as e:
        print(f"[API] RequestError in get_expenses: {e}")
        st.error("Cannot connect to the expenses service.")
        return

    if not expenses:
        st.info("No expenses found. Add some to get started!")
        return

    for item in expenses:
        col1, col2 = st.columns([3, 1])
        with col1:
            amount = f"{float(item['amount']):.2f}"
            st.write(
                f"{item['category']}: {amount} {item['currency']} - {item['description']}"
            )
        with col2:
            if st.button("Delete", key=f"del_{item['id']}"):
                client.delete_expense(item["id"])
                st.rerun()
