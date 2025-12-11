from csv import excel

import google.generativeai as genai
import streamlit as st

# ---------- Configure Gemini API ----------
genai.configure(api_key="AIzaSyAG1C8gYVQhcNBSME5-8d8WPnO2H5Ocfj4")  # keep this hardcoded for now
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.client(api_key = API_KEY)
except (KeyError,ValueError):
    st.error("API key not found.")
    st.stop()
except Exception as e:
    st.error(e)
    st.stop()

# ---------- Make a simple API call ----------

# Make a simple text-based completion (old API)
response = genai.Completion.create(
    model="models/text-bison-001",  # compatible model in v0.8.5
    prompt="You are a helpful assistant. \nUser: Hello! What is AI?\nAssistant:",
    max_output_tokens=200
)

# ---------- Print the AI response ----------
# Gemini AI returns a list of candidates; usually we take the first one
print(response.candidates[0].content)
