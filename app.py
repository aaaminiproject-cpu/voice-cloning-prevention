
     
import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import time
import os

st.set_page_config(
    page_title="VOICEGUARD | AI Voice Detection",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- PAGE STYLE ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at 50% 25%, #183b63 0%, transparent 38%),
      linear-gradient(135deg, #071426, #0b1c32 55%, #06101e);
    color: #edf7ff;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

header, footer {
    visibility: hidden;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 2px;
    color: white;
}

.brand span {
    color: #36cfff;
}

.hero-title {
    font-size: clamp(38px, 6vw, 72px);
    font-weight: 800;
    line-height: 1.04;
    color: white;
    letter-spacing: -3px;
}

.hero-title span {
    color: #37cfff;
}

.subtext {
    color: #a9bfd5;
    font-size: 16px;
    line-height: 1.8;
}

.eyebrow {
    color: #42d5ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
}

.panel {
    background: rgba(18, 43, 69, 0.82);
    border: 1px solid rgba(70, 190, 255, 0.23);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.22);
}

.robot-stage {
    position: relative;
    min-height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 25px;
    background: radial-gradient(ellipse, #174c78 0%, #0c2945 48%, transparent 75%);
}

.robot {
    width: min(100%, 390px);
    max-height: 440px;
    object-fit: contain;
    position: relative;
    z-index: 2;
    animation: floatRobot 4s ease-in-out infinite;
    filter: drop-shadow(0 0 25px rgba(34,190,255,0.35));
}

@keyframes floatRobot {
    0%, 100% { transform: translateY(0) rotate(-1deg); }
    50% { transform: translateY(-13px) rotate(1deg); }
}

.ring {
    position: absolute;
    width: 280px;
    height: 280px;
    border: 2px solid rgba(42,205,255,0.55);
    border-radius: 50%;
    box-shadow: 0 0 25px rgba(42,205,255,0.3);
    animation: pulse 3s ease-out infinite;
}

.ring.two {
    width: 350px;
    height: 350px;
    animation-delay: 1s;
}

@keyframes pulse {
    0% { transform: scale(0.75); opacity: 0.8; }
    100% { transform: scale(1.35); opacity: 0; }
}

.robot-caption {
    position: absolute;
    bottom: 18px;
    z-index: 3;
    color: #8feaff;
    font-size: 12px;
    letter-spacing: 2px;
    text-align: center;
}

.status-card {
    background: rgba(10, 30, 51, 0.9);
    border: 1px solid rgba(57,194,255,0.35);
    border-radius: 14px;
    padding: 15px;
    color: #dff8ff;
    text-align: center;
    margin-top: 12px;
}

.metric {
    background: rgba(22, 55, 84, 0.8);
    border: 1px solid rgba(70,190,255,0.2);
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 10px;
}

.metric-label {
    color: #91abc3;
    font-size: 12px;
}

.metric-value {
    font-size: 23px;
    font-weight: 700;
    color: #ffffff;
}

.stButton > button {
    background: linear-gradient(90deg, #087cce, #28c5ef);
    color: white;
    border: 0;
    border-radius: 12px;
    padding: 12px 25px;
    font-weight: 700;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 25px rgba(37,190,255,0.4);
    color: white;
}

.stFileUploader {
    background: rgba(16, 43, 68, 0.85);
    border: 1px dashed #39bdf2;
    border-radius: 15px;
    padding: 12px;
}

h2, h3 {
    color: #eaf7ff;
}

footer {
    color: #718da7;
}
</style>
""", unsafe_allow_html=True)


# ---------------- ROBOT IMAGE ----------------

image_path = "voiceguard_robot.png"

robot_html = ""

if os.path.exists(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    robot_html = f"""
    <div class="robot-stage">
        <div class="ring"></div>
        <div class="ring two"></div>
        <img class="robot"
             src="data:image/png;base64,{encoded}">
        <div class="robot-caption">
            VOICEGUARD AI ASSISTANT
        </div>
    </div>
    """
else:
    robot_html = """
    <div class="robot-stage">
        <div class="ring"></div>
        <div class="ring two"></div>
        <div style="font-size:100px;z-index:2;">🎙️</div>
        <div class="robot-caption">ADD ROBOT IMAGE TO YOUR REPOSITORY</div>
    </div>
    """


# ---------------- HEADER ----------------

st.markdown("""
<div class="brand">◈ VOICE<span>GUARD</span></div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- HERO SECTION ----------------

left, right = st.columns([1, 1.15], gap="large")

with left:
    st.markdown("""
    <div style="padding-top:55px;">
        <div class="eyebrow">AI VOICE CLONING DETECTOR</div>
        <br>
        <div class="hero-title">
            Protect the<br>
            Authentic <span>Voice.</span>
        </div>
        <br>
        <p class="subtext">
            Every voice tells a story. VOICEGUARD uses
            AI-powered audio analysis to help identify
            genuine and AI-generated voices.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status-card">
        ✦ Your voice deserves to be trusted.
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(robot_html, unsafe_allow_html=True)


# ---------------- ROBOT WELCOME ----------------

st.markdown("""
<div class="status-card">
    <b>🤖 Assistant:</b>
    Welcome to VOICEGUARD! I'm ready to listen.
    Upload an audio file and let's inspect its voice patterns.
</div>
""", unsafe_allow_html=True)

st.write("")
st.divider()


# ---------------- AUDIO UPLOAD ----------------

st.markdown('<div class="eyebrow">01 / AUDIO INPUT</div>',
            unsafe_allow_html=True)

st.subheader("Upload your audio")

st.markdown("""
<p class="subtext">
    Give the assistant a voice to listen to.
    Supported formats: WAV and MP3.
</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3"],
    help="Upload a WAV or MP3 audio file."
)

if uploaded_file is not None:

    st.success("🎧 Audio received! The assistant is listening.")

    st.audio(uploaded_file)

    # Load audio
    try:
        audio_bytes = uploaded_file.getvalue()

        audio, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=None,
            mono=True
        )

        duration = len(audio) / sample_rate
        peak = float(np.max(np.abs(audio)))
        samples = len(audio)

        st.write("")
        st.markdown('<div class="eyebrow">02 / AUDIO INSPECTION</div>',
                    unsafe_allow_html=True)

        st.subheader("Audio information")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric">
                <div class="metric-label">DURATION</div>
                <div class="metric-value">{duration:.2f}s</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric">
                <div class="metric-label">SAMPLE RATE</div>
                <div class="metric-value">{sample_rate} Hz</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric">
                <div class="metric-label">AUDIO SAMPLES</div>
                <div class="metric-value">{samples:,}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.subheader("Audio waveform")

        fig, ax = plt.subplots(figsize=(12, 3))
        time_axis = np.arange(len(audio)) / sample_rate

        ax.plot(time_axis, audio, linewidth=0.45)
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Amplitude")
        ax.set_facecolor("#102943")
        fig.patch.set_facecolor("#102943")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.spines["bottom"].set_color("#5c7894")
        ax.spines["left"].set_color("#5c7894")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        st.pyplot(fig)
        plt.close(fig)

        st.write("")

        # ---------------- ANALYSIS ----------------

        st.markdown(
            '<div class="eyebrow">03 / VOICE ANALYSIS</div>',
            unsafe_allow_html=True
        )

        st.subheader("Ready to analyse")

        if st.button("🔍  Analyse Audio", use_container_width=True):

            status_area = st.empty()
            progress = st.progress(0)

            stages = [
                ("🎧 Listening to your audio...", 25),
                ("📡 Scanning voice patterns...", 50),
                ("🧠 Analysing audio features...", 75),
                ("✨ Preparing inspection summary...", 100)
            ]

            for message, percentage in stages:
                status_area.markdown(
                    f'<div class="status-card">{message}</div>',
                    unsafe_allow_html=True
                )
                progress.progress(percentage)
                time.sleep(1.2)

            status_area.markdown("""
            <div class="status-card">
                ✅ Audio inspection completed!<br><br>
                The audio has been loaded and inspected successfully.
                The trained voice classification model is not
                connected yet.
            </div>
            """, unsafe_allow_html=True)

            st.info(
                "Model integration is the next step. "
                "No genuine/AI classification has been made yet."
            )

    except Exception as error:
        st.error(
            "Unable to process this audio file. "
            "Please try another WAV or MP3 file."
        )
        st.caption(str(error))


# ---------------- FOOTER ----------------

st.write("")
st.divider()

st.markdown("""
<div style="text-align:center;padding:25px;color:#829bb4;">
    <b>VOICEGUARD</b><br>
    AI Voice Cloning Detection Project<br><br>
    Built with Python • PyTorch • Streamlit
</div>
""", unsafe_allow_html=True)
