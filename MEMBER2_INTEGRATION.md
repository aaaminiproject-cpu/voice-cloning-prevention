# VOXGUARD V2 — Member 2 Integration Guide

## Member
Afan — Member 2: Deep Learning and Detection Model.

## Model
VOXGUARD_V2_AUGMENTED

## Files created
- `src/model_v2.py`
- `src/preprocessing_v2.py`
- `src/predict_v2.py`
- `src/prevention.py`

## Checkpoint
The trained checkpoint is stored separately in shared Google Drive:

`VOXGUARD_V2/member2_model_v2_augmented.pth`

Do not commit the checkpoint into GitHub.

The application deployment environment must have access to the
checkpoint file or receive it through a secure deployment process.

## Load model

```python
from src.predict_v2 import load_v2_model

model, device, checkpoint = load_v2_model(
    "/path/to/member2_model_v2_augmented.pth"
)
```

## Predict uploaded audio

```python
from src.predict_v2 import predict_v2

result = predict_v2(
    audio_array,
    sample_rate,
    model,
    device
)
```

Audio is supplied as a NumPy array and its original sample rate.

## Run prevention engine

```python
from src.prevention import voxguard_prevention_engine

decision = voxguard_prevention_engine(
    audio_array,
    sample_rate,
    model,
    device,
    source="upload"
)

print(decision)
```

## Live microphone

The website should capture microphone audio and pass the decoded
audio array and sample rate to `protect_live_audio()`.

## Initial decision thresholds

- Spoof score >= 70: BLOCK
- Spoof score >= 40 and < 70: VERIFY
- Spoof score < 40: ALLOW

These are demonstration thresholds, not calibrated production
security thresholds.

## Important scope limitation

This system can gate playback inside an application that integrates
the model. It cannot independently intercept or block external
WhatsApp calls, normal phone calls, or other third-party applications.

## Model limitations

The model is a research prototype trained on a limited dataset.
Its test accuracy was approximately 88% on the recorded held-out
test set. Results can vary on unseen speakers, codecs, languages,
recording devices and new voice-cloning systems.

Do not treat a Genuine prediction as proof of identity.
For sensitive actions, use independent speaker verification.
