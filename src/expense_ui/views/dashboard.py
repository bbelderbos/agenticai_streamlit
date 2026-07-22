"""
Build dashboard.py — fetch client.get_summary(user_id) and render two Plotly charts:

Pie chart of summary["category_totals"] — px.pie(names=..., values=[float(v) for v in ...])
Bar chart of summary["monthly_totals"] — px.bar(x=..., y=[float(v) for v in ...])
Show st.info(...) for each chart section when the data dict is empty
Wrap in try/except HTTPStatusError, RequestError and show st.error(...) on failure
Note: Decimal values come back from the API as strings, so convert with float(v) before passing to Plotly
"""

import streamlit as st
from httpx import HTTPStatusError, RequestError
from plotly import express as px


def render(client, user_id):
    st.header("Dashboard")
    try:
        summary = client.get_summary(user_id)

        st.header("Category Totals")
        if not summary["category_totals"]:
            st.info("No category totals data available.")
        else:
            fig_pie = px.pie(
                names=list(summary["category_totals"].keys()),
                values=[float(v) for v in summary["category_totals"].values()],
            )
            st.plotly_chart(fig_pie)

        st.header("Monthly Totals")
        if not summary["monthly_totals"]:
            st.info("No monthly totals data available.")
        else:
            fig_bar = px.bar(
                x=list(summary["monthly_totals"].keys()),
                y=[float(v) for v in summary["monthly_totals"].values()],
            )
            fig_bar.update_xaxes(type="category")
            st.plotly_chart(fig_bar)

    except HTTPStatusError as e:
        print(f"[API] HTTPStatusError in get_summary: {e.response.status_code} - {e.response.text}")
        st.error(f"Cannot connect to server: {e.response.status_code}")
    except RequestError as e:
        print(f"[API] RequestError in get_summary: {e}")
        st.error("Cannot connect to the server. Please try again later.")
