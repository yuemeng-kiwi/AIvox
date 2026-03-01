import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# API Keys (Mock or Real)
# Prioritize Session State keys (from UI) -> Env Vars -> Hardcoded Fallback
MINIMAX_API_KEY = st.session_state.get('MINIMAX_API_KEY') or os.getenv("MINIMAX_API_KEY", "sk-cp-K2-kmmZVFekS6M4Cdsrb9Mfrfktg7erB7MeE6EUlBpjuXiXu2Q7Wh0WkJR8IviAcbXwxB3OfDOYqBDTXNjtBGUZHalt3QyJxxdnotcQp_2E-b4WrwEuGqvU")
AGORA_APP_ID = st.session_state.get('AGORA_APP_ID') or os.getenv("AGORA_APP_ID", "mock_agora_app_id")

# Feature Flags
ENABLE_MOCK_MODE = not (st.session_state.get('MINIMAX_API_KEY') or os.getenv("MINIMAX_API_KEY"))
ENABLE_VOICE = False     # Phase 2 feature

# MiniMax Config
MINIMAX_API_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"
MINIMAX_MODEL = "abab6.5s-chat"

# Supported Languages
LANGUAGES = {
    "en": "English",
    "ja": "Japanese",
    "th": "Thai",
    "vi": "Vietnamese",
    "zh": "Chinese",
    "ko": "Korean",
    "id": "Indonesian",
    "tl": "Tagalog",
    "hi": "Hindi",
    "ar": "Arabic",
    "es": "Spanish"
}

# UI Colors
COLORS = {
    "parchment": "#F9F5EE",
    "torii": "#C0392B",
    "matcha": "#4A7C59",  # Updated to calm green
    "indigo": "#2C3E7A",  # Doctor panel professional blue
    "gold": "#B8860B",    # Translated response warm gold
    "ink": "#1A1208",     # Text
    "text_light": "#FFFFFF"
}

# MiniMax Prompt Template
MINIMAX_SYSTEM_PROMPT = """
You are a compassionate AI medical communication assistant for Omotenashi Care.
A foreign patient in Japan has described their symptoms. Your role is to:

1. Translate their message into natural Japanese
2. Extract specific medical symptoms as a list
3. Assess their emotional sentiment: anxious | calm | distressed | confused
4. Rate clinical urgency: low | medium | high
5. Write a concise, professional clinical note in Japanese for the doctor

Respond ONLY with valid JSON — no markdown, no explanation:
{
"translation_jp": "natural Japanese translation",
"symptoms": ["symptom 1", "symptom 2", "symptom 3"],
"sentiment": "anxious",
"urgency": "high",
"doctor_summary": "concise clinical note in Japanese"
}
"""
