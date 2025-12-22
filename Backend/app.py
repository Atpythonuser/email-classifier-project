# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import re
import uvicorn

MODEL_PATH = "email_classifier.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

app = FastAPI(title="Email Classifier API")

class PredictRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Your backend program is running"}

URL_REGEX = re.compile(r"https?://[^\s]+", re.IGNORECASE)
CAD_EXTS = (".step", ".stp", ".iges", ".igs", ".stl", ".prt", ".sldprt", ".dwg", ".dxf", ".pdf")

def extract_urls(text: str):
    urls = URL_REGEX.findall(text)
    file_refs = re.findall(r"\b[\w\-\/\\:.]+\.(?:step|stp|iges|igs|stl|prt|sldprt|dwg|dxf|pdf)\b",
                           text, flags=re.IGNORECASE)
    return list(dict.fromkeys(urls + file_refs))

@app.post("/predict")
def predict(req: PredictRequest):
    text = req.text or ""
    X = vectorizer.transform([text])
    predicted_label = model.predict(X)[0]
    cad_urls = extract_urls(text)

    return {
        "labels": predicted_label,
        "cad_urls": cad_urls
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
