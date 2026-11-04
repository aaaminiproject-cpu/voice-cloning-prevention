
import streamlit as st
import streamlit.components.v1 as components
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import time
import html

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="VOICEGUARD | AI Voice Cloning Detector",
    page_icon="🛡️",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

if "robot_state" not in st.session_state:
    st.session_state.robot_state = "welcome"

if "robot_message" not in st.session_state:
    st.session_state.robot_message = (
        "Hello! Welcome to VOICEGUARD. "
        "I'm your voice analysis assistant!"
    )

# ---------------- ROBOT ASSISTANT ----------------

def show_robot(state, message):

    robot_styles = {
        "welcome": "wave",
        "listening": "listen",
        "scanning": "scan",
        "analysing": "think",
        "complete": "happy",
        "waiting": "neutral"
    }

    animation = robot_styles.get(state, "wave")
    safe_message = html.escape(message)

    st.markdown("""
    <style>
    .robot-card {
        background: linear-gradient(140deg, #102C45, #091827);
        border: 1px solid #17627C;
        border-radius: 18px;
        padding: 18px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 15px 0;
        box-shadow: 0 8px 28px #00CFFF12;
    }

    .robot {
        width: 78px;
        height: 78px;
        min-width: 78px;
        border-radius: 25px;
        background: linear-gradient(145deg, #DDFBFF, #6ACFE8);
        border: 2px solid #35E6FF;
        box-shadow: 0 0 18px #35E6FF55;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: robotFloat 3s ease-in-out infinite;
    }

    .robot-face {
        width: 53px;
        height: 40px;
        border-radius: 15px;
        background: #09263A;
        position: relative;
    }

    .eyes {
        display: flex;
        justify-content: center;
        gap: 13px;
        padding-top: 10px;
    }

    .eye {
        width: 7px;
        height: 10px;
        border-radius: 50%;
        background: #35E6FF;
        box-shadow: 0 0 8px #35E6FF;
    }

    .mouth {
        width: 15px;
        height: 5px;
        border-bottom: 2px solid #35E6FF;
        border-radius: 50%;
        margin: 4px auto;
    }

    .robot.wave {
        animation: waveRobot 1.4s ease-in-out infinite;
    }

    .robot.listen {
        animation: listenRobot 1.2s ease-in-out infinite;
    }

    .robot.scan {
        animation: scanRobot 0.8s ease-in-out infinite;
    }

    .robot.think {
        animation: thinkRobot 1.5s ease-in-out infinite;
    }

    .robot.happy {
        animation: happyRobot 0.65s ease-in-out infinite;
    }

    .robot.neutral {
        animation: robotFloat 3s ease-in-out infinite;
    }

    @keyframes robotFloat {
        0%,100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }

    @keyframes waveRobot {
        0%,100% { transform: rotate(-5deg) translateY(0); }
        50% { transform: rotate(7deg) translateY(-7px); }
    }

    @keyframes listenRobot {
        0%,100% { transform: rotate(-8deg); }
        50% { transform: rotate(8deg); }
    }

    @keyframes scanRobot {
        0%,100% { transform: scale(1); }
        50% { transform: scale(1.07); }
    }

    @keyframes thinkRobot {
        0%,100% { transform: translateY(0) rotate(0); }
        50% { transform: translateY(-5px) rotate(5deg); }
    }

    @keyframes happyRobot {
        0%,100% { transform: translateY(0) rotate(-5deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }

    .robot-title {
        color: #35E6FF;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .robot-message {
        color: #EAF6FF;
        font-size: 14px;
        line-height: 1.5;
    }

    .robot-status {
        color: #8CAFC5;
        font-size: 11px;
        margin-top: 6px;
    }

    @media (max-width: 500px) {
        .robot-card { padding: 12px; gap: 12px; }
        .robot { width: 65px; height: 65px; min-width: 65px; }
        .robot-message { font-size: 12px; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="robot-card">
        <div class="robot {animation}">
            <div class="robot-face">
                <div class="eyes">
                    <div class="eye"></div>
                    <div class="eye"></div>
                </div>
                <div class="mouth"></div>
            </div>
        </div>
        <div>
            <div class="robot-title">VOICEGUARD AI ASSISTANT</div>
            <div class="robot-message">{safe_message}</div>
            <div class="robot-status">● {state.upper()} MODE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Speech button: browser support required
    components.html(
        f"""
        <button onclick="speakMessage()"
        style="
            background:#12344D;
            color:#35E6FF;
            border:1px solid #17627C;
            padding:9px 15px;
            border-radius:9px;
            cursor:pointer;
            font-weight:bold;">
            🔊 Speak message
        </button>
        <script>
        function speakMessage() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const speech = new SpeechSynthesisUtterance(
                    {repr(message)}
                );
                speech.rate = 0.95;
                speech.pitch = 1.1;
                window.speechSynthesis.speak(speech);
            }}
        }}
        </script>
        """,
        height=48
    )


# ---------------- CYBERSECURITY DESIGN ----------------

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

.hero {
    background: linear-gradient(125deg, #102E49, #091827);
    border: 1px solid #17627C;
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 15px 45px #00BFFF18;
}

.hero h1 {
    color: white !important;
    font-size: clamp(27px, 5vw, 46px);
    font-weight: 850;
}

.hero p {
    color: #A9BED4 !important;
}

.panel {
    background: linear-gradient(145deg, #102A42, #0A1929);
    border: 1px solid #1A526B;
    border-radius: 17px;
    padding: 20px;
    margin-bottom: 15px;
    transition: transform 0.3s, box-shadow 0.3s;
}

.panel:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px #00CFFF22;
}

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

div.stButton > button {
    background: linear-gradient(100deg, #00AFCB, #35E6FF);
    color: #06101D;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 11px 24px;
}

div.stButton > button:hover {
    box-shadow: 0 0 20px #35E6FF77;
    color: #06101D;
}

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
""", unsafe_allow_html=True)


