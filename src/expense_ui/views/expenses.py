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
