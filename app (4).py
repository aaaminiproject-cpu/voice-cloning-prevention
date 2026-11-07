"""VoxGuard - single-file app (Member 3). Run: streamlit run app.py"""
# ================= STYLE =================
"""VoxGuard styling + hero visual (Member 3)."""
LIGHT = dict(bg="#f4f6fb", surf="#ffffff", surf2="#e9eef7", ink="#12151f", mute="#5d6678", accent="#2f5bff", vio="#8b5cf6", line="#dbe2ee")
DARK = dict(bg="#0b0e17", surf="#141926", surf2="#1b2233", ink="#eef1f8", mute="#99a3b8", accent="#6b8cff", vio="#a78bfa", line="#273049")

def css(t):
    v = "".join(f"--{k}:{x};" for k, x in t.items())
    return f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif&display=swap');
:root{{{v}}}
html,body,[class*="css"],.stApp{{font-family:'Inter',sans-serif;color:var(--ink)}}
.stApp{{background:radial-gradient(900px 500px at 85% -10%,color-mix(in srgb,var(--vio) 18%,transparent),transparent),var(--bg)}}
#MainMenu,footer,header[data-testid="stHeader"]{{visibility:hidden;height:0}}
.block-container{{max-width:1180px;padding:1rem 1.2rem 4rem}}
h1,h2,h3{{font-family:'Instrument Serif',serif!important;font-weight:400!important;letter-spacing:-.01em;color:var(--ink)}}
h2{{font-size:2.4rem!important}} p,li,label,span{{color:inherit}}
.brand{{font-weight:600;letter-spacing:.28em;font-size:.95rem}} .brand b{{color:var(--accent)}}
.eyebrow{{color:var(--accent);font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;font-weight:600}}
.mute{{color:var(--mute)}}
.card{{background:var(--surf);border:1px solid var(--line);border-radius:22px;padding:1.3rem 1.4rem;animation:up .6s both;transition:transform .25s,box-shadow .25s}}
.card:hover{{transform:translateY(-3px);box-shadow:0 18px 40px -22px var(--accent)}}
.hero-t{{font-family:'Instrument Serif',serif;font-size:clamp(2.6rem,7vw,5rem);line-height:1.02;margin:.3rem 0 1rem}}
.hero-t span{{background:linear-gradient(100deg,var(--accent),var(--vio),var(--accent));background-size:200%;-webkit-background-clip:text;color:transparent;animation:flow 6s linear infinite}}
.big{{font-family:'Instrument Serif',serif;font-size:2.2rem;line-height:1.1}}
.bar{{height:10px;border-radius:99px;background:var(--surf2);overflow:hidden;margin:.35rem 0 1rem}}
.bar i{{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--vio));animation:grow 1s both}}
.pill{{display:inline-block;padding:.25rem .8rem;border-radius:99px;background:var(--surf2);font-size:.78rem;margin:.15rem .2rem .15rem 0}}
.step{{flex:1;min-width:150px;position:relative}} .flow{{display:flex;gap:.8rem;flex-wrap:wrap}}
.num{{font-family:'Instrument Serif',serif;font-size:2.4rem;color:var(--accent)}}
.status{{border-left:4px solid var(--vio);background:var(--surf2);padding:1rem 1.2rem;border-radius:14px}}
div[data-testid="stRadio"]>div{{flex-direction:row;gap:.3rem;overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none;padding:.3rem}}
div[data-testid="stRadio"] label{{background:var(--surf);border:1px solid var(--line);border-radius:99px;padding:.35rem .95rem;white-space:nowrap;cursor:pointer;transition:.2s}}
div[data-testid="stRadio"] label:hover{{border-color:var(--accent);transform:translateY(-1px)}}
div[data-testid="stRadio"] label:has(input:checked){{background:var(--ink);color:var(--bg)}}
div[data-testid="stRadio"] label>div:first-child{{display:none}}
.stButton>button,.stDownloadButton>button{{border-radius:99px;border:1px solid var(--line);background:var(--surf);color:var(--ink);padding:.55rem 1.3rem;font-weight:500;transition:.25s}}
.stButton>button:hover{{background:linear-gradient(100deg,var(--accent),var(--vio));color:#fff;border-color:transparent;transform:translateY(-2px)}}
div[data-testid="stFileUploader"] section{{border:2px dashed var(--line);border-radius:26px;background:var(--surf);padding:2.2rem 1rem;transition:.25s}}
div[data-testid="stFileUploader"] section:hover{{border-color:var(--accent);background:var(--surf2)}}
.stProgress>div>div>div{{background:linear-gradient(90deg,var(--accent),var(--vio))}}
@keyframes up{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
@keyframes flow{{to{{background-position:200%}}}} @keyframes grow{{from{{width:0}}}}
@media(max-width:640px){{.block-container{{padding:.6rem .8rem 4rem}}h2{{font-size:1.8rem!important}}.card{{padding:1rem}}.step{{min-width:100%}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style>"""

def hero(t):
    a, v, i = t["accent"], t["vio"], t["ink"]
    paths = "".join(f'<path class="w w{n}" d="M-400 {200+n*0} Q-300 {120-n*18} -200 200 T0 200 T200 200 T400 200 T600 200 T800 200 T1000 200" fill="none" stroke="url(#g)" stroke-width="{3-n*.6}" opacity="{.9-n*.22}"/>' for n in range(3))
    bars = "".join(f'<rect x="{150+k*22}" y="{200-10}" width="10" rx="5" height="20" fill="url(#g)" class="b" style="animation-delay:{k*.07:.2f}s"/>' for k in range(25))
    return f"""<div style="height:440px"><svg viewBox="0 0 800 400" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
<defs><linearGradient id="g"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{v}"/></linearGradient>
<radialGradient id="o"><stop offset="0" stop-color="{v}" stop-opacity=".35"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient></defs>
<circle cx="400" cy="200" r="190" fill="url(#o)" class="p"/><circle cx="400" cy="200" r="130" fill="none" stroke="{a}" stroke-opacity=".25" class="p2"/>
{bars}{paths}
<g transform="translate(400 200)"><rect x="-30" y="-78" width="60" height="110" rx="30" fill="{i}" opacity=".92"/>
<path d="M-48 0v10a48 48 0 0 0 96 0V0" fill="none" stroke="{i}" stroke-width="6" stroke-linecap="round"/><path d="M0 58v34M-24 92h48" stroke="{i}" stroke-width="6" stroke-linecap="round"/>
<g stroke="#fff" stroke-opacity=".35" stroke-width="3"><path d="M-18 -50h36M-18 -34h36M-18 -18h36M-18 -2h36"/></g></g></svg>
<style>svg{{overflow:visible}}.w{{animation:m 9s linear infinite}}.w1{{animation-duration:13s}}.w2{{animation-duration:17s;animation-direction:reverse}}
@keyframes m{{to{{transform:translateX(-200px)}}}}.b{{transform-box:fill-box;transform-origin:center;animation:e 1.4s ease-in-out infinite}}
@keyframes e{{0%,100%{{transform:scaleY(.4)}}50%{{transform:scaleY(5)}}}}.p{{transform-origin:400px 200px;animation:pu 4s ease-in-out infinite}}
.p2{{transform-origin:400px 200px;animation:pu 4s 1s ease-in-out infinite}}@keyframes pu{{50%{{transform:scale(1.08)}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style></div>"""

# ================= CORE =================
"""VoxGuard core (Member 3): real audio features, model bridge, history.
No predictions are ever generated here. Predictions come only from Member 2's adapter."""
import os, json, time, tempfile, importlib
from pathlib import Path
import numpy as np, librosa
import plotly.graph_objects as go

SR = int(os.getenv("VOXGUARD_SR", "22050"))   # TODO: set to Member 1's sample rate
N_MELS = int(os.getenv("VOXGUARD_N_MELS", "128"))  # display only
HIST = Path(os.getenv("VOXGUARD_HISTORY", "voxguard_history.json"))

def load_audio(data: bytes, name: str):
    with tempfile.NamedTemporaryFile(suffix=Path(name).suffix, delete=False) as f:
        f.write(data); p = f.name
    try: y, sr = librosa.load(p, sr=SR, mono=True)
    finally: os.remove(p)
    return y, sr

def features(y, sr):
    S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS), ref=np.max)
    sp = np.abs(np.fft.rfft(y)); fr = np.fft.rfftfreq(len(y), 1 / sr)
    return dict(
        duration=len(y) / sr, sr=sr, y=y, mel=S,
        cent=librosa.feature.spectral_centroid(y=y, sr=sr)[0],
        roll=librosa.feature.spectral_rolloff(y=y, sr=sr)[0],
        mfcc=librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13),
        dom=float(fr[np.argmax(sp[1:]) + 1]) if len(sp) > 1 else 0.0,
        rms=float(np.sqrt(np.mean(y ** 2))))

def find_checkpoint():
    c = [os.getenv("VOXGUARD_MODEL_PATH"), "member2_model.pth", "models/member2_model.pth"]
    try:
        import streamlit as st; c.insert(1, st.secrets.get("MODEL_PATH"))
    except Exception: pass
    for p in c:
        if p and Path(p).is_file(): return str(p)
    gid = os.getenv("VOXGUARD_GDRIVE_ID")  # optional Google Drive file id
    if gid:
        try:
            import gdown; Path("models").mkdir(exist_ok=True)
            gdown.download(id=gid, output="models/member2_model.pth", quiet=True)
            if Path("models/member2_model.pth").is_file(): return "models/member2_model.pth"
        except Exception: pass
    return None

def run_model(y, sr):
    """SINGLE INTEGRATION POINT. Returns dict(status, message, genuine, spoof, label)."""
    bad = lambda s, m: dict(status=s, message=m)
    ck = find_checkpoint()
    if not ck: return bad("unavailable", "member2_model.pth not found. Set VOXGUARD_MODEL_PATH, add it to secrets as MODEL_PATH, or set VOXGUARD_GDRIVE_ID.")
    os.environ["VOXGUARD_MODEL_PATH"] = ck
    try: ad = importlib.import_module("model_adapter")
    except Exception as e: return bad("unavailable", f"model_adapter.py could not be imported: {e}")
    fn = next((getattr(ad, n) for n in ("predict", "predict_audio") if hasattr(ad, n)), None)
    if fn is None: return bad("unavailable", "No predict()/predict_audio() in model_adapter.py. Edit run_model() in app.py to match its real interface.")
    try: out = fn(y, sr)
    except Exception as e: return bad("error", f"Adapter call failed ({type(e).__name__}): {e}. Adjust run_model() to the adapter's real signature.")
    try:
        g = float(out.get("genuine", out.get("real"))); s = float(out.get("spoof", out.get("fake")))
        if g > 1 or s > 1: g, s = g / 100, s / 100
        assert 0 <= g <= 1 and 0 <= s <= 1
    except Exception: return bad("error", f"Unrecognised adapter output: {out!r}. Expected keys genuine/spoof.")
    return dict(status="ok", genuine=g, spoof=s, label="genuine" if g >= s else "spoof", message="")

def _hist():
    try: return json.loads(HIST.read_text())
    except Exception: return []
def hist_load(): return _hist()
def hist_add(rec):
    h = _hist(); h.insert(0, rec); HIST.write_text(json.dumps(h[:100]))
def hist_clear():
    try: HIST.unlink()
    except Exception: pass
def now(): return time.strftime("%d %b %Y, %H:%M")

# ---- Plotly figures (real data only) ----
def _fig(h=260, t=None):
    t = t or {}
    f = go.Figure(); f.update_layout(height=h, margin=dict(l=8, r=8, t=8, b=8), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color=t.get("ink", "#222"), size=11)); return f
def fig_wave(F, t=None):
    y = F["y"]; k = max(1, len(y) // 3000); x = np.arange(0, len(y), k) / F["sr"]
    f = _fig(200, t); f.add_scatter(x=x, y=y[::k], line=dict(color=(t or {}).get("accent", "#2f5bff"), width=1), fill="tozeroy")
    f.update_xaxes(title="seconds", showgrid=False); f.update_yaxes(showgrid=False, zeroline=False); return f
def fig_mel(F, t=None, key="mel"):
    f = _fig(280, t); f.add_heatmap(z=F[key], colorscale="Viridis" if key == "mel" else "Purples", showscale=False)
    f.update_xaxes(title="time frames"); f.update_yaxes(title="mel band" if key == "mel" else "MFCC"); return f
def fig_spec(F, t=None):
    ts = librosa.times_like(F["cent"], sr=F["sr"]); f = _fig(240, t)
    f.add_scatter(x=ts, y=F["cent"], name="Centroid", line=dict(color="#2f5bff"))
    f.add_scatter(x=ts, y=F["roll"], name="Rolloff", line=dict(color="#8b5cf6"))
    f.update_layout(legend=dict(orientation="h", y=1.15)); f.update_xaxes(title="seconds"); f.update_yaxes(title="Hz"); return f

# ================= UI + PAGES =================
import sys, hashlib
from pathlib import Path
import streamlit as st, streamlit.components.v1 as components
import numpy as np

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
    y, sr = load_audio(data, up.name); bar.progress(35, "Computing spectral features…")
    F = features(y, sr); bar.progress(65, "Running detection model…")
    R = run_model(y, sr); bar.progress(100, "Done"); bar.empty()
    return dict(name=up.name, size=len(data), ts=now(), F=F, R=R)

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
    hist_add(dict(name=rec["name"], ts=rec["ts"], status=R["status"], duration=round(rec["F"]["duration"], 2),
        label=R.get("label"), genuine=R.get("genuine"), spoof=R.get("spoof"), note=R["message"]))

def go_to(page_name):
    """Button callback: runs before the nav widget is created on the next rerun."""
    st.session_state["nav"] = page_name

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
        c1.button("Upload Audio  →", use_container_width=True, on_click=go_to, args=("Detect",))
        c2.button("Explore Technology", use_container_width=True, on_click=go_to, args=("Technology",))
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
        with l: st.markdown("**Waveform**"); plot(fig_wave(rec["F"], T))
        with r: st.markdown("**Mel spectrogram**"); plot(fig_mel(rec["F"], T))
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
        with l: st.markdown("**Waveform**"); plot(fig_wave(F, T))
        with r: st.markdown("**Mel spectrogram**"); plot(fig_mel(F, T))
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
        st.markdown("**Waveform**"); plot(fig_wave(F, T))
        st.markdown("**Mel spectrogram**"); plot(fig_mel(F, T))
        st.markdown("**Spectral centroid and rolloff**"); plot(fig_spec(F, T))
        st.markdown("**MFCC (13 coefficients)**"); plot(fig_mel(F, T, "mfcc"))

elif page == "History":
    head("Records", "Detection history")
    h = hist_load()
    if not h: st.info("No analyses yet.")
    for i, r in enumerate(h):
        lab = {"genuine": "Genuine", "spoof": "AI / Spoof"}.get(r["label"], "No prediction")
        conf = f' · {pct(max(r["genuine"], r["spoof"]))}' if r.get("genuine") is not None else ""
        with st.expander(f'{r["name"]} · {r["ts"]} · {lab}{conf}'):
            st.write(f'Status: **{r["status"]}** · Duration {r["duration"]} s')
            if r.get("genuine") is not None: st.write(f'Genuine {pct(r["genuine"])} · Spoof {pct(r["spoof"])}')
            if r.get("note"): st.caption(r["note"])
    if h and st.button("Clear history"): hist_clear(); st.rerun()
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
                plot(fig_wave(rec["F"], T)); plot(fig_mel(rec["F"], T))
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
