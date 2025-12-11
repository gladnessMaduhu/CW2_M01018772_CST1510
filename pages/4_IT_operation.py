import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="IT Operations", layout="wide")

# ---------- Login check ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("Home")
    st.stop()

st.title("IT Operations | Intelligence Platform")

# ---------- Database connection ----------
# Get absolute path to project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
db_path = os.path.join(project_root, "DATA", "intelligence_platform.db")


if not os.path.exists(db_path):
    st.error(f"Database file not found at {db_path}")
    st.stop()

# Connect to your existing database
conn = sqlite3.connect(db_path)

# Get list of tables
tables_df = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
tables = tables_df["name"].tolist()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Database Tables")
    selected = st.selectbox("Select Table", tables)

# ---------- Read Selected Table ----------
df = pd.read_sql_query(f"SELECT * FROM {selected}", conn)

st.subheader(f"Table: {selected}")
st.dataframe(df, use_container_width=True)

# ---------- Numeric Trend ----------
numeric_cols = df.select_dtypes(include=["int", "float"]).columns

if len(numeric_cols) > 0:
    st.subheader("Numeric Trend")
    column_to_plot = st.selectbox("Column", numeric_cols)
    st.line_chart(df[column_to_plot])
else:
    st.info("No numeric columns found.")
