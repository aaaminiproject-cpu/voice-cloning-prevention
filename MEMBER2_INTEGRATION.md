VOXGUARD — Member 2 Integration Guide
Member
Afan — Member 2: Deep Learning and Detection Model.
Branch
afan-member2
Existing model (V2)
Model version: VOXGUARD_V2_AUGMENTED
Source files:
src/model_v2.py
src/preprocessing_v2.py
src/predict_v2.py
src/prevention.py
Preserve the existing V2 checkpoint member2_model_v2_augmented.pth and V1 checkpoint src/member2_model.pth.
New model (V2.1 — separate checkpoint)
Model version: VOXGUARD_V2_1_VALIDATION_THRESHOLD
Checkpoint uploaded to this branch at:
src/member2_model_v2_1_thresholded.pth
This file is separate from V1 and V2. Do not rename, overwrite, or delete existing checkpoints.
V2.1 uses the same VoiceDetectionCNNV2 architecture and V2 preprocessing:
Sample rate: 16,000 Hz
Audio duration: 4 seconds (crop/pad)
Mel bins: 64
FFT: 1,024
Hop length: 256
Model input: [batch, 1, 64, 251]
Labels: Genuine = 0, Spoof = 1
V2.1 stores a Spoof probability threshold selected using validation data in checkpoint key spoof_threshold. This is a validation-derived operating point, not a calibrated security guarantee.
Important integration compatibility note
The current src/predict_v2.py loader can load the V2.1 state dictionary because the architecture is the same. However, its current predict_v2() function uses an argmax decision and does not apply the V2.1 spoof_threshold.
Therefore:
Loading the V2.1 checkpoint with the existing loader is structurally compatible.
Do not claim the V2.1 validation threshold is active when using the current predict_v2().
Before switching the website to V2.1, update the prediction adapter to apply the checkpoint's spoof_threshold to the Spoof softmax score.
Keep the existing website/V2 integration unchanged until the V2.1 adapter is tested.
Load V2.1 checkpoint (from repository root)
import torch
from src.model_v2 import VoiceDetectionCNNV2

checkpoint_path = "src/member2_model_v2_1_thresholded.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = torch.load(
    checkpoint_path,
    map_location=device,
    weights_only=False
)

model = VoiceDetectionCNNV2().to(device)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

spoof_threshold = float(checkpoint["spoof_threshold"])
print("Loaded:", checkpoint["model_version"])
print("Validation-selected spoof threshold:", spoof_threshold)
V2.1 inference rule
Use the existing V2 preprocessing function to create the input tensor. Then apply the stored threshold to the Spoof softmax score:
from src.preprocessing_v2 import preprocess_audio_v2

def predict_v21(audio_array, sample_rate, model, device, spoof_threshold):
    x = preprocess_audio_v2(audio_array, sample_rate).to(device)

    model.eval()
    with torch.no_grad():
        probabilities = torch.softmax(model(x), dim=1)[0]

    genuine_score = float(probabilities[0].item())
    spoof_score = float(probabilities[1].item())

    prediction = (
        "Spoof" if spoof_score >= spoof_threshold else "Genuine"
    )

    return {
        "prediction": prediction,
        "genuine_score": genuine_score * 100,
        "spoof_score": spoof_score * 100,
        "spoof_threshold": spoof_threshold,
        "model_version": "VOXGUARD_V2_1_VALIDATION_THRESHOLD",
        "note": "Softmax scores are not calibrated probabilities."
    }
This prediction decision is separate from the existing prevention engine's 40/70 demonstration risk bands. Those bands must be reviewed before V2.1 is enabled in the website. Do not combine these thresholds without testing.
Existing V2 prediction and prevention
For the existing V2 integration, the previous API remains:
from src.predict_v2 import load_v2_model, predict_v2
from src.prevention import voxguard_prevention_engine

model, device, checkpoint = load_v2_model(
    "path/to/member2_model_v2_augmented.pth"
)

result = predict_v2(audio_array, sample_rate, model, device)
decision = voxguard_prevention_engine(
    audio_array, sample_rate, model, device, source="upload"
)
Evaluation record
The previously recorded V2 augmented model test accuracy was 88% on its held-out 500-sample test subset. Its Spoof recall was 77.2%. These are results from that experiment, not V2.1 results.
V2.1 results must be taken from the completed V2.1 notebook's final test output. Do not copy V2 metrics into the V2.1 report.
Safety and limitations
A Genuine prediction is not proof of speaker identity.
Softmax scores are not calibrated probabilities.
Threshold selection trades off missed Spoof samples against false alarms on Genuine samples.
The model is a research prototype; unseen speakers, codecs, languages, devices and newer cloning systems may behave differently.
A short microphone demo does not establish continuous low-latency real-time performance.
The prevention gate only controls playback inside an application that integrates it. It cannot intercept WhatsApp, normal phone calls, or other third-party apps.
For sensitive actions, use independent speaker verification.
File preservation
Do not modify or overwrite:
V1 checkpoint src/member2_model.pth
Existing V2 checkpoint member2_model_v2_augmented.pth
Member 3's website files, including app.py and model_adapter.py
V2.1 is an additional checkpoint. Integrate it only after the adapter and end-to-end website tests pass.
