from typing import List, Dict, Optional
import google.generativeai as genai
import streamlit as st

class AIAssistant:
    """
    AI Assistant wrapper class for chat models.
    Handles message history and AI responses.
    Can be adapted to Gemini AI or other providers.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash", system_prompt: str = None):
        # Configure Gemini AI if API key is provided
        if api_key:
            genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(model_name)
        self._system_prompt = system_prompt or (
            "You are a helpful assistant. Answer questions clearly and concisely."
        )
        self._history: List[Dict[str, str]] = []

    def set_system_prompt(self, prompt: str):
        """Update the system prompt for the AI."""
        self._system_prompt = prompt

    def send_message(self, user_message: str) -> str:
        """
        Send a message to the AI model and return the response.
        Stores the conversation in history.
        """
        # Store user message
        self._history.append({"role": "user", "parts": [{"text": user_message}]})

        # Build messages for Gemini API
        messages = [{"role": "system", "parts": [{"text": self._system_prompt}]}] + self._history

        try:
            # Call Gemini AI
            response = self.model.generate_content(messages)
            answer = response.text
        except Exception as e:
            answer = f"⚠️ Error: {e}"

        # Store assistant response
        self._history.append({"role": "model", "parts": [{"text": answer}]})

        return answer

    def get_history(self) -> List[Dict[str, str]]:
        """Return the conversation history."""
        return self._history

    def clear_history(self):
        """Clear the conversation history."""
        self._history.clear()
