import io
from datetime import datetime
import pandas as pd


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def status_text(pred):
    return pred["predicted_class"] if pred["model_available"] else "Signal analysis only - classification pending (no model connected)"


def build_report(rec):
    p = rec["prediction"]
    lines = ["VOICEGUARD INSPECTION REPORT", "=" * 32,
             f"File: {rec['name']}", f"Size: {rec['size_kb']:.1f} KB", f"SHA-256: {rec['hash'][:16]}...",
             f"Date/time: {rec['time']}", "", "AUDIO / SIGNAL PROPERTIES"]
    lines += [f"  {k}: {v}" for k, v in rec["features"].items()]
    lines += ["", "MODEL PREDICTION"]
    if p["model_available"]:
        lines += [f"  Class: {p['predicted_class']}", f"  Confidence: {p['confidence']:.2%}"]
        lines += [f"  P({k}) = {v:.4f}" for k, v in (p["probabilities"] or {}).items()]
    else:
        lines += ["  Not available.", f"  {p['message']}"]
    lines += ["", f"FINAL INSPECTION STATUS: {status_text(p)}"]
    return "\n".join(lines)


def history_csv(history):
    rows = [{"Filename": h["name"], "Date": h["time"], "Duration (s)": h["features"]["Duration (s)"],
             "Prediction": h["prediction"]["predicted_class"] if h["prediction"]["model_available"] else "Not available",
             "Confidence": f"{h['prediction']['confidence']:.2%}" if h["prediction"]["model_available"] else ""}
            for h in history]
    buf = io.StringIO(); pd.DataFrame(rows).to_csv(buf, index=False)
    return buf.getvalue()
