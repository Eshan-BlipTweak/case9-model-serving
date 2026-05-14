"""
Retrain gate — runs in CI when new training data is pushed.
Loads the model, evaluates on held-out set, exits 1 if below threshold.
"""
import argparse
import sys
from transformers import pipeline
from sklearn.metrics import accuracy_score

# Minimal held-out eval set (hardcoded for demo — in prod, load from data/eval.csv)
EVAL_SET = [
    ("I love this product, it works perfectly!", "POSITIVE"),
    ("Absolutely wonderful experience, highly recommend.", "POSITIVE"),
    ("Great quality, fast shipping, very happy.", "POSITIVE"),
    ("This is terrible, completely broken on arrival.", "NEGATIVE"),
    ("Worst purchase I have ever made, total waste.", "NEGATIVE"),
    ("Awful quality, would not recommend to anyone.", "NEGATIVE"),
    ("Pretty good overall, minor issues but fine.", "POSITIVE"),
    ("Disappointed with the result, expected better.", "NEGATIVE"),
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.80)
    args = parser.parse_args()

    print("Loading model...")
    clf = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        truncation=True,
    )

    texts  = [x[0] for x in EVAL_SET]
    labels = [x[1] for x in EVAL_SET]

    preds = [clf(t)[0]["label"] for t in texts]
    acc   = accuracy_score(labels, preds)

    print(f"Accuracy: {acc:.3f} | Threshold: {args.threshold}")

    if acc < args.threshold:
        print("FAIL — accuracy below threshold. Blocking promotion.")
        sys.exit(1)
    else:
        print("PASS — model promoted.")
        sys.exit(0)

if __name__ == "__main__":
    main()