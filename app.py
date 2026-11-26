"""VoxGuard - app + model code (CPU only).

Run the app:      streamlit run app.py
Train the model:  open member2_voice_detection.ipynb (it imports this file)

Requirements: streamlit>=1.40 torch librosa soundfile scipy numpy plotly
"""
import os, json, time, tempfile, hashlib
from pathlib import Path
import numpy as np, librosa
import torch
import torch.nn as nn
import torch.nn.functional as tnf
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

# ---------------------------------------------------------------------------
# MODEL + PREPROCESSING  (single source of truth)
# The training notebook (member2_voice_detection.ipynb) does `import app` and
# uses exactly these names, so training and inference can never drift apart.
# Everything here runs on CPU.
# ---------------------------------------------------------------------------
SR = 16000                 # model sample rate
DURATION = 4               # seconds per analysis window
WINDOW = SR * DURATION
MODEL_N_MELS = 64
MODEL_N_FFT = 1024
MODEL_HOP = 256
PREPROCESS_VERSION = 2     # checkpoints without this key are treated as legacy (v1)
UNSURE_BELOW = 0.65        # below this confidence the app says "Inconclusive"
CPU = torch.device("cpu")

try:
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
except Exception:
    pass


class VoiceDetectionCNN(nn.Module):
    """Same architecture as the notebook (class 0 = genuine, class 1 = spoof)."""

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))
        self.fc1 = nn.Linear(64 * 4 * 4, 128)
        self.fc2 = nn.Linear(128, 2)

    def forward(self, x):
        x = self.pool(tnf.relu(self.conv1(x)))
        x = self.pool(tnf.relu(self.conv2(x)))
        x = self.pool(tnf.relu(self.conv3(x)))
        x = self.adaptive_pool(x)
        x = torch.flatten(x, 1)
        x = tnf.relu(self.fc1(x))
        return self.fc2(x)


def to_mono_16k(y, sr):
    """Any array (mono / stereo, channels first or last) -> mono float32 at 16 kHz."""
    y = np.asarray(y, dtype=np.float32)
    if y.ndim == 2:
        y = y.mean(axis=0) if y.shape[0] <= 8 else y.mean(axis=1)
    y = np.nan_to_num(y.reshape(-1), nan=0.0, posinf=0.0, neginf=0.0)
    if int(sr) != SR:
        y = librosa.resample(y, orig_sr=int(sr), target_sr=SR)
    return y.astype(np.float32)


def clean_waveform(y):
    """Make a microphone recording look like the training data:
    remove DC offset, cut rumble below 80 Hz, trim leading/trailing silence,
    peak-normalise. Used identically in training and inference."""
    from scipy.signal import butter, sosfilt
    y = np.asarray(y, dtype=np.float32).reshape(-1)
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
    if y.size == 0:
        return y
    y = y - float(np.mean(y))
    sos = butter(4, 80, btype="highpass", fs=SR, output="sos")
    y = sosfilt(sos, y).astype(np.float32)
    trimmed, _ = librosa.effects.trim(y, top_db=35)
    if trimmed.size >= int(0.5 * SR):
        y = trimmed
    peak = float(np.max(np.abs(y))) if y.size else 0.0
    if peak > 1e-6:
        y = y / peak * 0.95
    return y.astype(np.float32)


def fit_window(y, n=WINDOW, tile=True):
    """Return exactly n samples (crop, or repeat/zero-pad when too short)."""
    y = np.asarray(y, dtype=np.float32)
    if len(y) >= n:
        return y[:n]
    if len(y) == 0:
        return np.zeros(n, dtype=np.float32)
    if tile:
        return np.tile(y, int(np.ceil(n / len(y))))[:n]
    return np.pad(y, (0, n - len(y)))


def wave_to_mel(window):
    """4-second window -> normalised log-mel (64 x 251), values in [-1, 0]."""
    mel = librosa.feature.melspectrogram(y=window, sr=SR, n_fft=MODEL_N_FFT,
                                         hop_length=MODEL_HOP, n_mels=MODEL_N_MELS)
    db = librosa.power_to_db(mel, ref=np.max)
    return (np.clip(db, -80, 0) / 80.0).astype(np.float32)


