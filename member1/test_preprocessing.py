
import numpy as np

from member1.preprocessing import (
    preprocess_audio,
    generate_mel_spectrogram
)

from member1.labels import get_label, get_label_name


# 1. Test mono audio, resampling and padding
sr = 22050
audio = np.random.randn(sr * 2).astype(np.float32)

processed = preprocess_audio(audio, sr)
assert processed.shape == (64000,)


# 2. Test stereo audio
stereo = np.random.randn(2, 16000 * 5).astype(np.float32)

processed_stereo = preprocess_audio(stereo, 16000)
assert processed_stereo.shape == (64000,)


# 3. Test cropping audio longer than 4 seconds
long_audio = np.random.randn(16000 * 6).astype(np.float32)

cropped = preprocess_audio(long_audio, 16000)
assert cropped.shape == (64000,)


# 4. Test audio already at 16 kHz
normal_audio = np.random.randn(64000).astype(np.float32)

normal = preprocess_audio(normal_audio, 16000)
assert normal.shape == (64000,)


# 5. Test Mel spectrogram
mel = generate_mel_spectrogram(normal)

assert mel.shape == (64, 251)
assert np.all(np.isfinite(mel))
assert np.min(mel) >= -1.0
assert np.max(mel) <= 0.0


# 6. Test label mapping
assert get_label("bonafide") == 0
assert get_label("spoof") == 1
assert get_label_name(0) == "Genuine"
assert get_label_name(1) == "AI Generated"


# 7. Test invalid inputs
try:
    preprocess_audio(normal_audio, 0)
    raise AssertionError("Invalid sample rate was accepted")
except ValueError:
    pass

try:
    generate_mel_spectrogram(np.zeros(100))
    raise AssertionError("Invalid audio length was accepted")
except ValueError:
    pass

try:
    get_label("unknown")
    raise AssertionError("Unknown label was accepted")
except ValueError:
    pass


print("All Member 1 preprocessing tests passed!")
print("Processed audio shape:", processed.shape)
print("Stereo audio shape:", processed_stereo.shape)
print("Mel spectrogram shape:", mel.shape)
print("Label mapping tests passed.")
print("Invalid input tests passed.")
