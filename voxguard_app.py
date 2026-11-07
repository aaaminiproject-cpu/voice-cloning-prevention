"""VoxGuard UI (Member 3). Run: streamlit run voxguard_ui/voxguard_app.py"""
import sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import streamlit as st, streamlit.components.v1 as components
import numpy as np
import vox_core as C
from vox_style import LIGHT, DARK, css, hero

st.set_page_config(page_title="VoxGuard", page_icon="🎙️", layout="wide", initial_sidebar_state="collapsed")
ss = st.session_state
ss.setdefault("dark", False); ss.setdefault("cur", None); ss.setdefault("nav", "Home")
T = DARK if ss.dark else LIGHT
st.markdown(css(T), unsafe_allow_html=True)
PAGES = ["Home", "Detect", "Results", "Analysis", "History", "Compare", "Technology", "About"]

def pct(x): return f"{x*100:.1f}%"
def card(html): st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)
def head(eye, title, sub=""):
    st.markdown(f'<div class="eyebrow">{eye}</div><h2>{title}</h2><p class="mute">{sub}</p>', unsafe_allow_html=True)
def plot(fig): st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))

def process(up):
    """Real pipeline: decode -> features -> model adapter. Returns record dict."""
    data = up.getvalue(); bar = st.progress(0, "Decoding audio…")
    y, sr = C.load_audio(data, up.name); bar.progress(35, "Computing spectral features…")
    F = C.features(y, sr); bar.progress(65, "Running detection model…")
    R = C.run_model(y, sr); bar.progress(100, "Done"); bar.empty()
    return dict(name=up.name, size=len(data), ts=C.now(), F=F, R=R)

def uploader(key, label="Drop a WAV or MP3 file"):
    up = st.file_uploader(label, type=["wav", "mp3"], key=key)
    if up is None: return None
    c = (key, up.name, hashlib.md5(up.getvalue()).hexdigest())
    if ss.get(key + "_id") != c:
        ss[key + "_rec"] = process(up); ss[key + "_id"] = c
    return ss[key + "_rec"]

def status_box(R):
    if R["status"] != "ok":
        st.markdown(f'<div class="status"><b>Model integration: {R["status"]}</b><br>{R["message"]}<br><span class="mute">No prediction is shown because none was produced by the trained model.</span></div>', unsafe_allow_html=True)

def meta(rec):
    F = rec["F"]; return f'<span class="pill">{rec["name"]}</span><span class="pill">{F["duration"]:.2f} s</span><span class="pill">{rec["size"]/1e6:.2f} MB</span><span class="pill">{F["sr"]} Hz</span>'

def verdict(R):
    if R["status"] != "ok": return
    g = R["label"] == "genuine"
    st.markdown(f'<div class="card"><div class="eyebrow">Classification</div><div class="big">{"Genuine Human Voice" if g else "AI-Generated or Cloned Voice"}</div>'
      f'<p class="mute">Model confidence, not a guarantee of authenticity.</p>'
      f'<div>Genuine · {pct(R["genuine"])}</div><div class="bar"><i style="width:{R["genuine"]*100}%"></i></div>'
      f'<div>AI / Spoof · {pct(R["spoof"])}</div><div class="bar"><i style="width:{R["spoof"]*100}%"></i></div></div>', unsafe_allow_html=True)

def save(rec):
    R = rec["R"]; ok = R["status"] == "ok"
    C.hist_add(dict(name=rec["name"], ts=rec["ts"], status=R["status"], duration=round(rec["F"]["duration"], 2),
        label=R.get("label"), genuine=R.get("genuine"), spoof=R.get("spoof"), note=R["message"]))

# ---------- top bar ----------
a, b = st.columns([5, 1])
a.markdown('<div class="brand">VOX<b>GUARD</b></div>', unsafe_allow_html=True)
if b.button("☾ / ☀", key="theme", use_container_width=True): ss.dark = not ss.dark; st.rerun()
page = st.radio("nav", PAGES, key="nav", horizontal=True, label_visibility="collapsed")

