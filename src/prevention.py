from pathlib import Path
import shutil

from src.predict_v2 import predict_v2


# Initial demonstration thresholds.
# These are not calibrated security thresholds.
BLOCK_THRESHOLD = 70.0
VERIFY_THRESHOLD = 40.0


def voxguard_prevention_engine(
    audio,
    sr,
    model,
    device,
    source="upload"
):
    """
    Analyse audio and recommend an in-app safety action.

    BLOCK  = high spoof score
    VERIFY = uncertain result
    ALLOW  = lower spoof score
    """

    result = predict_v2(audio, sr, model, device)
    spoof_score = result["spoof_score"]

    if spoof_score >= BLOCK_THRESHOLD:
        action = "BLOCK"
        status = "HIGH RISK"
        message = (
            "Suspicious AI-generated or cloned voice detected. "
            "Playback should be stopped pending verification."
        )

    elif spoof_score >= VERIFY_THRESHOLD:
        action = "VERIFY"
        status = "UNCERTAIN"
        message = (
            "Voice authenticity is uncertain. "
            "Verify the speaker before proceeding."
        )

    else:
        action = "ALLOW"
        status = "LOW RISK"
        message = (
            "No strong spoof signal detected. "
            "Playback may proceed with normal caution."
        )

    return {
        **result,
        "source": source,
        "action": action,
        "status": status,
        "message": message
    }


def quarantine_audio(audio_path, quarantine_folder=None):
    """
    Preserve a copy of suspicious audio.
    Does not delete or modify the original file.
    """

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(audio_path)

    if quarantine_folder is None:
        quarantine_folder = Path(
            "/content/voxguard_quarantine"
        )

    quarantine_folder = Path(quarantine_folder)
    quarantine_folder.mkdir(parents=True, exist_ok=True)

    destination = quarantine_folder / audio_path.name

    # Avoid overwriting an existing quarantined file.
    if destination.exists():
        destination = (
            quarantine_folder /
            f"{audio_path.stem}_copy{audio_path.suffix}"
        )

    shutil.copy2(audio_path, destination)

    return str(destination)


def protected_playback(
    audio,
    sr,
    result,
    audio_path=None,
    play_allowed=False
):
    """
    Gate playback based on the prevention decision.

    Playback is disabled by default. The calling application
    must explicitly set play_allowed=True to play an ALLOW result.
    """

    action = result["action"]

    if action == "BLOCK":
        quarantine_location = None

        if audio_path is not None:
            quarantine_location = quarantine_audio(audio_path)

        return {
            "played": False,
            "action": "BLOCK",
            "quarantine_location": quarantine_location,
            "message": "Playback blocked by VOXGUARD."
        }

    if action == "VERIFY":
        return {
            "played": False,
            "action": "VERIFY",
            "quarantine_location": None,
            "message": "Verification required before playback."
        }

    if not play_allowed:
        return {
            "played": False,
            "action": "ALLOW",
            "quarantine_location": None,
            "message": (
                "Audio passed the initial screening. "
                "The application must explicitly authorize playback."
            )
        }

    from IPython.display import Audio, display

    display(Audio(audio, rate=sr))

    return {
        "played": True,
        "action": "ALLOW",
        "quarantine_location": None,
        "message": "Audio playback authorized."
    }


def protect_live_audio(audio, sr, model, device):
    """Apply the same prevention engine to microphone audio."""

    return voxguard_prevention_engine(
        audio=audio,
        sr=sr,
        model=model,
        device=device,
        source="live_microphone"
    )
