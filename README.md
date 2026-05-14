---
title: Case9 Sentiment
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Case 9: Model Serving Lite — Sentiment API

**Live demo:** https://huggingface.co/spaces/YOUR_USERNAME/case9-sentiment
**Repo:** https://github.com/YOUR_USERNAME/case9-model-serving
**Demo video:** https://loom.com/share/XXXXX

## What this is
A production-style sentiment classification API built on DistilBERT,
serving predictions with structured logging, drift monitoring, and a
CI pipeline that gates model promotion on metric regression.

## How to run locally
1. `git clone https://github.com/YOUR_USERNAME/case9-model-serving`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`
4. Open http://localhost:8000/docs

## Example curl
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely fantastic!"}'
```

## Stack
- FastAPI — lightweight, auto-generates /docs, production-ready
- DistilBERT (HuggingFace) — 40% smaller than BERT, same accuracy for sentiment
- Docker multi-stage — builder layer separates install from runtime
- GitHub Actions — CI lints, tests, builds image, pushes to ghcr.io
- HF Spaces — free HTTPS hosting for ML demos

## What's NOT done
- GPU inference (CPU is fine for demo, p95 latency ~200ms)
- Persistent log storage (logs to stdout; production would use a sink)
- Full retrain pipeline (workflow scaffold is there, training script is stubbed)

## In production, I would also add
- Prometheus metrics endpoint + Grafana dashboard
- Log aggregation (Datadog / Loki)
- Model versioning with MLflow
- Rate limiting middleware
- Async batching for throughput