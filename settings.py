import json
import os
from pathlib import Path
from tensorflow.keras.models import load_model


BASE_DIR = Path(__file__).resolve().parent

CLASSES_PATH = BASE_DIR / "model" / "classes.json"
MODEL_PATH = BASE_DIR / "model" / "model.h5"
DATA_PATH = BASE_DIR / "data" / "data.csv"
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
SAVE_PATH = BASE_DIR / "data"
SAVE_CORRECT_PATH = SAVE_PATH / "correct"
SAVE_INCORRECT_PATH = SAVE_PATH / "incorrect"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MODEL = load_model(MODEL_PATH)

with open(CLASSES_PATH) as f:
    CLASS_NAMES = json.load(f)