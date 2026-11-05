"""Member 3 - signal analysis + plots. Every output is computed from the uploaded bytes."""
import hashlib, io
import numpy as np, librosa, librosa.display, soundfile as sf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 22050          # display/analysis rate (the model pipeline will use its own, e.g. 16 kHz)
MAX_SECONDS = 120   # safety cap for large files
BG, FG, CY, BL = "#0b1530", "#cbd5e1", "#22d3ee", "#3b82f6"


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_audio(data: bytes):
    """Return (y, sr, full_duration_seconds). Raises ValueError with a friendly message."""
    try:
        y, sr = librosa.load(io.BytesIO(data), sr=SR, mono=True, duration=MAX_SECONDS)
    except Exception as e:
        raise ValueError("Could not decode this file. Upload a valid WAV or MP3. "
                         f"({type(e).__name__})") from e
    if y.size < SR // 2:
        raise ValueError("Audio is shorter than 0.5 s - please upload a longer recording.")
    try:
        total = sf.info(io.BytesIO(data)).duration
    except Exception:
        total = y.size / sr
    return y, sr, float(total)


def features(y, sr, total):
    rms = librosa.feature.rms(y=y)[0]
    cen = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    return {
        "Duration (s)": round(total, 2),
        "Analysed (s)": round(y.size / sr, 2),
        "Sample rate used (Hz)": sr,
        "RMS energy (mean)": round(float(rms.mean()), 5),
        "Peak amplitude": round(float(np.abs(y).max()), 4),
        "Zero-crossing rate": round(float(librosa.feature.zero_crossing_rate(y)[0].mean()), 5),
        "Spectral centroid (Hz)": round(float(cen.mean()), 1),
        "Spectral bandwidth (Hz)": round(float(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0].mean()), 1),
        "Spectral roll-off (Hz)": round(float(librosa.feature.spectral_rolloff(y=y, sr=sr)[0].mean()), 1),
        "Silence ratio": round(float((rms < 0.1 * rms.max()).mean()), 3),
    }


def _style(ax, title):
    ax.set_facecolor(BG); ax.set_title(title, color=FG, fontsize=11, loc="left")
    ax.tick_params(colors=FG, labelsize=8)
    for s in ax.spines.values():
        s.set_color("#1e3a5f")


def _fig(h=2.6):
    fig, ax = plt.subplots(figsize=(8, h)); fig.patch.set_facecolor(BG)
    return fig, ax


def make_figures(y, sr):
    figs = {}
    fig, ax = plt.subplots(figsize=(8, 2.6)); fig.patch.set_facecolor(BG)
    step = max(1, y.size // 20000)
    ax.plot(np.arange(0, y.size, step) / sr, y[::step], color=CY, lw=0.6)
    _style(ax, "Waveform"); ax.set_xlabel("Time (s)", color=FG); ax.set_ylabel("Amplitude", color=FG)
    fig.tight_layout(); figs["Waveform"] = fig

    fig, ax = _fig(3.2)
    S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128), ref=np.max)
    img = librosa.display.specshow(S, sr=sr, x_axis="time", y_axis="mel", ax=ax, cmap="magma")
    cb = fig.colorbar(img, ax=ax, format="%+2.0f dB"); cb.ax.tick_params(colors=FG, labelsize=8)
    _style(ax, "Mel spectrogram (display version - not the model input)")
    fig.tight_layout(); figs["Mel spectrogram"] = fig

    fig, ax = _fig()
    cen = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    ax.plot(librosa.times_like(cen, sr=sr), cen, color=BL, lw=1)
    _style(ax, "Spectral centroid"); ax.set_xlabel("Time (s)", color=FG); ax.set_ylabel("Hz", color=FG)
    fig.tight_layout(); figs["Spectral centroid"] = fig

    fig, ax = _fig()
    ro = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    t = librosa.times_like(ro, sr=sr)
    ax.plot(t, ro, color=CY, lw=1, label="Roll-off"); ax.plot(t, bw, color="#a78bfa", lw=1, label="Bandwidth")
    ax.legend(facecolor=BG, labelcolor=FG, fontsize=8); _style(ax, "Roll-off and bandwidth")
    ax.set_xlabel("Time (s)", color=FG); fig.tight_layout(); figs["Roll-off / bandwidth"] = fig

    fig, ax = _fig(3.0)
    mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    librosa.display.specshow(mf, x_axis="time", ax=ax, cmap="viridis", sr=sr)
    _style(ax, "MFCCs"); fig.tight_layout(); figs["MFCCs"] = fig
    return figs


def close_figures(figs):
    for f in figs.values():
        plt.close(f)
