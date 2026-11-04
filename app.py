

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import soundfile as sf

st.set_page_config(
    page_title="VoiceGuard | AI Voice Verification",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- PAGE THEME ----------------

st.markdown("""
<style>
.stApp {
    background: #edf2f5;
    color: #101b2b;
}
.block-container {
    max-width: 1250px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}
header[data-testid="stHeader"] {
    background: transparent;
}
footer {visibility: hidden;}

.stButton > button {
    background: #101b2b;
    color: white;
    border: 1px solid #101b2b;
    border-radius: 10px;
    padding: 0.65rem 1.5rem;
    font-weight: 600;
}
.stButton > button:hover {
    background: #243c54;
    color: white;
    border-color: #243c54;
}
section[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.75);
    border: 1px solid #d6e0e8;
    border-radius: 16px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HERO SECTION ----------------

hero_html = """
<!DOCTYPE html>
<html>
<head>
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: transparent;
    color: #101b2b;
}

.hero {
    position: relative;
    min-height: 590px;
    overflow: hidden;
    border-radius: 22px;
    background:
      radial-gradient(ellipse at 65% 43%, #c9e4f0 0%, transparent 38%),
      linear-gradient(115deg, #f8fafb, #e7eef2 65%, #dce7ed);
    padding: 28px 34px;
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 5;
}

.logo {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 3px;
}

.nav-links {
    font-size: 12px;
    letter-spacing: 1px;
    color: #263548;
    word-spacing: 18px;
}

.hero-title {
    position: absolute;
    left: 4%;
    top: 34%;
    z-index: 4;
    max-width: 390px;
}

.eyebrow {
    color: #477e9d;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: bold;
}

.hero-title h1 {
    font-size: clamp(40px, 5vw, 67px);
    line-height: 0.98;
    margin: 15px 0;
    letter-spacing: -2px;
    font-weight: 900;
}

.hero-title p {
    font-size: 14px;
    line-height: 1.6;
    color: #526477;
    max-width: 320px;
}

.hero-button {
    display: inline-block;
    margin-top: 16px;
    padding: 13px 23px;
    border: 1.5px solid #17283a;
    border-radius: 9px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
}

.robot-area {
    position: absolute;
    width: 54%;
    height: 460px;
    right: 1%;
    top: 90px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.orb {
    position: absolute;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    background:
      radial-gradient(circle at 35% 30%, #ffffff 0%, #d8edf4 28%,
      #91b7ca 62%, #587d93 100%);
    border: 5px solid rgba(95,133,155,.5);
    box-shadow: 0 0 35px #9bc9df, inset 0 0 35px #ffffff;
    animation: float 5s ease-in-out infinite;
}

.orb:before, .orb:after {
    content: "";
    position: absolute;
    border: 1px solid rgba(255,255,255,.8);
    border-radius: 50%;
    inset: 15px;
}
.orb:after {
    inset: 28px;
    border-color: rgba(73,159,190,.4);
}

.brain {
    position: absolute;
    top: 42px;
    left: 50%;
    transform: translateX(-50%);
    width: 175px;
    height: 120px;
    border-radius: 50% 50% 42% 42%;
    background:
      radial-gradient(ellipse, #f6c9ef 0%, #a8e9f2 35%,
      #8f9be8 65%, transparent 72%);
    filter: drop-shadow(0 0 17px #b4eaff);
    opacity: .95;
}

.brain:before, .brain:after {
    content: "";
    position: absolute;
    inset: 8px 20px;
    border: 2px solid rgba(255,255,255,.85);
    border-radius: 48%;
}
.brain:after {
    inset: 20px 42px;
    border-color: rgba(255,255,255,.75);
}

.robot {
    position: absolute;
    top: 145px;
    width: 210px;
    height: 260px;
    display: flex;
    flex-direction: column;
    align-items: center;
    filter: drop-shadow(0 15px 15px rgba(25,50,70,.25));
}

.head {
    width: 125px;
    height: 125px;
    border-radius: 48% 48% 42% 42%;
    background: linear-gradient(130deg, #f9ffff, #9bb6c5 50%, #e6f3f6);
    border: 4px solid #7f9baa;
    position: relative;
    z-index: 2;
    box-shadow: inset -10px -8px 18px #7795a7;
}

.face {
    position: absolute;
    top: 42px;
    left: 17px;
    width: 83px;
    height: 38px;
    border-radius: 20px;
    background: linear-gradient(90deg, #142b42, #315b73);
    box-shadow: 0 0 15px #8de9ff;
}

.eye {
    position: absolute;
    top: 13px;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #a4f4ff;
    box-shadow: 0 0 9px #9af5ff;
}
.eye.left { left: 20px; }
.eye.right { right: 20px; }

.mouth {
    position: absolute;
    width: 18px;
    height: 3px;
    background: #b8e9f4;
    bottom: 7px;
    left: 32px;
    border-radius: 5px;
}

.neck {
    width: 48px;
    height: 42px;
    background: linear-gradient(90deg, #607e91, #eaf6fa, #69889b);
    border-radius: 10px;
    margin-top: -2px;
}

.body {
    width: 185px;
    height: 110px;
    margin-top: -2px;
    border-radius: 48% 48% 18% 18%;
    background: linear-gradient(110deg, #7894a5, #f4fbfd 45%, #7f9baa);
    border: 3px solid #8ca7b5;
    position: relative;
}

.chest {
    position: absolute;
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: radial-gradient(circle, #d7ffff, #62c6df 40%, #315a75);
    border: 3px solid #d9faff;
    top: 17px;
    left: 61px;
    box-shadow: 0 0 20px #7deaff;
}

.mic {
    position: absolute;
    width: 28px;
    height: 50px;
    right: -18px;
    top: 24px;
    border-radius: 15px;
    background: linear-gradient(90deg, #455f73, #e7f6fa, #536f82);
    border: 2px solid #607c8e;
    transform: rotate(18deg);
}

.mic:after {
    content: "";
    position: absolute;
    width: 12px;
    height: 3px;
    background: #42677c;
    left: 6px;
    top: 12px;
    box-shadow: 0 8px #42677c, 0 16px #42677c;
}

.base {
    position: absolute;
    bottom: 12px;
    width: 260px;
    height: 25px;
    border-radius: 50%;
    background: linear-gradient(#faffff, #7e9eaf);
    border: 2px solid #8ba7b7;
    box-shadow: 0 10px 18px #6b8797;
}

.wave {
    position: absolute;
    top: 48%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #d17fc9, #6bd9e7, transparent);
    box-shadow: 0 0 14px #8de7f3;
    opacity: .8;
}

.wave:before {
    content: "〰 〰 〰 〰 〰 〰 〰 〰 〰 〰 〰";
    position: absolute;
    top: -25px;
    left: 0;
    width: 100%;
    color: #8b9fd1;
    font-size: 26px;
    letter-spacing: 4px;
    white-space: nowrap;
    overflow: hidden;
    animation: pulse 2s ease-in-out infinite;
}

.circuit {
    position: absolute;
    width: 200px;
    height: 90px;
    border-top: 1px solid #9bc9d9;
    border-right: 1px solid #9bc9d9;
    opacity: .7;
}
.circuit.one { right: 0; top: 180px; }
.circuit.two { left: 0; bottom: 65px; transform: rotate(180deg); }

.caption {
    position: absolute;
    bottom: 26px;
    right: 35px;
    color: #537286;
    font-size: 10px;
    letter-spacing: 2px;
}

@keyframes float {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}
@keyframes pulse {
    0%,100% { opacity: .45; transform: scaleY(.8); }
    50% { opacity: 1; transform: scaleY(1.2); }
}

@media(max-width: 700px) {
    .hero { min-height: 690px; padding: 22px; }
    .nav-links { display: none; }
    .hero-title { top: 100px; left: 7%; }
    .hero-title h1 { font-size: 42px; }
    .robot-area {
        width: 100%;
        right: 0;
        top: 310px;
        transform: scale(.82);
    }
    .caption { bottom: 12px; right: 15px; }
}
</style>
</head>

<body>
<div class="hero">

    <div class="nav">
        <div class="logo">VOICEGUARD</div>
        <div class="nav-links">
            OVERVIEW　 TECHNOLOGY　 VOICE ANALYSIS
        </div>
    </div>

    <div class="hero-title">
        <div class="eyebrow">INTELLIGENT AUDIO AUTHENTICATION</div>
        <h1>AI VOICE<br>VERIFICATION</h1>
        <p>
            Discover the difference between genuine human speech
            and AI-generated voices using intelligent audio analysis.
        </p>
        <div class="hero-button">ANALYSE YOUR AUDIO ↓</div>
    </div>

    <div class="robot-area">
        <div class="wave"></div>
        <div class="circuit one"></div>
        <div class="circuit two"></div>
        <div class="orb">
            <div class="brain"></div>
        </div>

        <div class="robot">
            <div class="head">
                <div class="face">
                    <div class="eye left"></div>
                    <div class="eye right"></div>
                    <div class="mouth"></div>
                </div>
            </div>
            <div class="neck"></div>
            <div class="body">
                <div class="chest"></div>
                <div class="mic"></div>
            </div>
        </div>
        <div class="base"></div>
    </div>

    <div class="caption">VOICEGUARD · NEURAL AUDIO SYSTEM</div>
</div>
</body>
</html>
"""

components.html(hero_html, height=610, scrolling=False)


# ---------------- FEATURE STRIP ----------------

st.markdown("""
<div style="
display:flex;
flex-wrap:wrap;
gap:12px;
margin:18px 0 28px 0;
">
<div style="flex:1;min-width:180px;background:#ffffffbd;
padding:20px;border:1px solid #d7e2e9;border-radius:14px;">
<div style="font-size:25px;">🎙️</div>
<b>Audio Input</b><br>
<small>WAV and MP3 support</small>
</div>
<div style="flex:1;min-width:180px;background:#ffffffbd;
padding:20px;border:1px solid #d7e2e9;border-radius:14px;">
<div style="font-size:25px;">〰️</div>
<b>Mel Spectrogram</b><br>
<small>Audio feature analysis</small>
</div>
<div style="flex:1;min-width:180px;background:#ffffffbd;
padding:20px;border:1px solid #d7e2e9;border-radius:14px;">
<div style="font-size:25px;">🧠</div>
<b>Deep Learning</b><br>
<small>Voice classification model</small>
</div>
</div>
""", unsafe_allow_html=True)


# ---------------- AUDIO UPLOAD ----------------

st.markdown("## 🎧 Analyse Your Voice")
st.write(
    "Upload an audio recording below to prepare it for "
    "genuine human voice or AI-generated voice analysis."
)

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3"]
)

if uploaded_file is not None:

    st.success("Audio uploaded successfully!")

    st.audio(uploaded_file)

    st.markdown("### Audio Information")

    st.write("**File name:**", uploaded_file.name)
    st.write(
        "**File size:**",
        f"{uploaded_file.size / 1024:.2f} KB"
    )

    st.info(
        "Your audio is ready. The trained voice-classification "
        "model will provide the genuine/AI result once integrated."
    )

    st.button(
        "🔍 Analyse Voice",
        disabled=True,
        help="Model integration is still pending."
    )

else:
    st.info("Upload a WAV or MP3 file to begin.")


# ---------------- FOOTER ----------------

st.markdown("""
<hr>
<div style="text-align:center;color:#718394;font-size:12px;">
VOICEGUARD · AI VOICE CLONING DETECTION PROJECT<br>
Built with Python, PyTorch and Streamlit
</div>
""", unsafe_allow_html=True)
