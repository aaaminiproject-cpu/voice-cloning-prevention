
import numpy as np
import librosa
import torch

SAMPLE_RATE = 16000
DURATION = 4
N_MELS = 64
N_FFT = 1024
HOP_LENGTH = 256


def common_audio_to_mel(audio, sr):
    audio = np.asarray(audio, dtype=np.float32)

    if audio.ndim == 2:
        if audio.shape[0] <= 8:
            audio = audio.mean(axis=0)
        else:
            audio = audio.mean(axis=1)

    audio = audio.flatten()

    if sr != SAMPLE_RATE:
        audio = librosa.resample(
            audio, orig_sr=sr, target_sr=SAMPLE_RATE
        )

    target_length = SAMPLE_RATE * DURATION
    audio = audio[:target_length]

    if len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)))

    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS
    )

    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = np.clip(mel_db, -80, 0) / 80.0

    return mel_db.astype(np.float32)


def preprocess_audio(audio, sr):
    mel = common_audio_to_mel(audio, sr)
    return torch.tensor(mel, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
