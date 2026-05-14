from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, uuid
from audio_detector import analyze_audio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "DeepShield AI Backend Running"}

@app.post("/analyze/audio")
async def analyze_audio_api(file: UploadFile = File(...)):
    # Give every upload a unique name to avoid collisions
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_name)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = analyze_audio(filepath)
    finally:
        # Always clean up, even if analysis throws
        if os.path.exists(filepath):
            os.remove(filepath)

    return result