# KopCoders-DeepShield-PS2

DeepShield AI is an audio deepfake detection web app that analyzes uploaded voice notes or audio clips and returns an authenticity score, risk level, and short explanation.

## Features

- **AI Audio Deepfake Detection:** Upload voice notes or audio clips and analyze whether the audio appears human or AI-generated.
- **Authenticity Score:** Displays a percentage score showing how authentic the audio appears.
- **Risk Classification:** Classifies results as LOW, MEDIUM, HIGH, or ERROR risk based on model prediction.
- **Audio Feature Extraction:** Uses signal-processing features such as MFCCs, spectral centroid, zero-crossing rate, and RMS energy.
- **Machine Learning Classification:** Uses a trained Random Forest model to classify audio as real or synthetic.
- **Secure Temporary Upload Handling:** Uploaded files are saved temporarily for analysis and deleted immediately after processing.
- **Clean Web Interface:** React frontend provides file upload, loading state, progress feedback, and result display.
- **Model-Based Analysis:** Loads a pre-trained `audio_model.pkl` file for local inference without requiring retraining.

## Tech Stack

- **Frontend:** React.js, JavaScript, CSS
- **Backend:** Python, FastAPI, Uvicorn
- **Machine Learning:** scikit-learn, RandomForestClassifier
- **Audio Processing:** librosa, NumPy
- **Model Storage:** joblib
- **API Communication:** Fetch API, multipart file upload
- **Development Tools:** Node.js, npm, Python virtual environment

## Repository Structure

```text
KopCoders-DeepShield-PS2/
├── README.md
├── docs/
├── frontend/
├── backend/
├── assets/
├── screenshots/
├── presentation/
├── demo/
└── requirements.txt
```

## Setup Instructions

### Backend

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm start
```

Open:

```text
http://localhost:3000
```
