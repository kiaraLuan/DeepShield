from pathlib import Path

import librosa
import joblib
import numpy as np

MODEL_PATH = Path(__file__).with_name("audio_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None

# =========================
# FEATURE EXTRACTION
# =========================

def _load_audio(file_path):
    audio, sr = librosa.load(
        file_path,
        sr=16000
    )

    return audio, sr


def _clean_features(features):
    return np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)


def extract_full_features(audio, sr):
    # MFCC
    mfccs = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=20
    )

    # CHROMA
    chroma = librosa.feature.chroma_stft(
        y=audio,
        sr=sr
    )

    # SPECTRAL CONTRAST
    contrast = librosa.feature.spectral_contrast(
        y=audio,
        sr=sr
    )

    # TONNETZ
    tonnetz = librosa.feature.tonnetz(
        y=librosa.effects.harmonic(audio),
        sr=sr
    )

    # EXTRA FEATURES
    spectral_centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sr
    )

    spectral_rolloff = librosa.feature.spectral_rolloff(
        y=audio,
        sr=sr
    )

    zero_crossing = librosa.feature.zero_crossing_rate(
        audio
    )

    rms = librosa.feature.rms(
        y=audio
    )

    # FINAL FEATURE VECTOR
    features = np.hstack([

        np.mean(mfccs, axis=1),

        np.mean(chroma, axis=1),

        np.mean(contrast, axis=1),

        np.mean(tonnetz, axis=1),

        np.mean(spectral_centroid),

        np.mean(spectral_rolloff),

        np.mean(zero_crossing),

        np.mean(rms)

    ])

    return _clean_features(features)


def extract_legacy_features(audio, sr):
    mfccs = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=13
    )

    spectral_centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sr
    )

    zero_crossing = librosa.feature.zero_crossing_rate(
        audio
    )

    rms = librosa.feature.rms(
        y=audio
    )

    features = np.hstack([
        np.mean(mfccs, axis=1),
        np.mean(spectral_centroid),
        np.std(spectral_centroid),
        np.mean(zero_crossing),
        np.mean(rms)
    ])

    return _clean_features(features)


def extract_features(file_path):
    audio, sr = _load_audio(file_path)
    expected_features = getattr(model, "n_features_in_", 49) if model else 49

    if expected_features <= 17:
        features = extract_legacy_features(audio, sr)
    else:
        features = extract_full_features(audio, sr)

    if len(features) > expected_features:
        features = features[:expected_features]

    if len(features) != expected_features:
        raise ValueError(
            f"Feature mismatch: extracted {len(features)} features, "
            f"but model expects {expected_features}."
        )

    return features.reshape(1, -1)


def analyze_with_heuristics(file_path):
    audio, sr = _load_audio(file_path)

    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)
    zero_crossing = librosa.feature.zero_crossing_rate(audio)
    rms = librosa.feature.rms(y=audio)

    score = 100
    evidence = []

    if float(np.mean(zero_crossing)) < 0.035:
        score -= 28
        evidence.append("flat voice cadence")

    if float(np.std(spectral_centroid)) < 520:
        score -= 24
        evidence.append("low spectral movement")

    if float(np.std(spectral_rolloff)) < 900:
        score -= 18
        evidence.append("limited high-frequency variation")

    if float(np.std(rms)) < 0.018:
        score -= 16
        evidence.append("overly even loudness")

    score = max(0, min(100, int(score)))

    if score < 55:
        risk = "HIGH"
        text = "AI-generated voice risk detected: " + ", ".join(evidence) + "."
    elif score < 80:
        risk = "MEDIUM"
        text = "Some synthetic-voice warning signs detected: " + ", ".join(evidence) + "."
    else:
        risk = "LOW"
        text = "Audio appears authentic with natural acoustic variation."

    return {
        "score": f"{score}%",
        "risk": risk,
        "text": text
    }

# =========================
# ANALYZE AUDIO
# =========================

def analyze_audio(file_path):

    try:
        if model is None:
            return analyze_with_heuristics(file_path)

        features = extract_features(file_path)

        probabilities = model.predict_proba(features)[0]

        classes = list(model.classes_)

        fake_index = classes.index(1)

        fake_probability = probabilities[fake_index]

        authenticity = int((1 - fake_probability) * 100)

        if fake_probability >= 0.5:

            risk = "HIGH"

            text = (
                "AI-generated voice patterns detected. "
                "Spectral inconsistencies and vocoder artifacts found."
            )

        else:

            risk = "LOW"

            text = (
                "Audio appears authentic with natural acoustic characteristics."
            )

        return {
            "score": f"{authenticity}%",
            "risk": risk,
            "text": text
        }

    except Exception as e:

        return {
            "score": "0%",
            "risk": "ERROR",
            "text": f"Analysis failed: {e}"
        }
