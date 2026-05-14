from transformers import pipeline
import time

_model = None

def load_model():
    global _model
    if _model is None:
        _model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True,
            max_length=512,
        )
    return _model

def predict(text: str) -> dict:
    model = load_model()
    start = time.time()
    result = model(text)[0]
    latency_ms = round((time.time() - start) * 1000, 2)
    return {
        "label": result["label"],
        "score": round(result["score"], 4),
        "latency_ms": latency_ms,
    }