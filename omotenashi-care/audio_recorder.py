import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import numpy as np
import av
import queue

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_queue = queue.Queue()

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert audio frame to numpy array and put in queue
        sound = frame.to_ndarray()
        self.audio_queue.put(sound)
        return frame

def audio_recorder():
    """
    Records audio from browser using WebRTC.
    Returns: Raw audio data or None.
    """
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"video": False, "audio": True},
    )

    if webrtc_ctx.state.playing:
        st.caption("🔴 Recording... Speak now!")
        return webrtc_ctx
    return None
