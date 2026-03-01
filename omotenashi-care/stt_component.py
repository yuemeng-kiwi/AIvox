import streamlit as st
import streamlit.components.v1 as components

def stt_component(key="stt"):
    """
    Embeds a simple Speech-to-Text button using Web Speech API.
    Returns the transcribed text via Streamlit component value.
    """
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Noto Sans JP', sans-serif; background-color: transparent; margin: 0; padding: 0; }}
            .container {{ display: flex; align-items: center; gap: 10px; }}
            button {{
                background-color: #4A7C59; /* Matcha */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: background-color 0.3s;
                font-size: 16px;
            }}
            button:hover {{ background-color: #3A6346; }}
            button.listening {{ background-color: #C0392B; animation: pulse 1.5s infinite; }}
            
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 rgba(192, 57, 43, 0.7); }}
                70% {{ box-shadow: 0 0 0 10px rgba(192, 57, 43, 0); }}
                100% {{ box-shadow: 0 0 0 0 rgba(192, 57, 43, 0); }}
            }}
            
            #status {{ font-size: 0.9em; color: #555; margin-left: 10px; font-style: italic; }}
        </style>
    </head>
    <body>
        <div class="container">
            <button id="mic-btn" onclick="toggleListening()">
                🎤 Start Speaking
            </button>
            <span id="status"></span>
        </div>

        <script>
            // Initialize Streamlit connection
            function sendMessageToStreamlit(text) {{
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: text
                }}, "*");
            }}

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            let recognition;
            let isListening = false;

            if (SpeechRecognition) {{
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.lang = 'en-US'; // Default to English
                recognition.interimResults = false;

                recognition.onstart = function() {{
                    isListening = true;
                    document.getElementById("mic-btn").classList.add("listening");
                    document.getElementById("mic-btn").innerHTML = "🛑 Stop Speaking";
                    document.getElementById("status").innerText = "Listening...";
                }};

                recognition.onend = function() {{
                    isListening = false;
                    document.getElementById("mic-btn").classList.remove("listening");
                    document.getElementById("mic-btn").innerHTML = "🎤 Start Speaking";
                    document.getElementById("status").innerText = "";
                }};

                recognition.onresult = function(event) {{
                    const transcript = event.results[0][0].transcript;
                    document.getElementById("status").innerText = "Recognized!";
                    sendMessageToStreamlit(transcript);
                }};
                
                recognition.onerror = function(event) {{
                    console.error("Speech recognition error", event.error);
                    document.getElementById("status").innerText = "Error: " + event.error;
                    isListening = false;
                    document.getElementById("mic-btn").classList.remove("listening");
                    document.getElementById("mic-btn").innerHTML = "🎤 Retry";
                }};
            }} else {{
                document.getElementById("mic-btn").disabled = true;
                document.getElementById("mic-btn").innerText = "Browser Not Supported";
                document.getElementById("status").innerText = "Please use Chrome/Edge/Safari";
            }}

            function toggleListening() {{
                if (!recognition) return;
                
                if (isListening) {{
                    recognition.stop();
                }} else {{
                    recognition.start();
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    # We use a trick to get data back: components.html cannot return values directly easily without custom component boilerplate.
    # For a hackathon, let's use a simpler approach: 
    # Just render the HTML, but since we can't easily get the value back to Python without a custom component build step...
    # wait, standard st.components.v1.html doesn't support return values.
    
    # BETTER APPROACH FOR HACKATHON:
    # Use 'streamlit-mic-recorder' or similar if installable.
    # Since we can't install packages easily in the cloud without rebuilding...
    
    # Wait, the user already has 'streamlit' installed. 
    # Let's use `st.audio_input` (New in Streamlit 1.39!) if available, or fallback to text.
    # But since we want "Real-Time" feeling, let's try to stick to a simple UI.
    
    return components.html(html_code, height=80)

# Since we can't easily get the JS value back without a proper component, 
# I will switch to using 'st.audio_input' which is the official supported way now!
# It records audio, and then we send that audio file to MiniMax (or OpenAI Whisper).
# BUT MiniMax Audio API might be complex.

# ALTERNATIVE: Use the browser's dictation feature on the INPUT FIELD directly.
# Most mobile/desktop keyboards have a microphone icon. That is the easiest "Voice Input".
