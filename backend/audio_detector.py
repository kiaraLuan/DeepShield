import librosa
import numpy as np

def analyze_audio(path):

    y, sr = librosa.load(path)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

    zero_crossing = librosa.feature.zero_crossing_rate(y)

    score = 100

    anomalies = []

    if np.mean(zero_crossing) < 0.02:
        score -= 20
        anomalies.append(
            "Synthetic voice cadence patterns"
        )

    if np.std(spectral_centroid) < 500:
        score -= 15
        anomalies.append(
            "Low spectral variation detected"
        )

    if score > 80:
        risk = "LOW"

    elif score > 50:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    return {
        "score": f"{score}%",
        "risk": risk,
        "text": (
            ", ".join(anomalies)
            if anomalies
            else "Audio appears authentic."
        )
    }