def make_windows(y, max_windows=8):
    """Up to `max_windows` 4 s windows (50% overlap) spread over the clip."""
    if len(y) <= WINDOW:
        return [fit_window(y)]
    starts = list(range(0, len(y) - WINDOW + 1, WINDOW // 2))
    if starts[-1] != len(y) - WINDOW:
        starts.append(len(y) - WINDOW)
    if len(starts) > max_windows:
        idx = np.linspace(0, len(starts) - 1, max_windows).round().astype(int)
        starts = [starts[i] for i in idx]
    return [y[s:s + WINDOW] for s in starts]


def load_detection_model(model_path):
    """Load a checkpoint written by the notebook. Always on CPU."""
    try:
        ck = torch.load(model_path, map_location="cpu", weights_only=True)
    except TypeError:                       # very old torch without weights_only
        ck = torch.load(model_path, map_location="cpu")
    state = ck.get("model_state_dict", ck) if isinstance(ck, dict) else ck
    cfg = {k: v for k, v in ck.items() if k != "model_state_dict"} if isinstance(ck, dict) else {}
    for key, expected in (("sample_rate", SR), ("n_mels", MODEL_N_MELS),
                          ("n_fft", MODEL_N_FFT), ("hop_length", MODEL_HOP), ("duration", DURATION)):
        if key in cfg and int(cfg[key]) != int(expected):
            raise ValueError(f"Checkpoint {key}={cfg[key]} does not match app.py ({expected}). "
                             "Retrain with the notebook that ships with this app.py.")
    model = VoiceDetectionCNN()
    model.load_state_dict(state)
    model.to(CPU).eval()
    cfg.setdefault("preprocess_version", 1)
    return model, cfg


def predict_waveform(y, sr, model, cfg=None, max_windows=8):
    """Probabilities for one recording. Returns genuine/spoof in 0..1."""
    cfg = cfg or {}
    y = to_mono_16k(y, sr)
    if y.size == 0:
        raise ValueError("Empty audio.")
    if int(cfg.get("preprocess_version", 1)) >= 2:
        windows = make_windows(clean_waveform(y), max_windows=max_windows)
    else:   # legacy checkpoint: first 4 s, zero padded, no cleaning
        windows = [fit_window(y, tile=False)]
    batch = torch.from_numpy(np.stack([wave_to_mel(w) for w in windows])).unsqueeze(1)
    with torch.no_grad():
        probs = torch.softmax(model(batch.to(CPU)), dim=1)
    mean = probs.mean(dim=0)
    return dict(genuine=float(mean[0]), spoof=float(mean[1]),
                window_spoof=[float(p) for p in probs[:, 1]],
                legacy=int(cfg.get("preprocess_version", 1)) < 2)


def predict_audio_file(audio_path, model, cfg=None):
    """Convenience wrapper used by the notebook's final check."""
    y, _ = librosa.load(audio_path, sr=SR, mono=True)
    out = predict_waveform(y, SR, model, cfg)
    g, s = out["genuine"], out["spoof"]
    return {"prediction": "Genuine" if g >= s else "Spoof", "confidence": max(g, s) * 100,
            "genuine_probability": g * 100, "spoof_probability": s * 100,
            "windows": len(out["window_spoof"])}


def quality_notes(y, sr):
    """Plain-language warnings about recordings that make the model unreliable."""
    notes = []
    dur = len(y) / sr
    if dur < 2.0:
        notes.append(f"Only {dur:.1f} s of audio. Results on clips under ~2 s are unreliable; record 4–10 s of continuous speech.")
    if float(np.mean(np.abs(y) >= 0.99)) > 0.005:
        notes.append("The recording is clipping (too loud). Move back from the microphone or lower the input volume.")
    frame = librosa.feature.rms(y=y, frame_length=1024, hop_length=512)[0]
    if frame.size >= 10:
        db = 20 * np.log10(frame + 1e-8)
        if float(np.percentile(db, 95) - np.percentile(db, 10)) < 12:
            notes.append("Speech barely stands out from the background (noisy room or very quiet voice). Try a quieter space, closer to the mic.")
    return notes


_MODEL = {}


def run_model(audio, sr):
    """Run the CNN (CPU) on decoded audio. Used for uploads AND microphone input."""
    bad = lambda status, message: dict(status=status, message=message, model_version="V1")
    ck = find_checkpoint()
    if not ck:
        return bad("unavailable", "member2_model.pth not found. Run the notebook to create it and put it next to app.py (or set VOXGUARD_MODEL_PATH).")
    try:
        key = (str(Path(ck).resolve()), Path(ck).stat().st_mtime)
        if key not in _MODEL:
            _MODEL.clear()
            _MODEL[key] = load_detection_model(ck)
        model, cfg = _MODEL[key]
        out = predict_waveform(audio, sr, model, cfg)
    except Exception as e:
        return bad("error", f"Detection failed ({type(e).__name__}): {e}")
    g, s = out["genuine"], out["spoof"]
    if not (0.0 <= g <= 1.0 and 0.0 <= s <= 1.0) or abs(g + s - 1.0) > 0.02:
        return bad("error", f"Unexpected scores: genuine={g:.4f}, spoof={s:.4f}")
    return dict(status="ok", genuine=g, spoof=s, label="genuine" if g >= s else "spoof",
                window_spoof=out["window_spoof"], legacy=out["legacy"], message="", model_version="V1")


# ================= AUDIO I/O + FEATURES =================
# SR (16 kHz) is defined with the model code below and is fixed.
N_MELS = 64  # mel bands for the display spectrogram
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

def fig_windows(ws, t=None):
    f = _fig(180, t)
    f.add_bar(x=[f"{i*2}-{i*2+4}s" if len(ws) > 1 else "0-4s" for i in range(len(ws))], y=[w * 100 for w in ws],
              marker_color=["#ff6b81" if w >= 0.5 else "#5ee0a0" for w in ws])
    f.update_yaxes(title="spoof %", range=[0, 100]); f.update_xaxes(title="window (approx.)"); return f


def main():
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

    def process(up, source="upload"):
        """Decode audio, compute display features and ALWAYS run the CNN (uploads and microphone alike)."""
        data = up.getvalue()
        name = getattr(up, "name", None) or ("microphone.wav" if source == "microphone" else "audio.wav")
        if not data:
            raise ValueError("No audio data was received.")

        bar = st.progress(0, "Decoding audio…")
        try:
            y, sr = load_audio(data, name)
            bar.progress(35, "Computing signal features…")
            F = features(y, sr)
            bar.progress(65, "Running detection model…")
            R = run_model(y, sr)
            R["warnings"] = quality_notes(y, sr)
            bar.progress(100, "Done")
            return dict(name=name, source=source, size=len(data), audio_bytes=data,
                        ts=now(), F=F, R=R, model_version="V1")
        finally:
            bar.empty()


    def uploader(key, label="Drop a WAV or MP3 file"):
        up = st.file_uploader(label, type=["wav", "mp3"], key=key)
        if up is None:
            return None
        file_hash = hashlib.sha256(up.getvalue()).hexdigest()
        cache_id = (key, up.name, file_hash)
        if ss.get(key + "_id") != cache_id:
            try:
                ss[key + "_rec"] = process(up, source="upload")
            except Exception as exc:
                ss[key + "_rec"] = None
                st.error(f"Audio analysis could not be completed: {exc}")
            ss[key + "_id"] = cache_id
        return ss.get(key + "_rec")


    def mic_input():
        label = "Click to record your voice"
        try:
            return st.audio_input(label, sample_rate=SR, key="voxguard_microphone")
        except TypeError:          # older Streamlit without the sample_rate argument
            return st.audio_input(label, key="voxguard_microphone")
        except AttributeError:
            st.info("Microphone recording needs Streamlit 1.40 or newer (pip install -U streamlit).")
            return None


    def status_box(R):
        if R["status"] != "ok":
            st.markdown(f'<div class="status"><b>Model integration: {R["status"]}</b><br>{R["message"]}<br><span class="mute">No prediction is shown because none was produced by the trained model.</span></div>', unsafe_allow_html=True)
            return
        for w in R.get("warnings", []):
            st.warning(w)
        if R.get("legacy"):
            st.info("This checkpoint was trained with the old preprocessing. Re-run the notebook and replace member2_model.pth for better microphone accuracy.")

    def meta(rec):
        F = rec["F"]; return f'<span class="pill">{rec["name"]}</span><span class="pill">{F["duration"]:.2f} s</span><span class="pill">{rec["size"]/1e6:.2f} MB</span><span class="pill">{F["sr"]} Hz</span>'

    def ring(p, col, label="CONFIDENCE"):
        c = 2 * 3.14159 * 54
        return (f'<svg class="ring" viewBox="0 0 140 140"><circle cx="70" cy="70" r="54" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="10"/>'
                f'<circle class="rg" cx="70" cy="70" r="54" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{c*p:.1f} {c:.1f}" transform="rotate(-90 70 70)"/>'
                f'<text class="rt" x="70" y="72" text-anchor="middle">{p*100:.0f}%</text><text class="rl" x="70" y="90" text-anchor="middle">{label}</text></svg>')

    def verdict(R):
        if R["status"] != "ok": return
        g = R["label"] == "genuine"; p = R["genuine"] if g else R["spoof"]
        unsure = p < UNSURE_BELOW
        col = "#e2b866" if unsure else ("#5ee0a0" if g else "#ff6b81")
        title = "Inconclusive: the model is unsure" if unsure else ("Genuine Human Voice" if g else "AI-Generated or Cloned Voice")
        note = ("Confidence is low. Record a longer, cleaner clip and try again." if unsure
                else "Model confidence, not a guarantee of authenticity.")
        st.markdown(f'<div class="card"><div class="eyebrow">Classification</div><div class="vrow">{ring(p, col)}<div style="flex:1;min-width:210px">'
          f'<div class="big">{title}</div>'
          f'<p class="mute" style="font-size:.85rem">{note}</p></div></div>'
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
        card(meta(rec))
        status_box(R)
        l, r = st.columns([1.15, 1])
        with l: verdict(R)
        with r:
            card('<div class="eyebrow">Signal profile</div><div class="tiles">' + tile("Duration", f'{F["duration"]:.1f} s') + tile("RMS energy", f'{F["rms"]:.3f}')
                 + tile("Centroid", f'{np.mean(F["cent"]):.0f} Hz') + tile("Rolloff", f'{np.mean(F["roll"]):.0f} Hz') + tile("Dominant", f'{F["dom"]:.0f} Hz') + tile("Nyquist", f'{F["sr"]/2:.0f} Hz') + '</div>')
            if R.get("status") == "ok":
                st.audio(F["y"], sample_rate=F["sr"])
            if rec.get("source") == "microphone" and rec.get("audio_bytes"):
                st.download_button("Download this recording", data=rec["audio_bytes"],
                                   file_name="voxguard_microphone_test.wav", mime="audio/wav",
                                   key="download_mic_test", use_container_width=True)
        ws = R.get("window_spoof") or []
        if R.get("status") == "ok" and len(ws) > 1:
            st.markdown("**Spoof probability per 4 s window**")
            plot(fig_windows(ws, T))
        c1, c2 = st.columns(2)
        with c1: st.markdown("**Waveform**"); plot(fig_wave(F, T))
        with c2: st.markdown("**Mel spectrogram**"); plot(fig_mel(F, T))
        with st.expander("Deep signal analysis"):
            st.markdown("**Spectral centroid and rolloff**"); plot(fig_spec(F, T))
            st.markdown("**MFCC (13 coefficients)**"); plot(fig_mel(F, T, "mfcc"))
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
        for col, (n, t, d) in zip(st.columns(3), [("16 kHz", "Mono analysis", "Every clip is resampled the same way before detection."), ("64", "Mel bands", "A time-frequency picture of the voice for the CNN."), ("CPU", "No GPU needed", "Long clips are scored in 4 s windows and averaged.")]):
            with col: card(f'<div class="num">{n}</div><b>{t}</b><p class="mute">{d}</p>')
        st.markdown('<div class="marq"><div class="track">' + MARQ + '</div></div>', unsafe_allow_html=True)
        for col, (ic, t, d) in zip(st.columns(3), [("🎙️", "Upload or record", "Drop a WAV or MP3, or record straight from your microphone."),
                                                   ("🧠", "CNN-powered verdicts", "Genuine and spoof confidence straight from the trained PyTorch model."),
                                                   ("🛡️", "Honest by design", "If the model is offline you get a clear status, never an invented score.")]):
            with col: card(f'<div class="ico">{ic}</div><b>{t}</b><p class="mute">{d}</p>')
        st.markdown('<div class="band"><div class="eyebrow gold">Ready when you are</div><div class="hero-t" style="font-size:clamp(2rem,5vw,3.2rem)">Is that voice <span class="gold"><i>real?</i></span></div><p class="mute">Drop in a recording and let VoxGuard read the signal.</p></div>', unsafe_allow_html=True)
        st.button("Start analysing  →", key="band_go", on_click=go_to, args=("Detect",))

    elif page == "Detect":
        head("Workspace", "Detect a voice", "Add a recording and read the full report right below. Uploads and microphone recordings go through the same model.")

        cu, cm = st.columns(2)
        with cu:
            st.markdown("**Upload a file**")
            rec = uploader("main")
            # Only a newly uploaded file becomes the active result, so reruns never
            # overwrite a microphone result.
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
            mic_audio = mic_input()
            st.caption("Tip: record 4–10 s of normal speech in a quiet room, about 20 cm from the mic.")
            if mic_audio is not None:
                if st.button("Analyze recorded voice", key="analyze_mic", use_container_width=True):
                    try:
                        with st.spinner("Analysing microphone recording…"):
                            mrec = process(mic_audio, source="microphone")
                        ss.cur = mrec
                        ss.active_source = "microphone"
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


if __name__ == "__main__":
    main()
