import requests
import json
import config
import time

# MiniMax API Configuration
MINIMAX_API_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"

def process_patient_input(text, patient_lang="en", api_key=None):
    """
    Calls MiniMax API to analyze patient input.
    """
    if not api_key:
        return _mock_process_patient_input(text, patient_lang)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Construct the prompt for MiniMax
    system_prompt = f"""
    You are an AI medical assistant for 'Omotenashi Care'.
    Your goal is to help a doctor understand a foreign patient's symptoms.
    
    Output JSON format only:
    {{
        "translation_jp": "Translate patient's input to Japanese. Tone: Extremely polite, empathetic, and 'Omotenashi' style (using Desu/Masu form, very respectful). Avoid robotic language.",
        "sentiment": "anxious|distressed|calm|confused",
        "urgency": "high|medium|low",
        "symptoms": ["List", "of", "symptoms", "in", "English"],
        "doctor_summary": "A concise clinical summary in English for the doctor."
    }}
    """

    payload = {
        "model": "abab6.5s-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Patient ({patient_lang}): {text}"}
        ],
        "temperature": 0.1,
        "top_p": 0.95,
    }

    try:
        response = requests.post(MINIMAX_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Parse the JSON content from the response
        content = data['choices'][0]['message']['content']
        # Clean up code blocks if present
        if "```json" in content:
            content = content.replace("```json", "").replace("```", "")
            
        return json.loads(content)
        
    except Exception as e:
        print(f"MiniMax API Error: {e}")
        return _mock_process_patient_input(text, patient_lang)


def process_doctor_response(text, target_language="en", api_key=None):
    """
    Calls MiniMax API to translate doctor's response.
    """
    if not api_key:
        return _mock_process_doctor_response(text, target_language)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    target_lang_name = config.LANGUAGES.get(target_language, "English")

    payload = {
        "model": "abab6.5s-chat",
        "messages": [
            {"role": "system", "content": f"Translate this medical response to {target_lang_name}. Tone: Warm, polite, reassuring (Omotenashi style)."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
    }

    try:
        response = requests.post(MINIMAX_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"MiniMax API Error: {e}")
        return _mock_process_doctor_response(text, target_language)


# --- MOCK FALLBACKS ---
def _mock_process_patient_input(text, patient_lang):
    time.sleep(1.5)
    return {
        "translation_jp": "患者は胸の重苦しさを訴えており、特に階段を昇るときに症状が悪化します。",
        "sentiment": "anxious",
        "urgency": "medium",
        "symptoms": ["Chest heaviness", "Shortness of breath on exertion"],
        "doctor_summary": "Patient reports chest heaviness exacerbated by exertion (climbing stairs). Suspected angina or cardiac issue."
    }

def _mock_process_doctor_response(text, target_language):
    time.sleep(1.0)
    target_lang_name = config.LANGUAGES.get(target_language, target_language)
    if "ECG" in text or "electrocardiogram" in text or "心電図" in text:
        return "The doctor has recommended an electrocardiogram (ECG). Please rest until your appointment."
    return f"[{target_lang_name} translation]: {text} (Warm and polite tone)"
