import streamlit as st
import google.generativeai as genai

# ----------------- Configure Gemini -----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# ----------------- Page Title -----------------
st.title("🛡 Cybersecurity AI Assistant")

# ----------------- Initialize Session State -----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user",  # Gemini doesn't support 'system', so treat system as user
            "parts": [{
                "text": """
You are a cybersecurity expert assistant.
- Analyze incidents and threats
- Provide technical guidance
- Explain attack vectors and mitigations
- Use MITRE ATT&CK, CVE references when relevant
- Provide clear, actionable recommendations
Tone: Professional and technical
Format: Structured responses
"""
            }]
        }
    ]

# ----------------- Display Previous Messages -----------------
for message in st.session_state.messages:
    # Only display messages already submitted (skip initial "system as user" message)
    if "submitted" in message and message["submitted"]:
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(message["parts"][0]["text"])

# ----------------- Get User Input -----------------
prompt = st.chat_input("Ask about cybersecurity...")

if prompt:
    # ---- Display User Message ----
    with st.chat_message("user"):
        st.markdown(prompt)

    # ---- Store User Message (Gemini Format) ----
    st.session_state.messages.append({
        "role": "user",
        "parts": [{"text": prompt}],
        "submitted": True
    })

    # ---- Prepare Messages for Gemini ----
    gemini_messages = []
    for msg in st.session_state.messages:
        # Convert assistant role to 'model' for Gemini
        role = msg["role"]
        if role == "assistant":
            role = "model"
        gemini_messages.append({
            "role": role,
            "parts": msg["parts"]
        })

    # ---- Call Gemini API ----
    try:
        response = model.generate_content(gemini_messages)
        assistant_response = response.text
    except Exception as e:
        assistant_response = f"⚠️ Error: {e}"

    # ---- Display Assistant Message ----
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # ---- Store Assistant Message ----
    st.session_state.messages.append({
        "role": "assistant",  # keep 'assistant' for display; converted to 'model' for API
        "parts": [{"text": assistant_response}],
        "submitted": True
    })
