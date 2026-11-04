
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="VoiceGuard | AI Voice Detector",
    page_icon="🎙️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #F5F7FB;
}
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}
h1, h2, h3, p, label {
    color: #17233D;
}
.hero {
    background: white;
    padding: 28px;
    border-radius: 18px;
    border: 1px solid #E1E7F0;
    margin-bottom: 24px;
}
.upload-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #E1E7F0;
}
div.stButton > button {
    background: #2457C5;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 24px;
}
div.stButton > button:hover {
    background: #19449F;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h2>🎙️ VOICEGUARD</h2>
    <h1>Verify your audio.</h1>
    <p>AI-powered voice cloning and impersonation detection.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Upload your audio")

uploaded_file = st.file_uploader(
    "Choose a WAV or MP3 file",
    type=["wav", "mp3"]
)

if uploaded_file:
    st.success("Audio uploaded successfully!")
    st.audio(uploaded_file)

    st.divider()
    st.subheader("Audio analysis")

    if st.button("Analyze Audio"):
        try:
            audio, sr = librosa.load(
                uploaded_file,
                sr=16000,
                mono=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Duration", f"{len(audio)/sr:.2f} seconds")
                st.metric("Sample rate", f"{sr} Hz")

            with col2:
                st.metric("Audio samples", f"{len(audio):,}")
                st.metric("Peak amplitude", f"{np.max(np.abs(audio)):.3f}")

            st.subheader("Waveform")

            fig, ax = plt.subplots(figsize=(10, 3))
            librosa.display.waveshow(audio, sr=sr, ax=ax)
            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            st.pyplot(fig)
            plt.close(fig)

            st.info(
                "Audio inspection completed. "
                "AI voice classification will be enabled "
                "after connecting the trained detection model."
            )

        except Exception as e:
            st.error(f"Could not analyze audio: {e}")

st.divider()

st.caption("VOICEGUARD | AI Voice Cloning Detection Project")
