
import librosa
import librosa.display
import matplotlib.pyplot as plt

from src.preprocessing import (
    SAMPLE_RATE,
    N_MELS,
    N_FFT,
    HOP_LENGTH,
    common_audio_to_mel
)


def generate_mel_spectrogram(audio, sr):
    return common_audio_to_mel(audio, sr)


def display_mel_spectrogram(audio, sr):
    mel = generate_mel_spectrogram(audio, sr)

    plt.figure(figsize=(10, 4))

    librosa.display.specshow(
        mel * 80,
        sr=SAMPLE_RATE,
        hop_length=HOP_LENGTH,
        x_axis="time",
        y_axis="mel"
    )

    plt.colorbar(format="%+2.0f dB")
    plt.title("Voice Detection - Mel Spectrogram")
    plt.tight_layout()
    plt.show()

    return mel
