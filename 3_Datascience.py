import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data Science", layout="wide")

# ---------- Login check ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("Home")
    st.stop()

st.title("Data Science Dashboard")

# ---------- Load CSVs ----------
@st.cache_data
def load_datasets():
    # Go to project root (two levels up from pages folder)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # datasets_metadata.csv
    meta_path = os.path.join(project_root, "DATA", "datasets_metadata.csv")
    if not os.path.exists(meta_path):
        st.error(f"File not found: {meta_path}")
        df_meta = pd.DataFrame()
    else:
        df_meta = pd.read_csv(meta_path)

    # cyber_incidents.csv
    incidents_path = os.path.join(project_root, "DATA", "cyber_incidents.csv")
    if not os.path.exists(incidents_path):
        st.warning(f"File not found: {incidents_path}")
        df_incidents = pd.DataFrame()
    else:
        df_incidents = pd.read_csv(incidents_path)

    return df_meta, df_incidents

df_meta, df_incidents = load_datasets()

# Stop if no data loaded
if df_meta.empty and df_incidents.empty:
    st.stop()

# ---------- Display datasets metadata ----------
if not df_meta.empty:
    st.subheader("Datasets Metadata")
    st.dataframe(df_meta, use_container_width=True)

# ---------- Analyze cyber incidents ----------
if not df_incidents.empty:
    st.subheader("Cyber Incidents Overview")

    # Incidents per year
    if "Year" in df_incidents.columns:
        incidents_per_year = df_incidents.groupby("Year").size()
        st.line_chart(incidents_per_year)
    else:
        st.info("No 'Year' column in cyber incidents data.")

    # Incident type distribution
    if "IncidentType" in df_incidents.columns:
        st.bar_chart(df_incidents["IncidentType"].value_counts())
    else:
        st.info("No 'IncidentType' column in cyber incidents data.")

    # Optional: filter by year and type
    with st.sidebar:
        st.header("Filters")
        selected_year = st.selectbox("Year", sorted(df_incidents["Year"].dropna().unique())) if "Year" in df_incidents.columns else None
        selected_types = st.multiselect("Incident Type", df_incidents["IncidentType"].dropna().unique(), df_incidents["IncidentType"].dropna().unique()) if "IncidentType" in df_incidents.columns else []

    filtered = df_incidents.copy()
    if selected_year:
        filtered = filtered[filtered["Year"] == selected_year]
    if selected_types:
        filtered = filtered[filtered["IncidentType"].isin(selected_types)]

    st.subheader("Filtered Cyber Incidents")
    st.dataframe(filtered, use_container_width=True)
