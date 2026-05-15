from pathlib import Path

import cv2
import joblib
import numpy as np

MODEL_PATH = Path(__file__).with_name("video_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None


def _sample_frames(video_path, max_frames=8, size=(96, 96)):
    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise ValueError("Could not open video file.")

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    if frame_count <= 0:
        frame_indexes = set(range(max_frames))
    else:
        frame_indexes = set(
            np.linspace(0, max(frame_count - 1, 0), max_frames, dtype=int)
        )

    frames = []
    index = 0

    while len(frames) < max_frames:
        ok, frame = capture.read()
        if not ok:
            break

        if index in frame_indexes:
            frame = cv2.resize(frame, size)
            frames.append(frame)

        index += 1

    capture.release()

    if not frames:
        raise ValueError("No readable frames found in video.")

    return frames


def _stats(values):
    values = np.asarray(values, dtype=np.float32)
    return [
        float(np.mean(values)),
        float(np.std(values)),
        float(np.min(values)),
        float(np.max(values)),
    ]


def extract_video_features(video_path):
    frames = _sample_frames(video_path)

    sharpness = []
    edge_density = []
    brightness = []
    saturation = []
    color_spread = []
    frame_diffs = []
    hist_diffs = []

    previous_gray = None
    previous_hist = None

    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        edges = cv2.Canny(gray, 80, 160)

        sharpness.append(cv2.Laplacian(gray, cv2.CV_64F).var())
        edge_density.append(np.mean(edges > 0))
        brightness.append(np.mean(gray))
        saturation.append(np.mean(hsv[:, :, 1]))
        color_spread.append(np.mean(np.std(frame, axis=(0, 1))))

        hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
        cv2.normalize(hist, hist)

        if previous_gray is not None:
            frame_diffs.append(np.mean(cv2.absdiff(gray, previous_gray)))

        if previous_hist is not None:
            hist_diffs.append(cv2.compareHist(previous_hist, hist, cv2.HISTCMP_BHATTACHARYYA))

        previous_gray = gray
        previous_hist = hist

    if not frame_diffs:
        frame_diffs.append(0.0)

    if not hist_diffs:
        hist_diffs.append(0.0)

    features = np.hstack([
        _stats(sharpness),
        _stats(edge_density),
        _stats(brightness),
        _stats(saturation),
        _stats(color_spread),
        _stats(frame_diffs),
        _stats(hist_diffs),
    ])

    return np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)


def analyze_video_with_heuristics(video_path):
    features = extract_video_features(video_path)
    sharpness_std = features[1]
    frame_diff_mean = features[20]
    hist_diff_mean = features[24]

    score = 100
    evidence = []

    if sharpness_std < 55:
        score -= 25
        evidence.append("unusually stable blur patterns")

    if frame_diff_mean < 4:
        score -= 25
        evidence.append("limited frame-to-frame motion variation")

    if hist_diff_mean > 0.45:
        score -= 20
        evidence.append("unstable frame histogram shifts")

    score = max(0, min(100, int(score)))

    if score < 55:
        risk = "HIGH"
        text = "Suspicious video manipulation patterns detected: " + ", ".join(evidence) + "."
    elif score < 80:
        risk = "MEDIUM"
        text = "Some suspicious video patterns detected: " + ", ".join(evidence) + "."
    else:
        risk = "LOW"
        text = "Video appears authentic with normal frame consistency."

    return {
        "score": f"{score}%",
        "risk": risk,
        "text": text
    }


def analyze_video(video_path):
    try:
        if model is None:
            return analyze_video_with_heuristics(video_path)

        features = extract_video_features(video_path).reshape(1, -1)
        probabilities = model.predict_proba(features)[0]
        classes = list(model.classes_)
        fake_index = classes.index(1)
        fake_probability = probabilities[fake_index]
        authenticity = int((1 - fake_probability) * 100)

        if fake_probability >= 0.65:
            risk = "HIGH"
            text = (
                "Suspicious video manipulation patterns detected. "
                "Frame consistency, edge, and motion artifacts indicate possible deepfake content."
            )
        elif fake_probability >= 0.4:
            risk = "MEDIUM"
            text = (
                "Some suspicious video patterns detected. "
                "The clip has borderline frame consistency and motion signals."
            )
        else:
            risk = "LOW"
            text = "Video appears authentic with normal frame consistency."

        return {
            "score": f"{authenticity}%",
            "risk": risk,
            "text": text
        }

    except Exception as e:
        return {
            "score": "0%",
            "risk": "ERROR",
            "text": f"Video analysis failed: {e}"
        }
