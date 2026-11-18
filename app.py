"""VoxGuard - single-file app. Run: streamlit run app.py"""
import os, json, time, tempfile, hashlib
from pathlib import Path
import numpy as np, librosa
import plotly.graph_objects as go
import streamlit as st, streamlit.components.v1 as components

CONTACT = "aaa.miniproject@gmail.com"

# ================= STYLE =================
T = dict(ink="#f4f1ea", accent="#e2b866", vio="#8b7bff")

STYLE = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap');
:root{--bg:#06070b;--ink:#f4f1ea;--mute:#8d93a6;--gold:#e2b866;--gold2:#f6dc9b;--vio:#8b7bff;--good:#5ee0a0;--bad:#ff6b81;--line:rgba(255,255,255,.09);--glass:rgba(255,255,255,.04)}
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif;color:var(--ink)}
.stApp{background:radial-gradient(800px 520px at 8% -6%,rgba(139,123,255,.22),transparent 60%),radial-gradient(850px 520px at 96% 8%,rgba(226,184,102,.15),transparent 60%),radial-gradient(900px 600px at 50% 115%,rgba(139,123,255,.13),transparent 60%),var(--bg);background-attachment:fixed}
#MainMenu,footer,header[data-testid="stHeader"]{visibility:hidden;height:0}
.block-container{max-width:1160px;padding:1.2rem 1.2rem 3rem}
h1,h2,h3{font-family:'Instrument Serif',serif!important;font-weight:400!important;letter-spacing:-.01em;color:var(--ink)}
h2{font-size:2.8rem!important;line-height:1.05!important}
.stApp p,.stApp li,.stApp label,.stApp summary,.stApp [data-testid="stMarkdownContainer"]{color:var(--ink)!important}
.stApp [data-testid="stCaptionContainer"],.stApp [data-testid="stCaptionContainer"] *{color:var(--mute)!important}
.stApp .mute{color:var(--mute)!important}
.stApp a{color:var(--gold)!important;text-decoration:none}
.brand{font-weight:600;letter-spacing:.38em;font-size:.95rem;padding-top:.7rem}
.stApp .brand b,.stApp .eyebrow,.stApp .num{color:var(--gold)!important}
.eyebrow{font-size:.72rem;letter-spacing:.26em;text-transform:uppercase;font-weight:600;margin-bottom:.35rem}
.gold{background:linear-gradient(100deg,#f6dc9b,#e2b866 45%,#b88a3e);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent!important;color:transparent}
.card{background:linear-gradient(155deg,rgba(255,255,255,.075),rgba(255,255,255,.02));border:1px solid var(--line);border-radius:26px;padding:1.4rem 1.5rem;margin-bottom:.9rem;backdrop-filter:blur(14px);box-shadow:0 30px 60px -42px #000,inset 0 1px 0 rgba(255,255,255,.07);animation:up .6s both;transition:transform .3s,border-color .3s,box-shadow .3s}
.card:hover{transform:translateY(-3px);border-color:rgba(226,184,102,.45);box-shadow:0 26px 60px -34px rgba(226,184,102,.45)}
.hero-t{font-family:'Instrument Serif',serif;font-size:clamp(2.8rem,7vw,5.2rem);line-height:1;margin:.4rem 0 1.1rem}
.big{font-family:'Instrument Serif',serif;font-size:2.1rem;line-height:1.1}
.num{font-family:'Instrument Serif',serif;font-size:2.4rem}
.ico{font-size:1.8rem;margin-bottom:.3rem}
.bar{height:8px;border-radius:99px;background:rgba(255,255,255,.07);overflow:hidden;margin:.35rem 0 1rem}
.bar i{display:block;height:100%;border-radius:99px;animation:grow 1s both}
.bar i.g{background:linear-gradient(90deg,#2fbf85,var(--good))}
.bar i.s{background:linear-gradient(90deg,#e0475f,var(--bad))}
.pill{display:inline-block;padding:.28rem .85rem;border-radius:99px;background:rgba(255,255,255,.06);border:1px solid var(--line);font-size:.76rem;margin:.15rem .25rem .15rem 0}
.status{border-left:4px solid var(--vio);background:rgba(255,255,255,.05);padding:1rem 1.2rem;border-radius:16px;margin-bottom:.9rem}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.7rem;margin-top:.5rem}
.tile{background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:18px;padding:.8rem 1rem}
.tk{color:var(--mute);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase}
.tv{font-family:'Instrument Serif',serif;font-size:1.7rem;line-height:1.2}
.vrow{display:flex;gap:1.4rem;align-items:center;flex-wrap:wrap}
.ring{width:150px;height:150px;flex:none}
.ring .rg{animation:ringgrow 1.2s ease both}
.ring .rt{font-family:'Instrument Serif',serif;font-size:30px;fill:var(--ink)}
.ring .rl{font-size:9px;letter-spacing:.2em;fill:var(--mute);text-transform:uppercase}
.flow{display:flex;gap:.8rem;flex-wrap:wrap}.step{flex:1;min-width:150px}
.avatar{width:62px;height:62px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Instrument Serif',serif;font-size:1.7rem;color:#1a1304;background:linear-gradient(135deg,#f6dc9b,#e2b866 55%,#b88a3e);margin-bottom:.8rem}
.cta{display:inline-block;padding:.65rem 1.5rem;border-radius:99px;background:linear-gradient(100deg,#f6dc9b,#e2b866);font-weight:600;transition:.25s}
.stApp a.cta{color:#1a1304!important}
.cta:hover{transform:translateY(-2px);box-shadow:0 14px 34px -12px var(--gold)}
.foot{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.8rem;border-top:1px solid var(--line);margin-top:3rem;padding-top:1.4rem;font-size:.85rem}
.foot .brand{padding-top:0;font-size:.8rem}
div[data-testid="stRadio"]{display:flex;justify-content:flex-end}
div[data-testid="stRadio"]>div{flex-direction:row;gap:.2rem;overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none;padding:.35rem;background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:99px;backdrop-filter:blur(12px);max-width:100%}
div[data-testid="stRadio"] label{background:transparent;border:0;border-radius:99px;padding:.4rem 1.1rem;white-space:nowrap;cursor:pointer;transition:.25s;font-weight:500}
div[data-testid="stRadio"] label:hover{background:rgba(255,255,255,.07)}
div[data-testid="stRadio"] label:has(input:checked){background:linear-gradient(100deg,#f6dc9b,#e2b866)}
div[data-testid="stRadio"] label>div:first-child{display:none}
.stApp div[data-testid="stRadio"] label:has(input:checked),.stApp div[data-testid="stRadio"] label:has(input:checked) *{color:#1a1304!important}
.stButton>button,.stDownloadButton>button{border-radius:99px;border:1px solid var(--line);background:rgba(255,255,255,.05);padding:.6rem 1.4rem;font-weight:500;transition:.25s;backdrop-filter:blur(10px)}
.stApp .stButton button,.stApp .stButton button *{color:var(--ink)!important}
.stButton>button:hover{background:linear-gradient(100deg,#f6dc9b,#e2b866);border-color:transparent;transform:translateY(-2px);box-shadow:0 14px 34px -14px var(--gold)}
.stApp .stButton button:hover,.stApp .stButton button:hover *{color:#1a1304!important}
div[data-testid="stFileUploader"] section{border:1.5px dashed rgba(226,184,102,.4);border-radius:26px;background:rgba(255,255,255,.03);padding:1.8rem 1rem;transition:.25s}
div[data-testid="stFileUploader"] section:hover{border-color:var(--gold);background:rgba(226,184,102,.06)}
.stApp [data-testid="stFileUploaderDropzone"] *{color:var(--mute)!important}
.stApp [data-testid="stFileUploaderDropzone"] button{background:linear-gradient(100deg,#f6dc9b,#e2b866)!important;border-radius:99px!important;border:none!important}
.stApp [data-testid="stFileUploaderDropzone"] button *{color:#1a1304!important}
div[data-baseweb="select"]>div{background:rgba(255,255,255,.05)!important;border:1px solid var(--line)!important;border-radius:16px!important}
[data-testid="stAudioInput"]>div{background:rgba(255,255,255,.04)!important;border:1px solid var(--line)!important;border-radius:22px!important}
[data-testid="stExpander"] details{background:rgba(255,255,255,.03);border:1px solid var(--line)!important;border-radius:18px}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--gold),var(--vio))}
.stApp [data-testid="stAlert"]{background:rgba(18,24,42,.92)!important;border:1px solid rgba(226,184,102,.35)!important;border-radius:18px!important}
.stApp [data-testid="stAlert"] *{color:#fff!important}
.stApp [data-testid="stAlert"] svg{fill:#fff!important}
.marq{overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:.7rem 0;margin:2rem 0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent);mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.marq .track{display:flex;gap:2.2rem;width:max-content;animation:scrollx 30s linear infinite}
.marq span{font-family:'Instrument Serif',serif;font-size:1.7rem;white-space:nowrap}
.marq span:nth-child(even){color:var(--gold)}
.eq{display:flex;gap:4px;align-items:flex-end;height:46px;margin:.8rem 0}
.eq i{width:6px;height:100%;border-radius:4px;background:linear-gradient(var(--gold),var(--vio));transform-origin:bottom;animation:eqb 1.2s ease-in-out infinite}
.band{background:linear-gradient(120deg,#0d0f1c,#1d1b4b 60%,#3b2a8c);border:1px solid var(--line);border-radius:30px;padding:2.2rem 1.8rem;margin:1.6rem 0 .8rem}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes grow{from{width:0}}
@keyframes ringgrow{from{stroke-dasharray:0 400}}
@keyframes scrollx{to{transform:translateX(-50%)}}
@keyframes eqb{0%,100%{transform:scaleY(.15)}50%{transform:scaleY(1)}}
.stApp ::-webkit-scrollbar{width:8px;height:8px}
.stApp ::-webkit-scrollbar-thumb{background:rgba(255,255,255,.12);border-radius:99px}
@media(max-width:640px){.block-container{padding:.8rem .8rem 3rem}h2{font-size:2rem!important}.card{padding:1.1rem}.step{min-width:100%}div[data-testid="stRadio"]{justify-content:flex-start}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
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


EQ = '<div class="eq">' + ''.join(f'<i style="animation-delay:{k*0.09:.2f}s"></i>' for k in range(32)) + '</div>'
_items = ["PyTorch", "Convolutional Neural Networks", "Mel Spectrograms", "Librosa", "MFCC", "Spectral Centroid", "Deep Learning", "Genuine vs Spoof"]
MARQ = ''.join(f'<span>{x}</span><span>✦</span>' for x in _items * 2)

# ================= CORE (unchanged logic) =================
SR = int(os.getenv("VOXGUARD_SR", "16000"))   # Member 1 spec: 16 kHz mono
N_MELS = int(os.getenv("VOXGUARD_N_MELS", "64"))  # Member 1 spec: 64 mel bands (display)
HIST = Path(os.getenv("VOXGUARD_HISTORY", "voxguard_history.json"))

def load_audio(data: bytes, name: str):
    """Decode an uploaded or microphone recording to finite mono 16 kHz audio."""
    if not data:
        raise ValueError("The audio recording is empty. Please record or upload it again.")

    suffix = Path(name or "audio.wav").suffix.lower()
    if not suffix or len(suffix) > 10:
        suffix = ".wav"

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(data)
            temp_path = f.name
        y, sr = librosa.load(temp_path, sr=SR, mono=True)
    except Exception as exc:
        raise ValueError(
            f"Could not decode this audio file ({type(exc).__name__}). "
            "Try a WAV or MP3 recording."
        ) from exc
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

    y = np.asarray(y, dtype=np.float32).reshape(-1)
    if y.size == 0:
        raise ValueError("No audio samples were found in this recording.")
    if not np.isfinite(y).all():
        y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
    if float(np.max(np.abs(y))) < 1e-7:
        raise ValueError("The recording is silent or too quiet. Please record it again.")
    return y, int(sr)

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

def _secret(k):
    try: return st.secrets.get(k)
    except Exception: return None

def find_checkpoint():
    names = ["member2_model.pth", "models/member2_model.pth", "src/member2_model.pth", "model/member2_model.pth", "checkpoints/member2_model.pth"]
    for p in [os.getenv("VOXGUARD_MODEL_PATH"), _secret("MODEL_PATH")] + names:
        if p and Path(p).is_file(): return str(p)
    gid = os.getenv("VOXGUARD_GDRIVE_ID") or _secret("VOXGUARD_GDRIVE_ID")  # Google Drive file id
    if gid:
        try:
            import gdown; Path("models").mkdir(exist_ok=True)
            gdown.download(id=str(gid), output="models/member2_model.pth", quiet=True)
            if Path("models/member2_model.pth").is_file() and Path("models/member2_model.pth").stat().st_size > 1000: return "models/member2_model.pth"
        except Exception: pass
    return None

_MODEL = {}

def find_v2_checkpoint():
    """Find the V2 checkpoint without ever confusing it with the V1 weights."""
    names = [
        "src/member2_model_v2_1_thresholded.pth",
        "member2_model_v2_1_thresholded.pth",
        "models/member2_model_v2_1_thresholded.pth",
        "checkpoints/member2_model_v2_1_thresholded.pth",
    ]
    for candidate in [os.getenv("VOXGUARD_V2_MODEL_PATH"), _secret("VOXGUARD_V2_MODEL_PATH")] + names:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    return None

def run_model(data: bytes, name: str, audio=None, sr=SR, model_version="V1"):
    """Run the selected model using its own architecture, preprocessing and weights."""
    bad = lambda status, message: dict(status=status, message=message, model_version=model_version)

    if model_version == "V2":
        ck = find_v2_checkpoint()
        if not ck:
            return bad("unavailable", "V2 checkpoint member2_model_v2_1_thresholded.pth was not found in src/ or the configured model path.")
        try:
            import torch
            from src.predict_v2 import load_v2_model
            from src.prevention import voxguard_prevention_engine
            cache_key = "V2:" + str(Path(ck).resolve())
            if cache_key not in _MODEL:
                _MODEL[cache_key] = load_v2_model(ck, device=torch.device("cpu"))
            model, device, _checkpoint = _MODEL[cache_key]
            if audio is None:
                audio, sr = load_audio(data, name)
            decision = voxguard_prevention_engine(audio, sr, model, device, source="upload")
            genuine = float(decision["genuine_score"]) / 100.0
            spoof = float(decision["spoof_score"]) / 100.0
            if not (0.0 <= genuine <= 1.0 and 0.0 <= spoof <= 1.0) or abs(genuine + spoof - 1.0) > 0.03:
                return bad("error", "V2 returned invalid class scores.")
            return dict(status="ok", genuine=genuine, spoof=spoof,
                        label="genuine" if genuine >= spoof else "spoof",
                        action=decision["action"], risk_status=decision["status"],
                        message=decision["message"], model_version="V2")
        except Exception as e:
            return bad("error", f"V2 inference failed ({type(e).__name__}): {e}")

    # V1 path intentionally retains its original checkpoint, loader and predictor.
    ck = find_checkpoint()
    if not ck:
        return bad("unavailable", "member2_model.pth not found. Put the V1 checkpoint in src/ or configure VOXGUARD_MODEL_PATH.")
    try:
        from src.predict import load_detection_model, predict_audio_file
        if ck not in _MODEL:
            _MODEL[ck] = load_detection_model(ck)
        model, device = _MODEL[ck]
    except Exception as e:
        return bad("error", f"V1 model failed to load ({type(e).__name__}): {e}")
    with tempfile.NamedTemporaryFile(suffix=Path(name).suffix or ".wav", delete=False) as f:
        f.write(data)
        temp_path = f.name
    try:
        out = predict_audio_file(temp_path, model, device)
    except Exception as e:
        return bad("error", f"V1 prediction failed ({type(e).__name__}): {e}")
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass
    try:
        genuine = float(out["genuine_probability"]) / 100.0
        spoof = float(out["spoof_probability"]) / 100.0
        if not (0.0 <= genuine <= 1.0 and 0.0 <= spoof <= 1.0) or abs(genuine + spoof - 1.0) >= 0.02:
            return bad("error", f"Unexpected V1 output scores: genuine={genuine:.4f}, spoof={spoof:.4f}")
    except Exception as e:
        return bad("error", f"Unexpected output from V1 predictor ({type(e).__name__}): {e}")
    return dict(status="ok", genuine=genuine, spoof=spoof,
                label="genuine" if genuine >= spoof else "spoof", message="", model_version="V1")

def _hist():
    try:
        if not HIST.exists():
            return []
        value = json.loads(HIST.read_text(encoding="utf-8"))
        return value if isinstance(value, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def hist_load():
    return _hist()


def hist_add(rec):
    h = _hist()
    h.insert(0, rec)
    HIST.parent.mkdir(parents=True, exist_ok=True)
    temp = HIST.with_suffix(HIST.suffix + ".tmp")
    temp.write_text(json.dumps(h[:100], ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(HIST)


def hist_clear():
    try:
        HIST.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass

def now(): return time.strftime("%d %b %Y, %H:%M")

# ---- Plotly figures (real data only) ----
def _fig(h=260, t=None):
    t = t or {}
    f = go.Figure(); f.update_layout(height=h, margin=dict(l=8, r=8, t=8, b=8), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color=t.get("ink", "#222"), size=11)); return f
def fig_wave(F, t=None):
    y = F["y"]; k = max(1, len(y) // 3000); x = np.arange(0, len(y), k) / F["sr"]
    f = _fig(200, t); f.add_scatter(x=x, y=y[::k], line=dict(color=(t or {}).get("accent", "#e2b866"), width=1), fill="tozeroy", fillcolor="rgba(226,184,102,.15)")
    f.update_xaxes(title="seconds", showgrid=False); f.update_yaxes(showgrid=False, zeroline=False); return f
def fig_mel(F, t=None, key="mel"):
    f = _fig(280, t); f.add_heatmap(z=F[key], colorscale="Magma" if key == "mel" else "Viridis", showscale=False)
    f.update_xaxes(title="time frames"); f.update_yaxes(title="mel band" if key == "mel" else "MFCC"); return f
def fig_spec(F, t=None):
    ts = librosa.times_like(F["cent"], sr=F["sr"]); f = _fig(240, t)
    f.add_scatter(x=ts, y=F["cent"], name="Centroid", line=dict(color="#e2b866"))
    f.add_scatter(x=ts, y=F["roll"], name="Rolloff", line=dict(color="#8b7bff"))
    f.update_layout(legend=dict(orientation="h", y=1.15)); f.update_xaxes(title="seconds"); f.update_yaxes(title="Hz"); return f

# ================= UI =================
st.set_page_config(page_title="VoxGuard", page_icon="🎙️", layout="wide", initial_sidebar_state="collapsed")
ss = st.session_state
ss.setdefault("cur", None); ss.setdefault("nav", "Home")
ss.setdefault("active_source", None)
ss.setdefault("last_upload_seen", None)
ss.setdefault("mic_saved", None)
st.markdown(STYLE, unsafe_allow_html=True)
PAGES = ["Home", "Detect", "Compare", "History", "About"]

def pct(x): return f"{x*100:.1f}%"
def card(html): st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)
def head(eye, title, sub=""):
    st.markdown(f'<div class="eyebrow gold">{eye}</div><h2>{title}</h2><p class="mute">{sub}</p>', unsafe_allow_html=True)
def plot(fig): st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))
def tile(k, v): return f'<div class="tile"><div class="tk">{k}</div><div class="tv">{v}</div></div>'

def process(up, model_version="V1", source="upload", run_detection=True):
    """Decode audio and compute features. Run the CNN only when run_detection=True."""
    data = up.getvalue()
    name = getattr(up, "name", None) or ("microphone.wav" if source == "microphone" else "audio.wav")
    if not data:
        raise ValueError("No audio data was received.")

    bar = st.progress(0, "Decoding audio…")
    try:
        y, sr = load_audio(data, name)
        bar.progress(35, "Computing signal features…")
        F = features(y, sr)
        if run_detection:
            bar.progress(65, "Running detection model…")
            R = run_model(data, name, audio=y, sr=sr, model_version=model_version)
        else:
            # Requested presentation mode: microphone inputs always show a fixed
            # Genuine demo label. This is NOT a model prediction or authenticity check.
            bar.progress(65, "Preparing microphone demo report…")
            R = dict(
                status="mic_demo",
                label="genuine_demo",
                message=("Fixed microphone demo display: this recording is shown as Genuine "
                         "without running the authenticity classifier. This label must not be "
                         "treated as a real detection result. Upload the same recording to get "
                         "the trained model's actual prediction."),
                model_version=model_version,
            )
        bar.progress(100, "Done")
        return dict(name=name, source=source, size=len(data), audio_bytes=data,
                    ts=now(), F=F, R=R, model_version=model_version)
    finally:
        bar.empty()


def uploader(key, label="Drop a WAV or MP3 file", model_version="V1"):
    up = st.file_uploader(label, type=["wav", "mp3"], key=key)
    if up is None:
        return None

    file_hash = hashlib.sha256(up.getvalue()).hexdigest()
    cache_id = (key, model_version, up.name, file_hash)
    if ss.get(key + "_id") != cache_id:
        try:
            ss[key + "_rec"] = process(up, model_version, source="upload")
            ss[key + "_id"] = cache_id
        except Exception as exc:
            ss[key + "_rec"] = None
            ss[key + "_id"] = cache_id
            st.error(f"Audio analysis could not be completed: {exc}")
    return ss.get(key + "_rec")

def status_box(R):
    if R["status"] in ("mic_demo", "not_evaluated"):
        st.warning("Below is your input audio  result")
    elif R["status"] != "ok":
        st.markdown(f'<div class="status"><b>Model integration: {R["status"]}</b><br>{R["message"]}<br><span class="mute">No prediction is shown because none was produced by the trained model.</span></div>', unsafe_allow_html=True)

def meta(rec):
    F = rec["F"]; return f'<span class="pill">{rec["name"]}</span><span class="pill">{F["duration"]:.2f} s</span><span class="pill">{rec["size"]/1e6:.2f} MB</span><span class="pill">{F["sr"]} Hz</span>'

def ring(p, col, label="CONFIDENCE"):
    c = 2 * 3.14159 * 54
    return (f'<svg class="ring" viewBox="0 0 140 140"><circle cx="70" cy="70" r="54" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="10"/>'
            f'<circle class="rg" cx="70" cy="70" r="54" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{c*p:.1f} {c:.1f}" transform="rotate(-90 70 70)"/>'
            f'<text class="rt" x="70" y="72" text-anchor="middle">{p*100:.0f}%</text><text class="rl" x="70" y="90" text-anchor="middle">{label}</text></svg>')

def verdict(R):
    if R["status"] in ("mic_demo", "not_evaluated"):
        # Fixed microphone demo meter: presentation only, NOT a model score.
        demo_genuine, demo_spoof = 1.0, 0.0
        st.markdown(
            '<div class="card"><div class="eyebrow">Microphone demo display · fixed label</div>'
            '<div class="vrow">' + ring(demo_genuine, "#5ee0a0", label="DEMO") +
            '<div style="flex:1;min-width:210px"><div class="big">Genuine Human Voice</div>'
            '<p class="mute" style="font-size:.85rem">Fixed demo meter: 100% Genuine / 0% AI-Spoof. This is not a classifier prediction or authenticity confidence. Uploaded files are evaluated by the trained model.</p></div></div>'
            '<div style="margin-top:1rem">Genuine · 100.0%</div><div class="bar"><i class="g" style="width:100%"></i></div>'
            '<div>AI / Spoof · 0.0%</div><div class="bar"><i class="s" style="width:0%"></i></div></div>',
            unsafe_allow_html=True,
        )
        return
    if R["status"] != "ok": return
    g = R["label"] == "genuine"; col = "#5ee0a0" if g else "#ff6b81"; p = R["genuine"] if g else R["spoof"]
    st.markdown(f'<div class="card"><div class="eyebrow">Classification</div><div class="vrow">{ring(p, col)}<div style="flex:1;min-width:210px">'
      f'<div class="big">{"Genuine Human Voice" if g else "AI-Generated or Cloned Voice"}</div>'
      f'<p class="mute" style="font-size:.85rem">Model confidence, not a guarantee of authenticity.</p></div></div>'
      f'<div style="margin-top:1rem">Genuine · {pct(R["genuine"])}</div><div class="bar"><i class="g" style="width:{R["genuine"]*100}%"></i></div>'
      f'<div>AI / Spoof · {pct(R["spoof"])}</div><div class="bar"><i class="s" style="width:{R["spoof"]*100}%"></i></div></div>', unsafe_allow_html=True)

def save(rec):
    R = rec["R"]
    hist_add(dict(name=rec["name"], source=rec.get("source", "upload"), ts=rec["ts"],
        status=R.get("status", "unknown"), duration=round(rec["F"]["duration"], 2),
        label=R.get("label"), genuine=R.get("genuine"), spoof=R.get("spoof"),
        model=R.get("model_version", rec.get("model_version", "V1")),
        action=R.get("action"), note=R.get("message", "")))

def go_to(page_name):
    """Button callback: runs before the nav widget is created on the next rerun."""
    st.session_state["nav"] = page_name

def clear_cur():
    st.session_state["cur"] = None
    st.session_state["active_source"] = "cleared"

def show_result(rec):
    """One combined result section: verdict, signal profile, playback, charts and deep analysis."""
    R, F = rec["R"], rec["F"]
    card(meta(rec) + f'<span class="pill">Model {rec.get("model_version", R.get("model_version", "V1"))}</span>')
    status_box(R)
    l, r = st.columns([1.15, 1])
    with l: verdict(R)
    with r:
        card('<div class="eyebrow">Signal profile</div><div class="tiles">' + tile("Duration", f'{F["duration"]:.1f} s') + tile("RMS energy", f'{F["rms"]:.3f}')
             + tile("Centroid", f'{np.mean(F["cent"]):.0f} Hz') + tile("Rolloff", f'{np.mean(F["roll"]):.0f} Hz') + tile("Dominant", f'{F["dom"]:.0f} Hz') + tile("Nyquist", f'{F["sr"]/2:.0f} Hz') + '</div>')
        can_play = (R.get("status") in ("not_evaluated", "mic_demo") or
                    (R.get("status") == "ok" and (R.get("model_version") != "V2" or R.get("action") == "ALLOW")))
        if can_play:
            st.audio(F["y"], sample_rate=F["sr"])
        if rec.get("source") == "microphone" and rec.get("audio_bytes"):
            st.download_button(
                "Download microphone recording for model test",
                data=rec["audio_bytes"],
                file_name="voxguard_microphone_test.wav",
                mime="audio/wav",
                key="download_mic_test",
                use_container_width=True,
            )
    if R.get("status") == "ok" and R.get("model_version") == "V2":
        action = R.get("action")
        st.subheader(f"V2 prevention decision: {action}")
        st.caption("Demonstration thresholds only; this is not a calibrated security boundary or proof of identity.")
        if action == "ALLOW":
            st.success("The model classified this recording as likely genuine. Playback is allowed within VoxGuard. This result is a model prediction, not a guarantee of the speaker's identity or the recording's authenticity.")
        elif action == "VERIFY":
            st.warning("This recording needs additional verification. Playback is paused; confirm the speaker's identity through an independent trusted channel.")
        else:
            st.error("This recording was classified as potentially AI-generated or voice-cloned. Playback has been blocked within VoxGuard pending independent verification. Your original uploaded audio file remains unchanged.")
    c1, c2 = st.columns(2)
    with c1: st.markdown("**Waveform**"); plot(fig_wave(F, T))
    with c2: st.markdown("**Mel spectrogram**"); plot(fig_mel(F, T))
    with st.expander("Deep signal analysis"):
        st.markdown("**Spectral centroid and rolloff**"); plot(fig_spec(F, T))
        st.markdown("**MFCC (13 coefficients)**"); plot(fig_mel(F, T, "mfcc"))
    if R.get("status") in ("mic_demo", "not_evaluated"):
        st.caption("Your uploded audios are anlysesd and shown in the result.")
    else:
        st.caption("Detection output reflects the trained CNN's confidence on this clip; it is not a guaranteed probability and can be wrong on unfamiliar voices, noise or codecs.")

def footer():
    st.markdown(f'<div class="foot"><div class="brand">VOX<b>GUARD</b></div><div>Contact · <a href="mailto:{CONTACT}">{CONTACT}</a></div>'
                f'<div class="mute">© VoxGuard · AI voice authenticity analysis</div></div>', unsafe_allow_html=True)

# ---------- top bar ----------
a, b = st.columns([1, 2.4])
a.markdown('<div class="brand">VOX<b>GUARD</b></div>', unsafe_allow_html=True)
with b: page = st.radio("nav", PAGES, key="nav", horizontal=True, label_visibility="collapsed")

# ---------- pages ----------
if page == "Home":
    l, r = st.columns([1.1, 1])
    with l:
        st.markdown('<div style="padding-top:2.2rem"><div class="eyebrow gold">AI voice authenticity</div><div class="hero-t">Trust every voice.<br><span class="gold"><i>Verify every signal.</i></span></div>'
          '<p class="mute" style="max-width:34rem;font-size:1.05rem">Advanced AI-powered voice analysis designed to identify synthetic, cloned and potentially manipulated audio.</p></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("Start detecting  →", use_container_width=True, on_click=go_to, args=("Detect",))
        c2.button("How it works", use_container_width=True, on_click=go_to, args=("About",))
    with r: components.html(hero(T), height=450)
    for col, (n, t, d) in zip(st.columns(3), [("16 kHz", "Mono analysis", "Every clip is resampled the same way before detection."), ("64", "Mel bands", "A time-frequency picture of the voice for the CNN."), ("2", "Detection models", "Baseline V1 and the advanced V2 with a prevention decision.")]):
        with col: card(f'<div class="num">{n}</div><b>{t}</b><p class="mute">{d}</p>')
    st.markdown('<div class="marq"><div class="track">' + MARQ + '</div></div>', unsafe_allow_html=True)
    for col, (ic, t, d) in zip(st.columns(3), [("🎙️", "Upload or record", "Drop a WAV or MP3, or record straight from your microphone."),
                                               ("🧠", "CNN-powered verdicts", "Genuine and spoof confidence straight from the trained PyTorch model."),
                                               ("🛡️", "Honest by design", "If the model is offline you get a clear status, never an invented score.")]):
        with col: card(f'<div class="ico">{ic}</div><b>{t}</b><p class="mute">{d}</p>')
    st.markdown('<div class="band"><div class="eyebrow gold">Ready when you are</div><div class="hero-t" style="font-size:clamp(2rem,5vw,3.2rem)">Is that voice <span class="gold"><i>real?</i></span></div><p class="mute">Drop in a recording and let VoxGuard read the signal.</p></div>', unsafe_allow_html=True)
    st.button("Start analysing  →", key="band_go", on_click=go_to, args=("Detect",))

elif page == "Detect":
    head("Workspace", "Detect a voice", "Choose a model, add a recording, and read the full report right below. All in one place.")
    model_choice = st.selectbox("Detection model", ["V1 — Baseline Model", "V2 — Advanced Model"], key="detection_model")
    selected_model = "V2" if model_choice.startswith("V2") else "V1"

    cu, cm = st.columns(2)
    with cu:
        st.markdown("**Upload a file**")
        rec = uploader("main", model_version=selected_model)
        # Only a newly uploaded file/model selection becomes the active result.
        # This prevents the upload result from replacing a microphone result on reruns.
        current_upload_id = ss.get("main_id")
        if rec is not None and current_upload_id != ss.get("last_upload_seen"):
            ss.cur = rec
            ss.active_source = "upload"
            ss.last_upload_seen = current_upload_id
        if rec is not None and ss.get("active_source") == "microphone":
            if st.button("Show uploaded-file result", key="show_upload_result", use_container_width=True):
                ss.cur = rec
                ss.active_source = "upload"

    with cm:
        st.markdown("**Or record with your microphone**")
        mic_audio = st.audio_input("Click to record your voice", sample_rate=SR, key="voxguard_microphone")
        if mic_audio is not None:
            st.caption("Please enter the audio using microphone for audio analysis")
            if st.button("Analyze recorded voice", key="analyze_mic", use_container_width=True):
                mic_hash = hashlib.sha256(mic_audio.getvalue()).hexdigest()
                mic_id = (mic_hash, selected_model)
                try:
                    with st.spinner("Analysing microphone recording…"):
                        mrec = process(
                            mic_audio,
                            model_version=selected_model,
                            source="microphone",
                            run_detection=False,
                        )
                    ss.cur = mrec
                    ss.active_source = "microphone"
                    st.success("Microphone recording captured. Fixed Genuine demo display shown; no authenticity model verdict was generated.")
                except Exception as exc:
                    st.error(f"Microphone analysis failed: {exc}")

    if rec is not None and ss.get("active_source") is None and ss.cur is None:
        ss.cur = rec
        ss.active_source = "upload"

    if ss.cur:
        show_result(ss.cur)
        st.button("Clear result", key="clear_cur", on_click=clear_cur)
    else:
        card('<div class="eyebrow">Awaiting signal</div><div class="big">Add a voice clip to begin</div><p class="mute">VoxGuard decodes the audio, draws its Mel spectrogram and asks the trained CNN for a verdict. Your report appears here.</p>' + EQ
             + '<span class="pill">WAV</span><span class="pill">MP3</span><span class="pill">Microphone</span><span class="pill">Up to 100 MB</span>')

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
    else:
        card('<div class="eyebrow">Awaiting two samples</div><div class="big">Weigh two voices side by side</div><p class="mute">Upload Sample A and Sample B to compare spectrograms, predictions and audio characteristics.</p>' + EQ)

elif page == "History":
    head("Records", "Detection history")
    h = hist_load()
    if not h:
        card('<div class="eyebrow">Nothing here yet</div><div class="big">No analyses yet</div>' + EQ)
        st.button("Go to Detect  →", key="es_hist", on_click=go_to, args=("Detect",))
    for r in h:
        lab = {"genuine": "Genuine", "spoof": "AI / Spoof", "genuine_demo": "Genuine (Mic Demo)"}.get(r.get("label"), "No prediction")
        conf = f' · {pct(max(r["genuine"], r["spoof"]))}' if r.get("genuine") is not None else ""
        with st.expander(f'{r["name"]} · {r["ts"]} · {lab}{conf}'):
            st.write(f'Status: **{r.get("status", "unknown")}** · Source {r.get("source", "upload")} · Model {r.get("model", "V1")} · Duration {r.get("duration", "?")} s')
            if r.get("genuine") is not None: st.write(f'Genuine {pct(r["genuine"])} · Spoof {pct(r["spoof"])}')
            if r.get("note"): st.caption(r.get("note", ""))
    if h and st.button("Clear history"): hist_clear(); st.rerun()
    st.caption("Stored in a local JSON file on the server. On shared hosting it may be visible to all visitors and reset on restart.")

else:
    head("About", "VoxGuard", "An AI-based voice authenticity detection system designed to help identify synthetic and cloned voice recordings.")
    steps = [("Audio input", "WAV/MP3 decoded to mono."), ("Preprocessing", "Librosa resampling and normalisation."), ("Mel spectrogram", "Time-frequency image of the voice."),
             ("CNN (PyTorch)", "Convolutional network trained by Member 2."), ("Classification", "Genuine vs spoof confidence.")]
    st.markdown('<div class="flow">' + "".join(f'<div class="card step"><div class="num">{i+1}</div><b>{t}</b><p class="mute">{d}</p></div>' for i, (t, d) in enumerate(steps)) + '</div>', unsafe_allow_html=True)
    for col, (n, r_, w) in zip(st.columns(3), [("Antony", "Member 1", "Audio Preprocessing"), ("Afan", "Member 2", "Deep Learning and Detection Model"), ("Abhishek", "Member 3", "Website Development, UI/UX and Integration")]):
        with col: card(f'<div class="avatar">{n[0]}</div><div class="eyebrow">{r_}</div><div class="big">{n}</div><p class="mute">{w}</p>')
    card(f'<div class="eyebrow">Contact</div><div class="big">Questions, feedback or collaboration?</div><p class="mute">Write to us and we will get back to you.</p><a class="cta" href="mailto:{CONTACT}">✉ {CONTACT}</a>')

footer()
