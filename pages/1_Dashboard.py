import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard", layout="wide")

# ---------- Session check ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: only allow logged-in users
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go back to login"):
        st.switch_page("pages/Home.py")
    st.stop()

# ---------- Dashboard content ----------
st.title("📊 Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    n_points = st.slider("Number of data points", 10, 200, 50)

# Fake data
data = pd.DataFrame(np.random.randn(n_points, 3), columns=["A", "B", "C"])

# Layout: two charts side by side
col1, col2 = st.columns(2)
with col1:
    st.subheader("Line chart")
    st.line_chart(data)
with col2:
    st.subheader("Bar chart")
    st.bar_chart(data)

# Raw data in an expander
with st.expander("See raw data"):
    st.dataframe(data)

