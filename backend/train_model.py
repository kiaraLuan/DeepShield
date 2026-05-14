import os
import librosa
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATASET_PATH = "../deepfake_audio_dataset_jay15k"

X = []
y = []

# =========================
# FEATURE EXTRACTION
# =========================

def extract_features(file_path):

    try:

        audio, sr = librosa.load(
            file_path,
            sr=16000
        )

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

        return features

    except:
        return None


# =========================
# LOAD REAL FILES
# =========================

print("Loading REAL files...")

real_path = os.path.join(DATASET_PATH, "real")

for file in os.listdir(real_path):

    if file.endswith(".wav") or file.endswith(".mp3"):

        path = os.path.join(real_path, file)

        features = extract_features(path)

        if features is not None:

            X.append(features)

            y.append(0)   # REAL


# =========================
# LOAD FAKE FILES
# =========================

print("Loading FAKE files...")

fake_path = os.path.join(DATASET_PATH, "fake")

for file in os.listdir(fake_path):

    if file.endswith(".wav") or file.endswith(".mp3"):

        path = os.path.join(fake_path, file)

        features = extract_features(path)

        if features is not None:

            X.append(features)

            y.append(1)   # FAKE


# =========================
# TRAIN MODEL
# =========================

X = np.array(X)
y = np.array(y)

print("Total samples:", len(X))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy * 100)

# =========================
# SAVE MODEL
# =========================

joblib.dump(model, "audio_model.pkl")

print("Model saved as audio_model.pkl")