import streamlit as st
import config
import mock_api
import time
from streamlit_mic_recorder import speech_to_text

# Page Configuration (Updated)
st.set_page_config(
    page_title="Omotenashi Care",
    page_icon="⛩️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS & FONTS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css("omotenashi-care/styles.css")
except FileNotFoundError:
    # Fallback for local testing if running from inside the directory
    try:
        load_css("styles.css")
    except:
        st.error("CSS file not found.")

# --- SESSION STATE ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'patient_lang' not in st.session_state:
    st.session_state.patient_lang = "en" # Default to English
if 'session_active' not in st.session_state:
    st.session_state.session_active = False
if 'clinical_summary' not in st.session_state:
    st.session_state.clinical_summary = None
if 'last_patient_input' not in st.session_state:
    st.session_state.last_patient_input = ""
if 'last_voice_input' not in st.session_state:
    st.session_state.last_voice_input = ""
if 'last_doc_input' not in st.session_state:
    st.session_state.last_doc_input = ""

# --- HEADER ---
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">⛩️ Omotenashi Care</h1>
        <div class="header-subtitle">AI-Powered Medical Communication Bridge</div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.session_active:
    st.markdown("""
        <div class="session-banner">
            <span>🟢 Session Active / 通話中</span>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col_patient, col_doctor = st.columns(2)

# ================= PATIENT PANEL =================
with col_patient:
    st.markdown('<div class="panel-container patient-panel">', unsafe_allow_html=True)
    st.markdown("<h2>Patient (患者)</h2>", unsafe_allow_html=True)
    
    # 1. Language Selector
    selected_lang_code = st.selectbox(
        "Select your language / 言語を選択してください",
        options=list(config.LANGUAGES.keys()),
        format_func=lambda x: config.LANGUAGES[x],
        index=list(config.LANGUAGES.keys()).index(st.session_state.patient_lang)
    )
    st.session_state.patient_lang = selected_lang_code

    # API Key Configuration (Sidebar)
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("### API Keys")
        minimax_key = st.text_input("MiniMax API Key", type="password", help="Enter your MiniMax API Key here")
        agora_app_id = st.text_input("Agora App ID", type="password", help="Enter your Agora App ID here")
        
        if minimax_key:
            st.session_state['MINIMAX_API_KEY'] = minimax_key
        if agora_app_id:
            st.session_state['AGORA_APP_ID'] = agora_app_id
            
        st.markdown("---")
        # Display current status
        current_mm_key = st.session_state.get('MINIMAX_API_KEY') or config.MINIMAX_API_KEY
        if current_mm_key and "sk-" in current_mm_key:
             st.success("✅ MiniMax API Key Configured")
        else:
             st.warning("⚠️ Running in Mock Mode")


    # 2. Start Session Button
    if not st.session_state.session_active:
        st.write("") # Spacer
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("Start Session / セッションを開始", key="start_session"):
            st.session_state.session_active = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Input Method (Text / Dictation)
    st.info("🎙️ Speak directly into your microphone (English supported)")
    
    # Use streamlit-mic-recorder
    text_from_speech = speech_to_text(
        language='en',
        start_prompt="🎤 Start Recording",
        stop_prompt="🛑 Stop Recording",
        just_once=True,
        key='STT'
    )
    
    if text_from_speech:
        st.session_state.last_voice_input = text_from_speech

    patient_input = st.text_area(
        "Describe your symptoms / 症状を教えてください",
        value=st.session_state.get("last_voice_input", ""),
        height=120,
        placeholder="Type here or use the microphone button above..."
    )
    
    # 4. Send Button
    st.markdown('<div class="send-btn">', unsafe_allow_html=True)
    if st.button("Send to Doctor / 医師に送る", key="send_patient"):
        if patient_input:
            # Auto-start session if needed
            if not st.session_state.session_active:
                st.session_state.session_active = True
                
            with st.spinner("Translating & Analyzing..."):
                # Call Mock API (or Real if key exists)
                minimax_key = st.session_state.get('MINIMAX_API_KEY') or config.MINIMAX_API_KEY
                result = mock_api.process_patient_input(
                    patient_input, 
                    st.session_state.patient_lang,
                    api_key=minimax_key
                )
                
                if result:
                    # Update State
                    st.session_state.last_patient_input = patient_input
                    st.session_state.clinical_summary = result
                    st.session_state.messages.append({"role": "patient", "content": patient_input})
                    st.rerun()
                else:
                    st.error("Analysis failed. Please check API Key or try again.")
        else:
            st.warning("Please enter your symptoms.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. Transcript & History
    if st.session_state.messages:
        st.markdown("### Conversation / 会話")
        for msg in reversed(st.session_state.messages):
            if msg['role'] == "patient":
                st.markdown(f"""
                    <div class="transcript-box">
                        <strong>You:</strong><br>{msg['content']}
                    </div>
                """, unsafe_allow_html=True)
            elif msg['role'] == "doctor":
                # 6. Doctor's Reply (Gold Box)
                st.markdown(f"""
                    <div class="translation-box">
                        <strong>Doctor (Translated):</strong><br>{msg['content']}
                    </div>
                """, unsafe_allow_html=True)
                
                # Check for audio if present
                if msg.get('audio_bytes'):
                     st.audio(msg['audio_bytes'], format="audio/mp3")

    st.markdown('</div>', unsafe_allow_html=True) # End Patient Panel

# ================= DOCTOR PANEL =================
with col_doctor:
    st.markdown('<div class="panel-container doctor-panel">', unsafe_allow_html=True)
    st.markdown("<h2>Doctor (医師)</h2>", unsafe_allow_html=True)

    # 1. Empty State
    if not st.session_state.session_active:
        st.info("Waiting for patient to start session... / 患者の開始を待機中...")
    
    elif not st.session_state.clinical_summary:
        st.info("Waiting for patient input... / 患者の入力を待機中...")
    
    else:
        summary = st.session_state.clinical_summary
        
        # 2. Sentiment + Urgency Tags
        sentiment = summary.get('sentiment', 'confused')
        urgency = summary.get('urgency', 'low')
        
        st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <span class="tag tag-sentiment-{sentiment}">Sentiment: {sentiment.upper()}</span>
                <span class="tag tag-urgency-{urgency}">Urgency: {urgency.upper()}</span>
            </div>
        """, unsafe_allow_html=True)

        # 3. Japanese Translation
        st.markdown("<h4>Translation (JP)</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 8px; border-left: 4px solid {config.COLORS['indigo']}; margin-bottom: 15px;">
                {summary.get('translation_jp', '')}
            </div>
        """, unsafe_allow_html=True)

        # 4. Detected Symptoms
        st.markdown("<h4>Detected Symptoms</h4>", unsafe_allow_html=True)
        symptoms_html = ''.join([f'<span class="symptom-pill">{s}</span>' for s in summary.get('symptoms', [])])
        st.markdown(f"<div>{symptoms_html}</div>", unsafe_allow_html=True)
        st.write("") # Spacer

        # 5. Clinical Note
        st.markdown("<h4>Clinical Note</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="clinical-note">
                {summary.get('doctor_summary', '')}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 6. Doctor Response
        st.markdown("<h4>Doctor's Reply / 医師の返信</h4>", unsafe_allow_html=True)
        
        # Voice Input for Doctor
        doc_voice_text = speech_to_text(
            language='ja', # Default to Japanese for doctor
            start_prompt="🎤 Record Reply",
            stop_prompt="🛑 Stop",
            just_once=True,
            key='doc_STT'
        )
        
        # If voice input is captured, update the text area's session state
        if doc_voice_text:
            st.session_state.doc_input_area = doc_voice_text
            
        doctor_input = st.text_area(
            "Type or Speak your response:", 
            height=100, 
            placeholder="Speak or type response here...", 
            key="doc_input_area"
        )
        
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        if st.button("Send & Translate / 送信・翻訳", key="send_doctor"):
            if doctor_input:
                with st.spinner("Translating to Patient's Language..."):
                    # Call Mock API (or Real if key exists)
                    minimax_key = st.session_state.get('MINIMAX_API_KEY') or config.MINIMAX_API_KEY
                    translated_response = mock_api.process_doctor_response(
                        doctor_input, 
                        st.session_state.patient_lang,
                        api_key=minimax_key
                    )
                    
                    # Generate Audio (TTS)
                    audio_data = mock_api.generate_audio_response(
                        translated_response, 
                        st.session_state.patient_lang
                    )
                    
                    # Update State
                    st.session_state.messages.append({
                        "role": "doctor", 
                        "content": translated_response,
                        "audio_bytes": audio_data
                    })
                    
                    # Clear input after sending
                    st.session_state.doc_input_area = ""
                    
                    st.rerun()
            else:
                st.warning("Please enter a response.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # End Doctor Panel

# Footer
st.markdown("---")
st.caption("Powered by TRAE + MiniMax + Agora | Hackathon Build")
