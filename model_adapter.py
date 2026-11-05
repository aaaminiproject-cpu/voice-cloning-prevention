"""Single integration point between the website and Member 1 + Member 2 code.

The website only ever calls `predict(...)` and only ever reads the dict it returns.
Until a real predictor is registered, model_available is False and the UI shows
"model integration pending" - it never invents a classification.
"""
from typing import Callable, Optional

GENUINE, AI = "Genuine Human Voice", "AI-Generated / Cloned Voice"

_predictor: Optional[Callable] = None


def result(predicted_class=None, confidence=None, probabilities=None, model_available=False, message=""):
    return {"predicted_class": predicted_class, "confidence": confidence,
            "probabilities": probabilities, "model_available": model_available, "message": message}


def register_predictor(fn: Callable):
    """fn(audio_bytes: bytes, filename: str) -> dict with the keys of result()."""
    global _predictor
    _predictor = fn


def _try_load_real_model():
    """INTEGRATION POINT - edit this once Anthony's and Afan's code is merged.
    Inspect their real function names/signatures first, then wrap them, e.g.:

        from member2.predict import <their_function>
        def _wrapped(audio_bytes, filename):
            ... call Member 1 preprocessing, then Member 2 model ...
            return result(predicted_class=GENUINE or AI, confidence=0.97,
                          probabilities={GENUINE: 0.97, AI: 0.03}, model_available=True,
                          message="...")
        register_predictor(_wrapped)
    """
    return


_try_load_real_model()


def predict(audio_bytes: bytes, filename: str) -> dict:
    if _predictor is None:
        return result(message="Model integration pending: Member 1 (preprocessing) and "
                              "Member 2 (trained PyTorch model) are not connected yet. "
                              "No classification has been made.")
    try:
        out = _predictor(audio_bytes, filename)
        if out.get("predicted_class") not in (GENUINE, AI):
            raise ValueError("predicted_class must be GENUINE or AI constant from model_adapter")
        return out
    except Exception as e:
        return result(message=f"Model error: {e}")
