import streamlit as st
import pandas as pd
import google.generativeai as genai
import sqlite3
import os

st.set_page_config(page_title="AI Assistant", layout="wide")

# ---------------- Session Check ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.error("You must be logged in to use the AI assistant.")
    if st.button("Go to Login"):
        st.switch_page("Home")
    st.stop()

# ---------------- Configure Gemini ----------------
API_KEY = "AIzaSyBt5mHvvp_y6IZ2NvD6pKI2SGFKbcw14WE"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- Chat Memory ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("AI Assistant")
st.write("Ask me anything related to cybersecurity, data, or your datasets.")

# ---------------- Sidebar: DB Query Tool ----------------
with st.sidebar:
    st.header("Database Query (Optional)")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # CORRECT database path (2 levels up)
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
    DB_PATH = os.path.join(PROJECT_ROOT, "DATA", "intelligence_platform.db")

    # Connect safely
    if not os.path.exists(DB_PATH):
        st.error(f"Database not found at: {DB_PATH}")
    else:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [t[0] for t in tables]

        selected_table = st.selectbox("Select Table", tables)

        if st.button("Show Table Data"):
            df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
            st.dataframe(df, use_container_width=True)

        conn.close()

# ---------------- Display Previous Messages ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- Chat Input ----------------
prompt = st.chat_input("Type your message...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            answer = response.text

        except Exception as e:
            answer = f"⚠️ Error: {e}"

        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
