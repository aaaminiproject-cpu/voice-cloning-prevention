
import torch
import librosa

from src.model import VoiceDetectionCNN
from src.preprocessing import preprocess_audio


def load_detection_model(model_path):
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    checkpoint = torch.load(
        model_path,
        map_location=device,
        weights_only=False
    )

    model = VoiceDetectionCNN().to(device)
    state_dict = checkpoint.get(
        "model_state_dict", checkpoint
    )

    model.load_state_dict(state_dict)
    model.eval()

    return model, device


def predict_audio_file(audio_path, model, device):
    audio, sr = librosa.load(
        audio_path,
        sr=None,
        mono=True
    )

    input_tensor = preprocess_audio(audio, sr).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    genuine_probability = probabilities[0].item()
    spoof_probability = probabilities[1].item()

    prediction = (
        "Genuine"
        if genuine_probability >= spoof_probability
        else "Spoof"
    )

    confidence = max(
        genuine_probability,
        spoof_probability
    ) * 100

    return {
        "prediction": prediction,
        "confidence": confidence,
        "genuine_probability": genuine_probability * 100,
        "spoof_probability": spoof_probability * 100
    }
