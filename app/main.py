from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.model import predict
from app.logger import log_prediction
from app.drift import update, check_drift
import time

app = FastAPI(title="Sentiment API — Case 9", version="1.0.0")

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    score: float
    latency_ms: float

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": time.time()}

@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(req: PredictRequest):
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="text cannot be empty")
    result = predict(req.text)
    log_prediction(req.text, result)
    update(req.text)
    return result

@app.get("/drift")
def drift_endpoint():
    return check_drift()

@app.get("/")
def root():
    return {
        "name": "Sentiment API",
        "endpoints": ["/predict (POST)", "/drift (GET)", "/health (GET)"],
        "model": "distilbert-base-uncased-finetuned-sst-2-english",
    }