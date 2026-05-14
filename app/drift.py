import statistics
from collections import deque

# Rolling window of last 200 requests
_window = deque(maxlen=200)
BASELINE_AVG_LEN = 85.0   # rough expected avg text length
BASELINE_VOCAB   = 0.72   # expected unique-word ratio

def update(text: str):
    words = text.lower().split()
    unique_ratio = len(set(words)) / max(len(words), 1)
    _window.append({"length": len(text), "unique_ratio": unique_ratio})

def check_drift() -> dict:
    if len(_window) < 50:
        return {"status": "insufficient_data", "n": len(_window)}

    lengths = [r["length"] for r in _window]
    ratios  = [r["unique_ratio"] for r in _window]

    avg_len  = statistics.mean(lengths)
    avg_voc  = statistics.mean(ratios)

    len_drift = abs(avg_len - BASELINE_AVG_LEN) / BASELINE_AVG_LEN
    voc_drift = abs(avg_voc - BASELINE_VOCAB)   / BASELINE_VOCAB

    drifting = len_drift > 0.3 or voc_drift > 0.3

    return {
        "status": "DRIFT_DETECTED" if drifting else "ok",
        "n": len(_window),
        "avg_input_length": round(avg_len, 1),
        "avg_unique_ratio": round(avg_voc, 3),
        "length_drift_pct": round(len_drift * 100, 1),
        "vocab_drift_pct":  round(voc_drift * 100, 1),
    }