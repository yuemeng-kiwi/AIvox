import streamlit as st
import config
import mock_api
import time

# Page Configuration
st.set_page_config(
    page_title="Omotenashi Care",
    page_icon="⛩️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS & FONTS ---
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Serif+JP:wght@700&display=swap" rel="stylesheet">
    <style>
    :root {{
        --parchment: {config.COLORS['parchment']};
        --torii: {config.COLORS['torii']};
        --matcha: {config.COLORS['matcha']};
        --indigo: {config.COLORS['indigo']};
        --gold: {config.COLORS['gold']};
        --ink: {config.COLORS['ink']};
        --text-light: {config.COLORS['text_light']};
    }}

    /* Global Styles */
    .stApp {{
        background-color: var(--parchment);
        color: var(--ink);
        font-family: 'Noto Sans JP', sans-serif;
    }}
    
    h1, h2, h3 {{
        font-family: 'Noto Serif JP', serif;
        color: var(--ink);
    }}

    /* Header */
    .header-container {{
        text-align: center;
        padding: 20px 0;
        border-bottom: 2px solid var(--torii);
        margin-bottom: 20px;
        background-color: white;
    }}
    .header-title {{
        font-size: 2.5em;
        color: var(--torii);
        margin: 0;
    }}
    .header-subtitle {{
        font-size: 1.2em;
        color: var(--ink);
        opacity: 0.8;
    }}

    /* Session Banner */
    .session-banner {{
        background-color: var(--torii);
        color: white;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }}

    /* Panels */
    .panel-container {{
        border-radius: 15px;
        padding: 25px;
        height: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    
    .patient-panel {{
        background-color: rgba(74, 124, 89, 0.05); /* Light Matcha */
        border-top: 5px solid var(--matcha);
    }}
    
    .doctor-panel {{
        background-color: rgba(44, 62, 122, 0.05); /* Light Indigo */
        border-top: 5px solid var(--indigo);
    }}

    /* Buttons */
    .stButton>button {{
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }}
    
    /* Start Session Button */
    .start-btn>button {{
        background-color: var(--matcha);
        color: white;
        width: 100%;
        font-size: 1.2em;
    }}
    .start-btn>button:hover {{
        background-color: #3A6346;
    }}

    /* Send Button */
    .send-btn>button {{
        background-color: var(--torii);
        color: white;
        width: 100%;
    }}
    
    /* Tags & Pills */
    .tag {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: bold;
        margin-right: 8px;
        color: white;
    }}
    
    .tag-sentiment-anxious {{ background-color: var(--torii); }}
    .tag-sentiment-distressed {{ background-color: var(--gold); }}
    .tag-sentiment-calm {{ background-color: var(--matcha); }}
    .tag-sentiment-confused {{ background-color: var(--indigo); }}
    
    .tag-urgency-high {{ background-color: var(--torii); }}
    .tag-urgency-medium {{ background-color: var(--gold); }}
    .tag-urgency-low {{ background-color: var(--matcha); }}
    
    .symptom-pill {{
        display: inline-block;
        background-color: var(--matcha);
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        margin: 3px;
        font-size: 0.9em;
    }}

    /* Chat Bubbles */
    .transcript-box {{
        background-color: white;
        border-left: 4px solid var(--matcha);
        padding: 15px;
        margin: 15px 0;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    
    .translation-box {{
        background-color: #FFF8E1; /* Light Gold */
        border-left: 4px solid var(--gold);
        padding: 15px;
        margin: 15px 0;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}

    .clinical-note {{
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-top: 10px;
        font-family: 'Noto Serif JP', serif;
    }}

    </style>
""", unsafe_allow_html=True)

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
        st.markdown("If keys are not provided, the app will run in **Mock Mode**.")


    # 2. Start Session Button
    if not st.session_state.session_active:
        st.write("") # Spacer
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("Start Session / セッションを開始", key="start_session"):
            st.session_state.session_active = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # 3. Symptom Input
        patient_input = st.text_area(
            "Describe your symptoms / 症状を教えてください",
            height=120,
            placeholder="Type here... (e.g., I feel heavy in my chest)"
        )

        # 4. Send Button
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        if st.button("Send to Doctor / 医師に送る", key="send_patient"):
            if patient_input:
                with st.spinner("Translating & Analyzing..."):
                    # Call Mock API
                    result = mock_api.process_patient_input(patient_input, st.session_state.patient_lang)
                    
                    # Update State
                    st.session_state.last_patient_input = patient_input
                    st.session_state.clinical_summary = result
                    st.session_state.messages.append({"role": "patient", "content": patient_input})
                    
                    st.rerun()
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
        doctor_input = st.text_area("Response (JP/EN)", height=100, placeholder="Enter response here...", key="doc_input")
        
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        if st.button("Send & Translate / 送信・翻訳", key="send_doctor"):
            if doctor_input:
                with st.spinner("Translating to Patient's Language..."):
                    # Call Mock API
                    translated_response = mock_api.process_doctor_response(doctor_input, st.session_state.patient_lang)
                    
                    # Update State
                    st.session_state.messages.append({"role": "doctor", "content": translated_response})
                    
                    st.rerun()
            else:
                st.warning("Please enter a response.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # End Doctor Panel

# Footer
st.markdown("---")
st.caption("Powered by TRAE + MiniMax + Agora | Hackathon Build")