# ---------------- WEBSITE HEADER ----------------

st.markdown("""
<div class="hero">
<h2>🛡️ VOICEGUARD</h2>
<h1>AI VOICE CLONING DETECTOR</h1>
<p>Detect AI-generated voices and identify potential voice impersonation.</p>
<p style="color:#35E6FF;">● AUDIO INTELLIGENCE SYSTEM</p>
</div>
""", unsafe_allow_html=True)


# ---------------- WELCOME ASSISTANT ----------------

st.markdown("### 🤖 MEET YOUR AI ASSISTANT")

show_robot(
    "welcome",
    "Welcome to VOICEGUARD! We are a team of three developers building a project to help identify AI-generated and cloned voices. Let's inspect your audio together!"
)

with st.expander("Meet the developers"):
    st.markdown("""
    - **Anthony — Member 1:** Audio preparation and preprocessing.
    - **Afan — Member 2:** Deep learning and detection model.
    - **Abhishek — Member 3:** Website design and integration.
    """)


# ---------------- AUDIO INPUT ----------------

st.markdown("## 📡 AUDIO INPUT")

st.markdown("""
<div class="panel">
<h3>Upload Audio for Analysis</h3>
<p style="color:#A9BED4;">
Supported formats: WAV and MP3
</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your audio file",
    type=["wav", "mp3"]
)

if uploaded_file:

    show_robot(
        "listening",
        "I have received your audio! I'm listening and getting ready to inspect it."
    )

    st.success("Audio uploaded successfully!")
    st.audio(uploaded_file)

    if st.button("⚡ ANALYZE AUDIO"):

        # Show scanning activity
        show_robot(
            "scanning",
            "Starting the audio scan! I'm checking the signal before analysis."
        )

        time.sleep(1)

        # Show analysis activity
        show_robot(
            "analysing",
            "I'm examining your audio waveform and Mel frequency patterns. Please wait!"
        )

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

            # ---------------- COMPLETION ----------------

            st.session_state.history.append({
                "filename": uploaded_file.name,
                "duration": round(duration, 2),
                "sample_rate": sr
            })

            show_robot(
                "complete",
                "Audio inspection is complete! I've displayed the waveform and Mel spectrogram. The trained AI detection model still needs to be connected before I can classify this voice."
            )

            st.info(
                "Audio inspection completed. "
                "No genuine or AI-generated classification "
                "has been made yet."
            )

        except Exception as e:
            show_robot(
                "waiting",
                "Oops! I had trouble processing this audio. Please try another file."
            )
            st.error(f"Audio analysis failed: {e}")

else:
    show_robot(
        "waiting",
        "I'm ready! Upload a WAV or MP3 recording and I'll help inspect it."
    )


# ---------------- HISTORY ----------------

st.divider()
st.markdown("## 🕘 ANALYSIS HISTORY")

if st.session_state.history:

    for item in reversed(st.session_state.history):
        st.markdown(
            f"""
            <div class="panel">
                <b>🎵 {html.escape(item['filename'])}</b><br>
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
<p style="text-align:center; color:#7893AA; font-size:13px;">
🛡️ VOICEGUARD | AI VOICE CLONING DETECTION PROJECT
</p>
""", unsafe_allow_html=True)
            
