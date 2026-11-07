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
    if fn is None: return bad("unavailable", "No predict()/predict_audio() in model_adapter.py. Edit run_model() in vox_core.py to match its real interface.")
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
