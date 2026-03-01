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
    You are an AI medical interpreter.
    Your goal is to translate a patient's description into professional Japanese medical terminology for a doctor.
    
    Output JSON format only:
    {{
        "translation_jp": "Translate patient's input to Japanese using standard medical terminology (e.g., '胸部不快感' instead of '胸が変'). Be precise and clinical.",
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
            {"role": "system", "content": f"You are a caring medical assistant ('Omotenashi Care'). Translate this doctor's message to {target_lang_name}. Tone: Extremely warm, reassuring, and polite. Avoid cold medical jargon. Use simple words."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,  # Increased temperature for more natural/friendly tone
    }

    try:
        response = requests.post(MINIMAX_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"MiniMax API Error: {e}")
        return _mock_process_doctor_response(text, target_language)


from gtts import gTTS
import io

def generate_audio_response(text, lang_code="en"):
    """
    Generates audio from text using gTTS (Google Text-to-Speech).
    Returns: BytesIO object containing the audio.
    """
    try:
        # Map our config language codes to gTTS language codes
        # gTTS supports: 'en', 'ja', 'zh-CN', 'ko', 'es', etc.
        # Our config: 'en', 'ja', 'zh', 'ko', 'es'
        gtts_lang = lang_code
        if lang_code == 'zh': gtts_lang = 'zh-CN'
        
        tts = gTTS(text=text, lang=gtts_lang)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

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
