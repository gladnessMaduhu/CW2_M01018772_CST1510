import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Cybersecurity", layout="wide")

# ---------- Login check ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("Home")
    st.stop()

st.title("Cybersecurity Analytics")

# ---------- Load CSV ----------
@st.cache_data
def load_data():
    # Project root (two levels up from pages folder)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    csv_path = os.path.join(project_root, "DATA", "cyber_incidents.csv")

    if not os.path.exists(csv_path):
        st.error(f"CSV file not found at {csv_path}")
        return pd.DataFrame()  # return empty dataframe to avoid crash

    df = pd.read_csv(csv_path)
    return df

df = load_data()

# Stop if CSV failed to load
if df.empty:
    st.stop()

# ---------- Sidebar Filters ----------
with st.sidebar:
    st.header("Filters")

    # Filter by year
    if "Year" in df.columns:
        years = df["Year"].dropna().unique()
        selected_year = st.selectbox("Year", sorted(years))
    else:
        selected_year = None

    # Filter by incident type
    if "IncidentType" in df.columns:
        types = df["IncidentType"].dropna().unique()
        selected_types = st.multiselect("Incident Type", types, types)
    else:
        selected_types = []

# ---------- Filter Data ----------
filtered = df.copy()

if selected_year is not None:
    filtered = filtered[filtered["Year"] == selected_year]

if selected_types:
    filtered = filtered[filtered["IncidentType"].isin(selected_types)]

st.subheader("Filtered Cyber Incidents")
st.dataframe(filtered, use_container_width=True)

# ---------- Charts ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incidents by Month")
    if "Month" in filtered.columns:
        monthly_counts = filtered.groupby("Month").size()
        st.line_chart(monthly_counts)
    else:
        st.info("No 'Month' column in data.")

with col2:
    st.subheader("Incidents by Type")
    if "IncidentType" in filtered.columns:
        st.bar_chart(filtered["IncidentType"].value_counts())
    else:
        st.info("No 'IncidentType' column in data.")