# ---------- pages ----------
if page == "Home":
    l, r = st.columns([1.1, 1])
    with l:
        st.markdown(f'<div style="padding-top:2rem" class="reveal"><div class="eyebrow">AI voice authenticity</div><div class="hero-t">Trust Every Voice.<br><span>Verify Every Signal.</span></div>'
          '<p class="mute" style="max-width:34rem;font-size:1.05rem">Advanced AI-powered voice authenticity analysis designed to identify synthetic, cloned and potentially manipulated audio.</p></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("Upload Audio  →", use_container_width=True): ss.nav = "Detect"; st.rerun()
        if c2.button("Explore Technology", use_container_width=True): ss.nav = "Technology"; st.rerun()
    with r: components.html(hero(T), height=450)
    st.write("")
    for col, (n, t, d) in zip(st.columns(3), [("01", "Upload", "WAV or MP3, drag and drop."), ("02", "Analyse", "Mel spectrogram fed to a PyTorch CNN."), ("03", "Review", "Confidence scores with real audio features.")]):
        with col: card(f'<div class="num">{n}</div><b>{t}</b><p class="mute">{d}</p>')

elif page == "Detect":
    head("Workspace", "Audio detection", "Upload a recording to run the full pipeline.")
    rec = uploader("main")
    if rec:
        ss.cur = rec
        if ss.get("saved") != ss.get("main_id"): save(rec); ss.saved = ss.get("main_id")
        card(meta(rec)); st.audio(rec["F"]["y"], sample_rate=rec["F"]["sr"])
        status_box(rec["R"]); verdict(rec["R"])
        l, r = st.columns(2)
        with l: st.markdown("**Waveform**"); plot(C.fig_wave(rec["F"], T))
        with r: st.markdown("**Mel spectrogram**"); plot(C.fig_mel(rec["F"], T))
        st.caption("Remove the file with ✕ above to replace it.")
    else:
        card('<b>No audio yet.</b><p class="mute">Supported: WAV, MP3. Your file is processed in this session.</p>')

elif page == "Results":
    head("Report", "Detection results")
    rec = ss.cur
    if not rec: st.info("Upload audio in Detect first.")
    else:
        card(meta(rec)); status_box(rec["R"]); verdict(rec["R"])
        F = rec["F"]; l, r = st.columns(2)
        with l: st.markdown("**Waveform**"); plot(C.fig_wave(F, T))
        with r: st.markdown("**Mel spectrogram**"); plot(C.fig_mel(F, T))
        card(f'<b>Summary</b><p class="mute">Duration {F["duration"]:.2f} s at {F["sr"]} Hz. RMS energy {F["rms"]:.4f}. Mean spectral centroid {np.mean(F["cent"]):.0f} Hz. '
             'Detection output reflects the trained CNN\'s confidence on this clip; it is not a guaranteed probability and can be wrong on unfamiliar voices, noise or codecs.</p>')

elif page == "Analysis":
    head("Signal analysis", "Audio features", "All values computed from your uploaded file with librosa.")
    rec = ss.cur
    if not rec: st.info("Upload audio in Detect first.")
    else:
        F = rec["F"]
        for col, (k, v) in zip(st.columns(4), [("Dominant freq", f'{F["dom"]:.0f} Hz'), ("Spectral centroid", f'{np.mean(F["cent"]):.0f} Hz'), ("Spectral rolloff", f'{np.mean(F["roll"]):.0f} Hz'), ("Nyquist", f'{F["sr"]/2:.0f} Hz')]):
            with col: card(f'<div class="mute">{k}</div><div class="big">{v}</div>')
        st.markdown("**Waveform**"); plot(C.fig_wave(F, T))
        st.markdown("**Mel spectrogram**"); plot(C.fig_mel(F, T))
        st.markdown("**Spectral centroid and rolloff**"); plot(C.fig_spec(F, T))
        st.markdown("**MFCC (13 coefficients)**"); plot(C.fig_mel(F, T, "mfcc"))

elif page == "History":
    head("Records", "Detection history")
    h = C.hist_load()
    if not h: st.info("No analyses yet.")
    for i, r in enumerate(h):
        lab = {"genuine": "Genuine", "spoof": "AI / Spoof"}.get(r["label"], "No prediction")
        conf = f' · {pct(max(r["genuine"], r["spoof"]))}' if r.get("genuine") is not None else ""
        with st.expander(f'{r["name"]} · {r["ts"]} · {lab}{conf}'):
            st.write(f'Status: **{r["status"]}** · Duration {r["duration"]} s')
            if r.get("genuine") is not None: st.write(f'Genuine {pct(r["genuine"])} · Spoof {pct(r["spoof"])}')
            if r.get("note"): st.caption(r["note"])
    if h and st.button("Clear history"): C.hist_clear(); st.rerun()
    st.caption("Stored in a local JSON file on the server. On shared hosting it may be visible to all visitors and reset on restart.")

elif page == "Compare":
    head("Side by side", "Compare two samples", "Compares model outputs and audio characteristics only. It does not identify speakers.")
    l, r = st.columns(2)
    with l: A = uploader("cA", "Sample A")
    with r: B = uploader("cB", "Sample B")
    if A and B:
        for col, rec in zip(st.columns(2), (A, B)):
            with col:
                card(meta(rec)); status_box(rec["R"]); verdict(rec["R"])
                plot(C.fig_wave(rec["F"], T)); plot(C.fig_mel(rec["F"], T))
                F = rec["F"]; st.caption(f'Centroid {np.mean(F["cent"]):.0f} Hz · Rolloff {np.mean(F["roll"]):.0f} Hz · Dominant {F["dom"]:.0f} Hz')

elif page == "Technology":
    head("Under the hood", "The detection pipeline")
    steps = [("Audio input", "WAV/MP3 decoded to mono."), ("Preprocessing", "Librosa resampling and normalisation (Member 1)."), ("Mel spectrogram", "Time-frequency image of the voice."),
             ("CNN (PyTorch)", "Convolutional network trained by Member 2."), ("Classification", "Genuine vs spoof confidence.")]
    st.markdown('<div class="flow">' + "".join(f'<div class="card step"><div class="num">{i+1}</div><b>{t}</b><p class="mute">{d}</p></div>' for i, (t, d) in enumerate(steps)) + '</div>', unsafe_allow_html=True)
    st.write("")
    for col, (t, d) in zip(st.columns(3), [("PyTorch", "Deep learning framework running the model."), ("CNNs", "Learn local patterns in spectrograms that separate natural and synthetic speech."), ("Librosa", "Audio loading, Mel spectrograms, MFCCs, spectral features.")]):
        with col: card(f"<b>{t}</b><p class='mute'>{d}</p>")

else:
    head("About", "VoxGuard")
    card('<p class="big" style="font-size:1.6rem">VoxGuard is an AI-based voice authenticity detection system designed to help identify synthetic and cloned voice recordings.</p>')
    st.write("")
    for col, (n, r_, w) in zip(st.columns(3), [("Antony", "Member 1", "Audio Preprocessing"), ("Afan", "Member 2", "Deep Learning and Detection Model"), ("Abhishek", "Member 3", "Website Development, UI/UX and Integration")]):
        with col: card(f'<div class="eyebrow">{r_}</div><div class="big">{n}</div><p class="mute">{w}</p>')
