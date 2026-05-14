import json
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("prediction_logger")

def log_prediction(text: str, result: dict):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input_length": len(text),
        "input_preview": text[:80],
        "label": result["label"],
        "score": result["score"],
        "latency_ms": result["latency_ms"],
    }
    logger.info(json.dumps(entry))
    return entry