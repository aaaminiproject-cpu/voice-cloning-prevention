import numpy as np
import librosa
import torch

SAMPLE_RATE = 16000
DURATION = 4
TARGET_LENGTH = SAMPLE_RATE * DURATION
N_MELS = 64
N_FFT = 1024
HOP_LENGTH = 256

def common_audio_to_mel_v2(audio, sr):
    audio = np.asarray(audio, dtype=np.float32)

    if audio.ndim == 2:
        if audio.shape[0] <= 2:
            audio = np.mean(audio, axis=0)
        else:
            audio = np.mean(audio, axis=1)

    audio = np.squeeze(audio)

    if audio.ndim != 1 or audio.size == 0:
        raise ValueError("Invalid or empty audio.")

    if sr != SAMPLE_RATE:
        audio = librosa.resample(
            audio,
            orig_sr=sr,
            target_sr=SAMPLE_RATE
        )

    if len(audio) > TARGET_LENGTH:
        audio = audio[:TARGET_LENGTH]
    elif len(audio) < TARGET_LENGTH:
        audio = np.pad(
            audio,
            (0, TARGET_LENGTH - len(audio))
        )

    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0
    )

    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = np.clip(mel_db, -80, 0)
    mel_normalized = (mel_db + 80) / 80.0

    return mel_normalized.astype(np.float32)


def preprocess_audio_v2(audio, sr):
    mel = common_audio_to_mel_v2(audio, sr)

    return torch.tensor(
        mel,
        dtype=torch.float32
    ).unsqueeze(0).unsqueeze(0)
