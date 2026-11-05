import numpy as np
import librosa

SAMPLE_RATE = 16000
DURATION = 4
N_SAMPLES = SAMPLE_RATE * DURATION


def preprocess_audio(audio, original_sr):
    """
    Convert audio to mono, resample to 16 kHz,
    and crop or pad it to 4 seconds.
    """

    audio = np.asarray(audio, dtype=np.float32)

    
    if audio.ndim == 2:
        audio = np.mean(audio, axis=0)

    
    if original_sr != SAMPLE_RATE:
        audio = librosa.resample(
            audio,
            orig_sr=original_sr,
            target_sr=SAMPLE_RATE
        )

    
    if len(audio) > N_SAMPLES:
        audio = audio[:N_SAMPLES]

    elif len(audio) < N_SAMPLES:
        audio = np.pad(
            audio,
            (0, N_SAMPLES - len(audio))
        )

    return audio


def generate_mel_spectrogram(audio):
    """
    Generate normalized 64-band Mel spectrogram.
    Compatible with Member 2's existing configuration.
    """

    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=SAMPLE_RATE,
        n_fft=1024,
        hop_length=256,
        n_mels=64
    )

    mel_db = librosa.power_to_db(
        mel,
        ref=np.max
    )

    mel_db = np.clip(mel_db, -80, 0)

    mel_normalized = mel_db / 80.0

    return mel_normalized
