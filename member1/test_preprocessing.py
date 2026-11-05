
import numpy as np

from member1.preprocessing import (
    preprocess_audio,
    generate_mel_spectrogram
)

from member1.labels import get_label, get_label_name

# Create a sample 440 Hz audio signal
original_sr = 22050
duration = 2

time = np.linspace(
    0,
    duration,
    int(original_sr * duration),
    endpoint=False
)

audio = 0.2 * np.sin(2 * np.pi * 440 * time)
audio = audio.astype(np.float32)

# Test audio preprocessing
processed_audio = preprocess_audio(audio, original_sr)

# Test Mel spectrogram generation
mel = generate_mel_spectrogram(processed_audio)

# Test labels
assert get_label("bonafide") == 0
assert get_label("spoof") == 1
assert get_label_name(0) == "Genuine"
assert get_label_name(1) == "AI Generated"

# Verify output dimensions
assert processed_audio.shape == (64000,)
assert mel.shape == (64, 251)

print("Preprocessing test successful!")
print("Processed audio shape:", processed_audio.shape)
print("Mel spectrogram shape:", mel.shape)
print("Genuine label:", get_label("bonafide"))
print("Spoof label:", get_label("spoof"))
