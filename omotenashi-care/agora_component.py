import streamlit as st
import streamlit.components.v1 as components

def agora_voice_component(app_id, channel_name, uid, token=None):
    """
    Embeds the Agora Web SDK for voice communication.
    """
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.2.js"></script>
        <style>
            body {{ font-family: 'Noto Sans JP', sans-serif; background-color: transparent; }}
            .status {{ padding: 10px; border-radius: 5px; margin-bottom: 10px; font-weight: bold; text-align: center; }}
            .status.connected {{ background-color: #d4edda; color: #155724; }}
            .status.disconnected {{ background-color: #f8d7da; color: #721c24; }}
            .controls {{ display: flex; gap: 10px; justify-content: center; }}
            button {{
                padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;
                transition: background-color 0.3s;
            }}
            #join-btn {{ background-color: #4A7C59; color: white; }} /* Matcha */
            #leave-btn {{ background-color: #C0392B; color: white; }} /* Torii */
            button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        </style>
    </head>
    <body>
        <div id="status" class="status disconnected">Voice Channel: Disconnected</div>
        <div class="controls">
            <button id="join-btn" onclick="joinChannel()">📞 Join Voice</button>
            <button id="leave-btn" onclick="leaveChannel()" disabled>End Call</button>
        </div>

        <script>
            const client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            const options = {{
                appId: "{app_id}",
                channel: "{channel_name}",
                token: {f"'{token}'" if token else "null"},
                uid: {uid}
            }};
            
            let localAudioTrack;

            async function joinChannel() {{
                try {{
                    document.getElementById("status").innerText = "Connecting...";
                    
                    await client.join(options.appId, options.channel, options.token, options.uid);
                    localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                    await client.publish([localAudioTrack]);
                    
                    document.getElementById("status").innerText = "🟢 Connected to Voice Channel";
                    document.getElementById("status").className = "status connected";
                    document.getElementById("join-btn").disabled = true;
                    document.getElementById("leave-btn").disabled = false;
                    
                    console.log("Joined channel successfully");
                    
                }} catch (error) {{
                    console.error("Error joining channel:", error);
                    document.getElementById("status").innerText = "❌ Connection Failed";
                }}
            }}

            async function leaveChannel() {{
                try {{
                    if (localAudioTrack) {{
                        localAudioTrack.close();
                        localAudioTrack = null;
                    }}
                    await client.leave();
                    
                    document.getElementById("status").innerText = "Voice Channel: Disconnected";
                    document.getElementById("status").className = "status disconnected";
                    document.getElementById("join-btn").disabled = false;
                    document.getElementById("leave-btn").disabled = true;
                    
                    console.log("Left channel successfully");
                    
                }} catch (error) {{
                    console.error("Error leaving channel:", error);
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    return components.html(html_code, height=120)
