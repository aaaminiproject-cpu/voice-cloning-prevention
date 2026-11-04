
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import io

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="VOICEGUARD | AI Voice Cloning Detector",
    page_icon="🛡️",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CYBER DESIGN + 3D ANIMATIONS ----------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 15%, #10314B 0%, transparent 35%),
        radial-gradient(circle at 85% 70%, #102D47 0%, transparent 35%),
        #050D19;
    color: #EAF6FF;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown p,
label {
    color: #EAF6FF;
}

/* Floating background lights */
.orb {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    filter: blur(2px);
    opacity: 0.35;
}

.orb-one {
    width: 160px;
    height: 160px;
    top: 15%;
    right: 5%;
    background: #087FAD;
    animation: floatOne 9s ease-in-out infinite;
}

.orb-two {
    width: 110px;
    height: 110px;
    top: 55%;
    left: 3%;
    background: #1455A0;
    animation: floatTwo 11s ease-in-out infinite;
}

@keyframes floatOne {
    0%, 100% { transform: translate3d(0,0,0); }
    50% { transform: translate3d(-35px,35px,45px); }
}

@keyframes floatTwo {
    0%, 100% { transform: translate3d(0,0,0); }
    50% { transform: translate3d(35px,-30px,35px); }
}

/* Main hero */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(125deg, #102E49, #091827);
    border: 1px solid #17627C;
    border-radius: 22px;
    padding: 32px;
    margin-bottom: 25px;
    box-shadow: 0 15px 45px rgba(0, 190, 255, 0.10);
    animation: heroEnter 1s ease-out;
}

@keyframes heroEnter {
    from {
        opacity: 0;
        transform: translateY(25px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero h1 {
    color: white !important;
    font-size: clamp(28px, 5vw, 48px);
    font-weight: 850;
    letter-spacing: -1px;
    line-height: 1.15;
}

.hero p {
    color: #A9BED4 !important;
}

/* 3D shield */
.shield-scene {
    perspective: 700px;
    display: flex;
    justify-content: center;
    padding: 12px;
}

.shield {
    width: 115px;
    height: 115px;
    border: 2px solid #35E6FF;
    border-radius: 30px;
    background: linear-gradient(145deg, #164D6C, #071B2E);
    box-shadow:
        0 0 25px #00CFFF66,
        inset 0 0 20px #00CFFF22;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 65px;
    animation: shield3D 5s ease-in-out infinite;
    transform-style: preserve-3d;
}

@keyframes shield3D {
    0%, 100% {
        transform: rotateY(-12deg) rotateX(8deg) translateY(0);
    }
    50% {
        transform: rotateY(12deg) rotateX(-8deg) translateY(-12px);
    }
}

/* Panels */
.panel {
    background: linear-gradient(145deg, #102A42, #0A1929);
    border: 1px solid #1A526B;
    border-radius: 17px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 8px 25px #00000033;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.panel:hover {
    transform: perspective(700px) translateY(-5px) rotateX(2deg);
    box-shadow: 0 12px 30px #00CFFF22;
}

/* Upload box */
div[data-testid="stFileUploader"] {
    background: #10243A;
    border: 1px dashed #35CFEA;
    border-radius: 14px;
    padding: 15px;
}

div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] small {
    color: #EAF4FF !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(100deg, #00AFCB, #35E6FF);
    color: #06101D;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 11px 24px;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 0 20px #35E6FF77;
    color: #06101D;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #10243A;
    border: 1px solid #1A526B;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #A9BED4 !important;
}

div[data-testid="stMetricValue"] {
    color: #35E6FF !important;
}

footer {
    visibility: hidden;
}

</style>

<div class="orb orb-one"></div>
<div class="orb orb-two"></div>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero">
    <h2>🛡️ VOICEGUARD</h2>
    <h1>AI VOICE CLONING DETECTOR</h1>
    <p>
        Detect AI-generated voices and identify
        potential voice impersonation.
    </p>
    <p style="color:#35E6FF !important;">
        ● AUDIO INTELLIGENCE SYSTEM
    </p>
    <div class="shield-scene">
        <div class="shield">🛡️</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- AUDIO UPLOAD ----------------

st.markdown("## 📡 AUDIO INPUT")

st.markdown("""
<div class="panel">
    <h3>Upload Audio for Analysis</h3>
    <p style="color:#A9BED4;">
        Select an audio file to inspect its waveform
        and frequency characteristics.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose WAV or MP3",
    type=["wav", "mp3"]
)

# ---------------- ANALYSIS ----------------

if uploaded_file:

    st.success("Audio uploaded successfully!")

    st.audio(uploaded_file)

    if st.button("⚡ ANALYZE AUDIO"):

        try:
            audio, sr = librosa.load(
                uploaded_file,
                sr=16000,
                mono=True
            )

            duration = len(audio) / sr
            peak = float(np.max(np.abs(audio)))

            st.markdown("## 📊 AUDIO OVERVIEW")

            col1, col2, col3 = st.columns(3)

            col1.metric("DURATION", f"{duration:.2f} sec")
            col2.metric("SAMPLE RATE", f"{sr} Hz")
            col3.metric("PEAK AMPLITUDE", f"{peak:.3f}")

            # ---------------- WAVEFORM ----------------

            st.markdown("## 📈 AUDIO WAVEFORM")

            fig, ax = plt.subplots(figsize=(12, 3))
            fig.patch.set_facecolor("#10243A")
            ax.set_facecolor("#10243A")

            librosa.display.waveshow(
                audio,
                sr=sr,
                ax=ax,
                color="#35E6FF"
            )

            ax.set_xlabel("TIME", color="white")
            ax.set_ylabel("AMPLITUDE", color="white")
            ax.tick_params(colors="white")

            for spine in ax.spines.values():
                spine.set_color("#28718A")

            ax.grid(color="#24445B", alpha=0.4)

            st.pyplot(fig)
            plt.close(fig)

            # ---------------- MEL SPECTROGRAM ----------------

            st.markdown("## 🌌 MEL SPECTROGRAM")

            mel = librosa.feature.melspectrogram(
                y=audio,
                sr=sr,
                n_fft=1024,
                hop_length=256,
                n_mels=64
            )

            mel_db = librosa.power_to_db(
                mel,
                ref=np.max
            )

            fig, ax = plt.subplots(figsize=(12, 4))
            fig.patch.set_facecolor("#10243A")
            ax.set_facecolor("#10243A")

            image = librosa.display.specshow(
                mel_db,
                sr=sr,
                hop_length=256,
                x_axis="time",
                y_axis="mel",
                cmap="magma",
                ax=ax
            )

            ax.set_title(
                "Audio Frequency Visualization",
                color="white"
            )

            ax.tick_params(colors="white")

            fig.colorbar(image, ax=ax, format="%+2.0f dB")

            st.pyplot(fig)
            plt.close(fig)

            # ---------------- HISTORY ----------------

            st.session_state.history.append({
                "filename": uploaded_file.name,
                "duration": round(duration, 2),
                "sample_rate": sr
            })

            st.info(
                "Audio inspection completed. "
                "AI voice classification will be enabled "
                "after connecting the trained detection model."
            )

        except Exception as e:
            st.error(f"Audio analysis failed: {e}")

else:
    st.info("Waiting for audio input...")

# ---------------- HISTORY PANEL ----------------

st.divider()
st.markdown("## 🕘 ANALYSIS HISTORY")

if st.session_state.history:

    for item in reversed(st.session_state.history):
        st.markdown(
            f"""
            <div class="panel">
                <b>🎵 {item['filename']}</b><br>
                <span style="color:#A9BED4;">
                    Duration: {item['duration']} sec |
                    Sample rate: {item['sample_rate']} Hz
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.caption("Your analysis history will appear here during this session.")

# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<p style="
    text-align:center;
    color:#7893AA;
    font-size:13px;
">
    🛡️ VOICEGUARD |
    AI VOICE CLONING DETECTION PROJECT
</p>
""", unsafe_allow_html=True)
