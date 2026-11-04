
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="VOICEGUARD | AI Voice Cloning Detector",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CYBERSECURITY DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #06101D, #0B1B2D);
    color: #EAF4FF;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.stMarkdown,
.stMarkdown p,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
label {
    color: #EAF4FF !important;
}

.hero {
    background: linear-gradient(110deg, #102B43, #0C1B2D);
    border: 1px solid #17627C;
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(0, 210, 255, 0.08);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 36px;
    margin-bottom: 8px;
}

.hero p {
    color: #A9BED4 !important;
}

.panel {
    background: #10243A;
    border: 1px solid #1A526B;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
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
    background: #00BBD4;
    color: #06101D;
    font-weight: bold;
    border: none;
    border-radius: 9px;
    padding: 11px 25px;
}

div.stButton > button:hover {
    background: #35E6FF;
    color: #06101D;
    border: none;
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

.stAlert {
    border-radius: 10px;
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
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='color:#FFFFFF;'>AI VOICE CLONING DETECTOR</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#A9BED4;'>"
    "Detect AI-generated voices and identify "
    "potential voice impersonation."
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#35E6FF;'>● AUDIO ANALYSIS SYSTEM</p>",
    unsafe_allow_html=True
)


# ---------------- AUDIO UPLOAD ----------------

st.markdown("### 📡 AUDIO INPUT")

st.markdown("""
<div class="panel">
    <h3>Upload Audio for Analysis</h3>
    <p style="color:#A9BED4;">
        Supported formats: WAV and MP3
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Select an audio file",
    type=["wav", "mp3"]
)


# ---------------- AUDIO ANALYSIS ----------------

if uploaded_file:

    st.success("Audio uploaded successfully!")

    st.audio(uploaded_file)

    st.divider()

    st.markdown("### 🔍 AUDIO ANALYSIS")

    if st.button("⚡ ANALYZE AUDIO"):

        try:

            # Load audio at 16 kHz
            audio, sr = librosa.load(
                uploaded_file,
                sr=16000,
                mono=True
            )

            # Calculate audio information
            duration = len(audio) / sr

            peak = float(np.max(np.abs(audio)))

            # Display audio information
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "DURATION",
                f"{duration:.2f} sec"
            )

            col2.metric(
                "SAMPLE RATE",
                f"{sr} Hz"
            )

            col3.metric(
                "PEAK AMPLITUDE",
                f"{peak:.3f}"
            )

            # ---------------- WAVEFORM ----------------

            st.markdown("### 📈 AUDIO WAVEFORM")

            fig, ax = plt.subplots(figsize=(12, 3))

            fig.patch.set_facecolor("#10243A")

            ax.set_facecolor("#10243A")

            librosa.display.waveshow(
                audio,
                sr=sr,
                ax=ax,
                color="#35E6FF"
            )

            ax.set_xlabel(
                "TIME",
                color="white"
            )

            ax.set_ylabel(
                "AMPLITUDE",
                color="white"
            )

            ax.tick_params(colors="white")

            for spine in ax.spines.values():
                spine.set_color("#28718A")

            ax.grid(
                color="#24445B",
                alpha=0.4
            )

            st.pyplot(fig)

            plt.close(fig)

            # ---------------- RESULT STATUS ----------------

            st.info(
                "Audio inspection completed. "
                "AI voice classification is awaiting "
                "integration of the trained detection model."
            )

        except Exception as e:

            st.error(
                f"Audio analysis failed: {e}"
            )

else:

    st.info("Waiting for audio input...")


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<p style="
    text-align:center;
    color:#7893AA;
    font-size:13px;
">
    VOICEGUARD | AI VOICE CLONING DETECTION PROJECT
</p>
""", unsafe_allow_html=True)
                
