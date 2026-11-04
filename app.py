import os
import tempfile
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="VoiceGuard | AI Voice Verification", page_icon="🎙️", layout="wide")

# ---------------- SESSION STATE ----------------
for key, default in {
    "analysis_result": None,
    "analysis_file_name": None,
    "analysis_file_id": None,
    "analysis_history": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- THEME ----------------
st.markdown("""
<style>
.stApp{background:#edf2f5;color:#101b2b}
.block-container{max-width:1250px;padding-top:1rem;padding-bottom:3rem}
header[data-testid="stHeader"]{background:transparent}
footer{visibility:hidden}
.stButton>button{background:#101b2b;color:white;border:1px solid #101b2b;
border-radius:10px;padding:.65rem 1.5rem;font-weight:600;width:100%}
.stButton>button:hover{background:#29455e;color:white;border-color:#29455e}
section[data-testid="stFileUploader"]{background:white;border:1px solid #d6e0e8;
border-radius:16px;padding:18px}
div[data-testid="stMetric"]{background:white;border:1px solid #d6e0e8;
border-radius:12px;padding:15px}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO: ORIGINAL ROBOT DESIGN ----------------
hero_html = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;font-family:Arial;background:transparent;color:#101b2b}
.hero{position:relative;min-height:590px;overflow:hidden;border-radius:22px;
background:radial-gradient(ellipse at 65% 43%,#c9e4f0 0%,transparent 38%),
linear-gradient(115deg,#f8fafb,#e7eef2 65%,#dce7ed);padding:28px 34px}
.nav{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:5}
.logo{font-size:25px;font-weight:900;letter-spacing:3px}
.nav-links{font-size:12px;letter-spacing:1px;color:#263548}
.hero-title{position:absolute;left:4%;top:34%;z-index:4;max-width:390px}
.eyebrow{color:#477e9d;font-size:11px;letter-spacing:3px;font-weight:bold}
.hero-title h1{font-size:clamp(40px,5vw,67px);line-height:.98;margin:15px 0;
letter-spacing:-2px;font-weight:900}
.hero-title p{font-size:14px;line-height:1.6;color:#526477;max-width:320px}
.hero-button{display:inline-block;margin-top:16px;padding:13px 23px;border:1.5px solid #17283a;
border-radius:9px;font-size:12px;font-weight:bold;letter-spacing:1px}
.robot-area{position:absolute;width:54%;height:460px;right:1%;top:90px;
display:flex;align-items:center;justify-content:center}
.orb{position:absolute;width:360px;height:360px;border-radius:50%;
background:radial-gradient(circle at 35% 30%,#fff 0%,#d8edf4 28%,#91b7ca 62%,#587d93 100%);
border:5px solid rgba(95,133,155,.5);box-shadow:0 0 35px #9bc9df,inset 0 0 35px #fff;
animation:float 5s ease-in-out infinite}
.orb:before,.orb:after{content:"";position:absolute;border:1px solid rgba(255,255,255,.8);
border-radius:50%;inset:15px}.orb:after{inset:28px;border-color:rgba(73,159,190,.4)}
.brain{position:absolute;top:42px;left:50%;transform:translateX(-50%);width:175px;height:120px;
border-radius:50% 50% 42% 42%;background:radial-gradient(ellipse,#f6c9ef 0%,#a8e9f2 35%,#8f9be8 65%,transparent 72%);
filter:drop-shadow(0 0 17px #b4eaff)}
.brain:before,.brain:after{content:"";position:absolute;inset:8px 20px;border:2px solid rgba(255,255,255,.85);border-radius:48%}
.brain:after{inset:20px 42px;border-color:rgba(255,255,255,.75)}
.robot{position:absolute;top:145px;width:210px;height:260px;display:flex;flex-direction:column;
align-items:center;filter:drop-shadow(0 15px 15px rgba(25,50,70,.25))}
.head{width:125px;height:125px;border-radius:48% 48% 42% 42%;
background:linear-gradient(130deg,#f9ffff,#9bb6c5 50%,#e6f3f6);border:4px solid #7f9baa;
position:relative;z-index:2;box-shadow:inset -10px -8px 18px #7795a7}
.face{position:absolute;top:42px;left:17px;width:83px;height:38px;border-radius:20px;
background:linear-gradient(90deg,#142b42,#315b73);box-shadow:0 0 15px #8de9ff}
.eye{position:absolute;top:13px;width:9px;height:9px;border-radius:50%;background:#a4f4ff;box-shadow:0 0 9px #9af5ff}
.eye.left{left:20px}.eye.right{right:20px}
.mouth{position:absolute;width:18px;height:3px;background:#b8e9f4;bottom:7px;left:32px;border-radius:5px}
.neck{width:48px;height:42px;background:linear-gradient(90deg,#607e91,#eaf6fa,#69889b);
border-radius:10px;margin-top:-2px}
.body{width:185px;height:110px;margin-top:-2px;border-radius:48% 48% 18% 18%;
background:linear-gradient(110deg,#7894a5,#f4fbfd 45%,#7f9baa);border:3px solid #8ca7b5;position:relative}
.chest{position:absolute;width:58px;height:58px;border-radius:50%;
background:radial-gradient(circle,#d7ffff,#62c6df 40%,#315a75);border:3px solid #d9faff;
top:17px;left:61px;box-shadow:0 0 20px #7deaff}
.mic{position:absolute;width:28px;height:50px;right:-18px;top:24px;border-radius:15px;
background:linear-gradient(90deg,#455f73,#e7f6fa,#536f82);border:2px solid #607c8e;transform:rotate(18deg)}
.mic:after{content:"";position:absolute;width:12px;height:3px;background:#42677c;left:6px;top:12px;
box-shadow:0 8px #42677c,0 16px #42677c}
.base{position:absolute;bottom:12px;width:260px;height:25px;border-radius:50%;
background:linear-gradient(#faffff,#7e9eaf);border:2px solid #8ba7b7;box-shadow:0 10px 18px #6b8797}
.wave{position:absolute;top:48%;width:100%;height:2px;
background:linear-gradient(90deg,transparent,#d17fc9,#6bd9e7,transparent);box-shadow:0 0 14px #8de7f3}
.wave:before{content:"〰 〰 〰 〰 〰 〰 〰 〰 〰 〰";position:absolute;top:-25px;left:0;width:100%;
color:#8b9fd1;font-size:26px;letter-spacing:4px;white-space:nowrap;overflow:hidden;animation:pulse 2s ease-in-out infinite}
.circuit{position:absolute;width:200px;height:90px;border-top:1px solid #9bc9d9;border-right:1px solid #9bc9d9;opacity:.7}
.circuit.one{right:0;top:180px}.circuit.two{left:0;bottom:65px;transform:rotate(180deg)}
.caption{position:absolute;bottom:26px;right:35px;color:#537286;font-size:10px;letter-spacing:2px}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes pulse{0%,100%{opacity:.45;transform:scaleY(.8)}50%{opacity:1;transform:scaleY(1.2)}}
@media(max-width:700px){.hero{min-height:690px;padding:22px}.nav-links{display:none}
.hero-title{top:100px;left:7%}.hero-title h1{font-size:42px}
.robot-area{width:100%;right:0;top:310px;transform:scale(.82)}.caption{bottom:12px;right:15px}}
</style></head><body><div class="hero">
<div class="nav"><div class="logo">VOICEGUARD</div><div class="nav-links">OVERVIEW　 TECHNOLOGY　 VOICE ANALYSIS</div></div>
<div class="hero-title"><div class="eyebrow">INTELLIGENT AUDIO AUTHENTICATION</div>
<h1>AI VOICE<br>VERIFICATION</h1>
<p>Discover the difference between genuine human speech and AI-generated voices using intelligent audio analysis.</p>
<div class="hero-button">ANALYSE YOUR AUDIO ↓</div></div>
<div class="robot-area"><div class="wave"></div><div class="circuit one"></div><div class="circuit two"></div>
<div class="orb"><div class="brain"></div></div>
<div class="robot"><div class="head"><div class="face"><div class="eye left"></div><div class="eye right"></div><div class="mouth"></div></div></div>
<div class="neck"></div><div class="body"><div class="chest"></div><div class="mic"></div></div></div><div class="base"></div></div>
<div class="caption">VOICEGUARD · NEURAL AUDIO SYSTEM</div></div></body></html>
"""
components.html(hero_html, height=610, scrolling=False)

# ---------------- FEATURE CARDS ----------------
st.markdown("""
<div style="display:flex;flex-wrap:wrap;gap:12px;margin:18px 0 28px">
<div style="flex:1;min-width:180px;background:white;padding:20px;border:1px solid #d7e2e9;border-radius:14px">
<div style="font-size:25px">🎙️</div><b>Audio Input</b><br><small>WAV and MP3 support</small></div>
<div style="flex:1;min-width:180px;background:white;padding:20px;border:1px solid #d7e2e9;border-radius:14px">
<div style="font-size:25px">〰️</div><b>Mel Spectrogram</b><br><small>Audio feature analysis</small></div>
<div style="flex:1;min-width:180px;background:white;padding:20px;border:1px solid #d7e2e9;border-radius:14px">
<div style="font-size:25px">🧠</div><b>Deep Learning</b><br><small>Voice classification model</small></div>
</div>
""", unsafe_allow_html=True)

# ---------------- AUDIO PROCESSING ----------------
def inspect_audio(audio_bytes, file_name):
    suffix = os.path.splitext(file_name)[1].lower()
    if suffix not in (".wav", ".mp3"):
        suffix = ".wav"

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        signal, sample_rate = librosa.load(temp_path, sr=16000, mono=True)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    if signal is None or len(signal) == 0:
        raise ValueError("The uploaded audio is empty or could not be decoded.")

    duration = len(signal) / sample_rate
    rms = float(np.sqrt(np.mean(np.square(signal))))
    peak = float(np.max(np.abs(signal)))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(signal)[0]))
    centroid_graph = librosa.feature.spectral_centroid(y=signal, sr=sample_rate)[0]
    spectral_centroid = float(np.mean(centroid_graph))
    mel = librosa.feature.melspectrogram(y=signal, sr=sample_rate, n_fft=1024,
                                         hop_length=256, n_mels=64)
    mel_db = librosa.power_to_db(mel, ref=np.max)

    return {
        "signal": signal,
        "sample_rate": int(sample_rate),
        "duration": float(duration),
        "rms": rms,
        "peak": peak,
        "zero_crossing": zcr,
        "spectral_centroid": spectral_centroid,
        "centroid_graph": centroid_graph,
        "mel_db": mel_db,
    }

