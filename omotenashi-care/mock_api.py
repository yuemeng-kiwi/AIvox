import time
import random
import config

def process_patient_input(text, language):
    """
    Simulates processing patient input.
    Returns a dictionary with translation_jp, symptoms, sentiment, urgency, doctor_summary.
    """
    if config.ENABLE_MOCK_MODE:
        time.sleep(1.5)  # Simulate API latency
        
        text_lower = text.lower()
        
        # Default mock response
        response = {
            "translation_jp": "（翻訳されたテキスト）",
            "symptoms": ["不明"],
            "sentiment": "confused",
            "urgency": "low",
            "doctor_summary": "主訴：不明。詳細は問診が必要です。"
        }

        # Specific mock cases based on keywords (simulating understanding)
        # Demo Scenario Case
        if "heaviness in my chest" in text_lower and "climbing stairs" in text_lower:
             response = {
                "translation_jp": "階段を上るときに特に胸が重く感じます。毎朝めまいもあります。",
                "symptoms": ["Chest heaviness on exertion", "Morning dizziness", "Possible dyspnea"],
                "sentiment": "anxious",
                "urgency": "high",
                "doctor_summary": "患者は労作時の胸部圧迫感と起立性めまいを訴えています。心臓疾患の可能性を考慮し、心電図検査を優先してください。"
            }
        elif "heavy" in text_lower or "chest" in text_lower or "heart" in text_lower:
            response = {
                "translation_jp": "「胸が苦しいです。ここに圧迫感があります。」",
                "symptoms": ["胸部圧迫感", "心臓不安", "呼吸困難の可能性"],
                "sentiment": "anxious", 
                "urgency": "high",
                "doctor_summary": "主訴：胸部の圧迫感。患者は強い不安を感じており、心疾患のリスクを考慮する必要があります。早急な診察を推奨。"
            }
        elif "head" in text_lower or "ache" in text_lower or "pain" in text_lower:
             response = {
                "translation_jp": "「頭が痛いです。ズキズキします。」",
                "symptoms": ["頭痛", "疼痛"],
                "sentiment": "distressed",
                "urgency": "medium",
                "doctor_summary": "主訴：頭痛。疼痛レベルは中程度。継続的な痛みにより苦痛を感じている様子。"
            }
        elif "stomach" in text_lower or "belly" in text_lower:
             response = {
                "translation_jp": "「お腹が痛いです。」",
                "symptoms": ["腹痛", "胃部不快感"],
                "sentiment": "distressed",
                "urgency": "medium",
                "doctor_summary": "主訴：腹痛。消化器系の異常の可能性。"
            }
        
        return response

    else:
        # TODO: Implement Real MiniMax API call here
        pass

def process_doctor_response(text, target_language):
    """
    Simulates processing doctor response.
    Returns a translation and optionally audio data (mocked).
    """
    if config.ENABLE_MOCK_MODE:
        time.sleep(1.0)
        target_lang_name = config.LANGUAGES.get(target_language, target_language)
        
        # Specific mock response for the demo scenario
        if "ECG" in text or "electrocardiogram" in text or "心電図" in text:
            translated_text = "The doctor has recommended an electrocardiogram (ECG). Please rest until your appointment."
        else:
            translated_text = f"[{target_lang_name} translation]: {text} (Warm and polite tone)"
            
        # In a real app, this would return audio bytes from MiniMax T2A
        # For mock, we return just text, but the UI can use st.audio if we had a file
        return translated_text

    else:
        # TODO: Implement Real MiniMax API call here
        pass
