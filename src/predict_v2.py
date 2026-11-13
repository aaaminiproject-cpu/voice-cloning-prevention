from pathlib import Path
import torch

from src.model_v2 import VoiceDetectionCNNV2
from src.preprocessing_v2 import preprocess_audio_v2


def load_v2_model(model_path, device=None):
    """Load the trained VOXGUARD V2 model."""

    if device is None:
        device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

    checkpoint = torch.load(
        Path(model_path),
        map_location=device,
        weights_only=False
    )

    model = VoiceDetectionCNNV2().to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, device, checkpoint


def predict_v2(audio, sr, model, device):
    """Predict whether audio is Genuine or Spoof."""

    input_tensor = preprocess_audio_v2(audio, sr).to(device)

    model.eval()

    with torch.no_grad():
        logits = model(input_tensor)
        probabilities = torch.softmax(logits, dim=1)[0]

    genuine_score = float(probabilities[0].item() * 100)
    spoof_score = float(probabilities[1].item() * 100)

    prediction = (
        "Genuine"
        if genuine_score >= spoof_score
        else "Spoof"
    )

    return {
        "prediction": prediction,
        "genuine_score": genuine_score,
        "spoof_score": spoof_score,
        "model_version": "VOXGUARD_V2_AUGMENTED"
    }


def predict_file(audio_path, model, device):
    """Predict directly from an audio file."""

    import librosa

    audio, sr = librosa.load(
        str(audio_path),
        sr=None,
        mono=False
    )

    return predict_v2(audio, sr, model, device)