# ---------------- UPLOAD ----------------
st.markdown("---")
st.markdown("""
<div style="background:white;border:1px solid #d6e0e8;border-radius:16px;padding:20px">
<div style="color:#477e9d;font-size:11px;letter-spacing:2px;font-weight:bold">VOICE ANALYSIS</div>
<h2 style="color:#101b2b;margin:8px 0">Upload Your Audio</h2>
<p style="color:#607487">Upload a WAV or MP3 recording to inspect its audio characteristics and generate an analysis report.</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("🎙️ Choose an audio file", type=["wav", "mp3"], key="voiceguard_audio")

if uploaded_file is not None:
    file_id = (uploaded_file.name, uploaded_file.size)
    if st.session_state.analysis_file_id != file_id:
        st.session_state.analysis_result = None
        st.session_state.analysis_file_name = None
        st.session_state.analysis_file_id = file_id

    st.success("Audio uploaded successfully.")
    st.audio(uploaded_file.getvalue())
    st.caption(f"File: {uploaded_file.name} · Size: {uploaded_file.size / 1024:.1f} KB")

    if st.button("🔍 Analyse Audio", key="analyse_button"):
        try:
            with st.status("VoiceGuard is inspecting your audio...", expanded=True) as status:
                st.write("Reading and decoding uploaded audio...")
                computed_result = inspect_audio(uploaded_file.getvalue(), uploaded_file.name)
                st.write("Extracting audio characteristics...")
                st.write("Generating waveform and Mel spectrogram...")
                st.write("Preparing inspection report...")

                # Store complete result before dashboard rendering.
                st.session_state.analysis_result = computed_result
                st.session_state.analysis_file_name = uploaded_file.name
                st.session_state.analysis_file_id = file_id

                status.update(label="Audio inspection completed", state="complete", expanded=False)

            st.session_state.analysis_history.insert(0, {
                "file_name": uploaded_file.name,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "duration": computed_result["duration"],
                "sample_rate": computed_result["sample_rate"],
                "rms": computed_result["rms"],
                "peak": computed_result["peak"],
                "zero_crossing": computed_result["zero_crossing"],
                "spectral_centroid": computed_result["spectral_centroid"],
                "classification": "Pending trained model integration",
            })
            st.success("Your audio inspection report is ready.")
        except Exception as error:
            st.session_state.analysis_result = None
            st.error(f"Could not analyse this audio: {error}")
else:
    st.info("Choose a WAV or MP3 file above to begin audio inspection.")

# ---------------- DASHBOARD ----------------
# This condition protects every use of result. It is not dependent on
# a temporary local variable from a previous Streamlit rerun.
if st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result
    file_name = st.session_state.analysis_file_name or "Uploaded audio"

    st.markdown("---")
    st.markdown("## 📊 Voice Analysis Dashboard")
    st.markdown("### Current Inspection Status")
    st.success("Audio inspection completed successfully.")
    st.info("Signal analysis is complete. Genuine-versus-AI voice classification requires connecting the trained PyTorch model.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Duration", f"{result['duration']:.2f} sec")
    c2.metric("Sample Rate", f"{result['sample_rate']} Hz")
    c3.metric("RMS Energy", f"{result['rms']:.4f}")
    c4.metric("Peak Amplitude", f"{result['peak']:.4f}")

    st.markdown("---")
    st.markdown("### 1. Audio Waveform")
    signal = result["signal"]
    sr = result["sample_rate"]
    times = np.arange(len(signal)) / sr
    step = max(1, len(signal) // 12000)
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(times[::step], signal[::step], linewidth=0.6)
    ax.set(xlabel="Time (seconds)", ylabel="Amplitude", title="Audio Waveform")
    ax.grid(alpha=0.2)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("---")
    st.markdown("### 2. Mel Spectrogram")
    fig, ax = plt.subplots(figsize=(12, 4))
    im = ax.imshow(result["mel_db"], aspect="auto", origin="lower", interpolation="nearest")
    ax.set(xlabel="Time Frames", ylabel="Mel Frequency Bands", title="Mel Spectrogram")
    fig.colorbar(im, ax=ax, format="%+2.0f dB")
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("---")
    st.markdown("### 3. Audio Feature Analysis")
    left, right = st.columns(2)
    with left:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(result["centroid_graph"], linewidth=1)
        ax.set(xlabel="Frame", ylabel="Frequency (Hz)", title="Spectral Centroid")
        ax.grid(alpha=0.2)
        st.pyplot(fig)
        plt.close(fig)
    with right:
        names = ["RMS Energy", "Peak", "Zero Crossing"]
        values = [result["rms"], result["peak"], result["zero_crossing"]]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(names, values)
        ax.set_title("Audio Feature Measurements")
        ax.tick_params(axis="x", rotation=15)
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("---")
    st.markdown("### 4. Inspection Report")
    report_lines = [
        "VOICEGUARD - AUDIO INSPECTION REPORT",
        "====================================",
        "",
        f"File name: {file_name}",
        f"Inspection date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        "",
        "AUDIO INFORMATION",
        "-----------------",
        f"Sample rate: {result['sample_rate']} Hz",
        f"Duration: {result['duration']:.3f} seconds",
        f"RMS energy: {result['rms']:.6f}",
        f"Peak amplitude: {result['peak']:.6f}",
        f"Zero crossing rate: {result['zero_crossing']:.6f}",
        f"Average spectral centroid: {result['spectral_centroid']:.2f} Hz",
        "",
        "ANALYSIS OUTPUT",
        "---------------",
        "Waveform: Generated",
        "Mel spectrogram: Generated",
        "Audio feature graphs: Generated",
        "",
        "VOICE CLASSIFICATION",
        "--------------------",
        "Pending trained model integration.",
        "",
        "This report contains audio measurements only.",
        "It does not confirm whether the voice is genuine or AI-generated.",
    ]
    report_text = "\n".join(report_lines)
    st.text_area("Report Preview", report_text, height=300)
    st.download_button("📄 Download Inspection Report", data=report_text,
                       file_name="voiceguard_inspection_report.txt", mime="text/plain")
else:
    st.markdown("---")
    st.info("Your analysis dashboard will appear here after you upload an audio file and click Analyse Audio.")

# ---------------- HISTORY ----------------
st.markdown("---")
st.markdown("## 🕘 Analysis History")
if st.session_state.analysis_history:
    history_df = pd.DataFrame(st.session_state.analysis_history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download Analysis History", data=history_df.to_csv(index=False),
                       file_name="voiceguard_analysis_history.csv", mime="text/csv")
else:
    st.info("No analysis history yet. Upload an audio file and click Analyse Audio to create your first record.")

# ---------------- FOOTER ----------------
footer_html = """
<style>
.vg-footer{background:#1d304b;color:#f5f8fc;padding:38px 30px 20px;border-radius:16px;
margin-top:35px;font-family:Arial,sans-serif}
.vg-footer a{color:#dce7f3;text-decoration:none;display:block;margin:12px 0;font-size:14px}
.vg-footer a:hover{color:#83e5f5}
.vg-footer h3{color:white;font-size:22px;letter-spacing:2px}
.vg-footer h4{color:#91d7e8;font-size:14px;margin-bottom:15px}
.vg-footer p{color:#c3d0df;font-size:13px;line-height:1.7}
.vg-bottom{border-top:1px solid #52647a;margin-top:28px;padding-top:17px;text-align:center;color:#b9c7d6;font-size:12px}
</style>
<div class="vg-footer">
<div style="display:flex;flex-wrap:wrap;gap:35px;justify-content:space-between">
<div style="flex:2;min-width:220px"><h3>VOICEGUARD</h3><p>Intelligent AI voice verification.<br>Helping distinguish genuine human speech from AI-generated voices through audio analysis.</p></div>
<div style="flex:1;min-width:130px"><h4>EXPLORE</h4><a href="#overview">About Us</a><a href="#technology">Technology</a><a href="#news">Blog</a><a href="#contact">Contact</a></div>
<div style="flex:1;min-width:170px"><h4>INFORMATION</h4><a href="#privacy">Privacy</a><a href="#terms">Terms</a><a href="#security">Security and Compliance</a><a href="#status">System Status</a></div>
<div style="flex:1;min-width:130px"><h4>PROJECT</h4><a href="https://github.com/aaaminiproject-cpu/voice-cloning-prevention" target="_blank">GitHub Repository</a><a href="#team">Our Team</a></div>
</div>
<div class="vg-bottom">© 2026 VoiceGuard | AI Voice Cloning Detection Project<br>Built with Python · PyTorch · Streamlit</div>
</div>
"""
components.html(footer_html, height=340, scrolling=False)
