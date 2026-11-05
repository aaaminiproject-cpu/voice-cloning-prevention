"""VoiceGuard - Member 3 website. Run: streamlit run app.py"""
import streamlit as st
from member3 import audio_analysis as aa, model_adapter as ma, report as rp, styles as sty

REPO = "https://github.com/aaaminiproject-cpu/voice-cloning-prevention"
MAX_MB = 25

st.set_page_config(page_title="VoiceGuard", page_icon="🛡️", layout="wide")
st.markdown(sty.CSS, unsafe_allow_html=True)
ss = st.session_state
ss.setdefault("current", None); ss.setdefault("history", [])

st.markdown(f"""<div class="nav"><b>🛡️ VoiceGuard</b><a href="#home">Home</a><a href="#how">How It Works</a>
<a href="#analysis">Analysis</a><a href="#about">About Project</a><a href="{REPO}" target="_blank">GitHub</a></div>
<div id="home"></div>""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>AI Voice Cloning Detection</h1>'
            '<p>VoiceGuard inspects an audio recording, visualises its signal (waveform, Mel spectrogram, spectral '
            'features) and is built to classify it as a genuine human voice or an AI-generated / cloned voice using a '
            'PyTorch CNN on Mel spectrograms.</p></div>', unsafe_allow_html=True)
robot_slot = st.empty()

st.markdown('<div id="how"></div><div class="sec">How It Works</div>', unsafe_allow_html=True)
c = st.columns(4)
for col, (t, d) in zip(c, [("1 · Upload", "WAV or MP3 recording."), ("2 · Preprocess", "Member 1: mono, 16 kHz, normalise."),
                           ("3 · Detect", "Member 2: Mel spectrogram + CNN."), ("4 · Report", "Verdict, graphs, download.")]):
    col.markdown(f'<div class="card"><h3>{t}</h3>{d}</div>', unsafe_allow_html=True)

st.markdown('<div id="analysis"></div><div class="sec">Audio Upload</div>', unsafe_allow_html=True)
up = st.file_uploader("Upload a WAV or MP3 file", type=["wav", "mp3"], help=f"Max {MAX_MB} MB")

state = "welcome"
if up is not None:
    data = up.getvalue()
    if len(data) > MAX_MB * 1024 * 1024:
        st.error(f"File is larger than {MAX_MB} MB."); up = None
if up is not None:
    h = aa.file_hash(data)
    if ss.current and ss.current["hash"] != h:
        aa.close_figures(ss.current["figs"]); ss.current = None   # never show stale analysis
    state = "listening"
    st.audio(data, format="audio/mp3" if up.name.lower().endswith(".mp3") else "audio/wav")
    st.caption(f"**{up.name}** · {len(data)/1024:.1f} KB · SHA-256 {h[:12]}…")
    if st.button("🔍 Analyse Audio", type="primary"):
        robot_slot.markdown(sty.robot_html("scanning"), unsafe_allow_html=True)
        try:
            with st.spinner("Scanning audio..."):
                y, sr, total = aa.load_audio(data)
                rec = {"name": up.name, "size_kb": len(data) / 1024, "hash": h, "time": rp.now(),
                       "features": aa.features(y, sr, total), "figs": aa.make_figures(y, sr),
                       "prediction": ma.predict(data, up.name)}
            if ss.current:
                aa.close_figures(ss.current["figs"])
            ss.current = rec
            if not any(x["hash"] == h for x in ss.history):
                ss.history.append({k: v for k, v in rec.items() if k != "figs"})
        except ValueError as e:
            st.error(str(e))
else:
    if ss.current:
        aa.close_figures(ss.current["figs"]); ss.current = None

cur = ss.current
if cur:
    p = cur["prediction"]
    state = ("genuine" if p["predicted_class"] == ma.GENUINE else "ai") if p["model_available"] else "neutral"
robot_slot.markdown(sty.robot_html(state), unsafe_allow_html=True)

if cur:
    st.markdown('<div class="sec">Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="pill p-info">Inspection complete · {cur["time"]}</span>', unsafe_allow_html=True)
    f = list(cur["features"].items())
    for i in range(0, len(f), 5):
        for col, (k, v) in zip(st.columns(5), f[i:i + 5]):
            col.metric(k, v)
    figs = cur["figs"]
    st.pyplot(figs["Waveform"]); st.pyplot(figs["Mel spectrogram"])
    a, b = st.columns(2); a.pyplot(figs["Spectral centroid"]); b.pyplot(figs["Roll-off / bandwidth"])
    st.pyplot(figs["MFCCs"])

    st.markdown('<div class="sec">Detection Result</div>', unsafe_allow_html=True)
    if p["model_available"]:
        cls = "p-ok" if p["predicted_class"] == ma.GENUINE else "p-bad"
        st.markdown(f'<span class="pill {cls}">{p["predicted_class"]}</span>', unsafe_allow_html=True)
        st.metric("Confidence", f'{p["confidence"]:.2%}')
        for k, v in (p["probabilities"] or {}).items():
            st.write(k); st.progress(float(v))
        st.write(p["message"])
    else:
        st.markdown(f'<div class="demo"><b>Model integration pending.</b> {p["message"]}<br>'
                    'The graphs above are real signal analysis of your file. They are not evidence that the voice '
                    'is genuine or AI-generated.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec">Inspection Report</div>', unsafe_allow_html=True)
    txt = rp.build_report(cur)
    st.code(txt, language=None)
    st.download_button("⬇️ Download report", txt, f"voiceguard_report_{cur['hash'][:8]}.txt")

st.markdown('<div class="sec">Analysis History (this session)</div>', unsafe_allow_html=True)
if ss.history:
    import pandas as pd
    st.dataframe(pd.read_csv(__import__("io").StringIO(rp.history_csv(ss.history))), use_container_width=True)
    st.download_button("⬇️ Download history CSV", rp.history_csv(ss.history), "voiceguard_history.csv")
else:
    st.caption("No analyses yet. Uploaded audio is held in memory only and is never saved to disk.")

st.markdown(f"""<div id="about"></div><div class="sec">About Project</div>
<div class="card">AI Detection and Prevention of Voice Cloning and Impersonation Attacks Using Mel Spectrogram with PyTorch.
<br><b>Team:</b> Anthony - audio preprocessing &amp; dataset · Afan - Mel spectrogram &amp; CNN model · Abhishek - website &amp; integration.</div>
<div class="foot"><b>VoiceGuard</b> · College mini-project · <a href="{REPO}" style="color:#67e8f9">GitHub</a></div>""",
            unsafe_allow_html=True)
