import streamlit as st
from decouple import config

from api_client import ExpenseAPIClient
from views import add_expense, dashboard, expenses

st.set_page_config(page_title="Expense Tracker", layout="wide")


def check_password():
    if st.session_state.get("authenticated"):
        return True

    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == st.secrets.get(
            "APP_PASSWORD", config("APP_PASSWORD", default="")
        ):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False


if not check_password():
    st.stop()

API_BASE_URL = st.secrets.get("API_BASE_URL") or config(
    "API_BASE_URL", default="http://localhost:8000/api/v1"
)
client = ExpenseAPIClient(base_url=API_BASE_URL)

with st.sidebar:
    st.title("Expense Tracker")
    user_id_input = st.text_input("User ID", value="12345", key="sidebar_user_id")
    user_id = int(user_id_input) if user_id_input.strip().isdigit() else None
    page = st.radio("Navigate", ["Dashboard", "Expenses", "Add Expense"])

if page == "Dashboard":
    dashboard.render(client, user_id)
elif page == "Expenses":
    expenses.render(client, user_id)
elif page == "Add Expense":
    add_expense.render(client, user_id)
