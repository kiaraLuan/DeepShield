import random
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from video_detector import extract_video_features

DATASET_PATH = Path("..") / "archive (1)" / "FaceForensics++_C23"
REAL_FOLDERS = ["original"]
FAKE_FOLDERS = [
    "DeepFakeDetection",
    "Deepfakes",
    "Face2Face",
    "FaceShifter",
    "FaceSwap",
    "NeuralTextures",
]
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
MAX_REAL = 24
MAX_FAKE_PER_FOLDER = 6


def collect_videos(folder):
    videos = []
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS:
            videos.append(path)
    return videos


def load_class(folder_names, label, max_per_folder):
    rows = []
    labels = []

    for folder_name in folder_names:
        folder = DATASET_PATH / folder_name
        videos = collect_videos(folder)
        random.shuffle(videos)

        for path in videos[:max_per_folder]:
            try:
                rows.append(extract_video_features(path))
                labels.append(label)
                print(f"loaded {label}: {path.name}")
            except Exception as exc:
                print(f"skip {path}: {exc}")

    return rows, labels


def main():
    random.seed(42)

    real_rows, real_labels = load_class(REAL_FOLDERS, 0, MAX_REAL)
    fake_rows, fake_labels = load_class(FAKE_FOLDERS, 1, MAX_FAKE_PER_FOLDER)

    X = np.asarray(real_rows + fake_rows)
    y = np.asarray(real_labels + fake_labels)

    if len(X) == 0:
        raise RuntimeError(f"No videos found in {DATASET_PATH}")

    print("Total samples:", len(X))
    print("Feature count:", X.shape[1])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=220,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("Accuracy:", round(accuracy * 100, 2))
    joblib.dump(model, "video_model.pkl")
    print("Model saved as video_model.pkl")


if __name__ == "__main__":
    main()
