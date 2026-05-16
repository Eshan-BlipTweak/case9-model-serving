# Decisions Log — Case 9

## Assumptions I made
1. CPU inference is acceptable — HF Spaces free tier has no GPU; latency ~39ms after warm-up is demo-acceptable
2. In-memory drift window (deque) — no persistent store needed for a 2-day demo
3. DistilBERT SST-2 as the base model — already trained on sentiment, no fine-tuning needed
4. Stdout logging is sufficient for demo — production would use a log aggregator

## Trade-offs
| Choice | Alternative | Why I picked this |
|---|---|---|
| FastAPI | Flask | Auto-generates OpenAPI docs, pydantic validation, async-ready |
| DistilBERT | Larger BERT models | 40% smaller, same accuracy for sentiment, faster inference |
| HF Spaces | Render | Native ML model support, free, no sleep delay |
| Rolling deque for drift | Full stats library | Lightweight, no extra dependency for a stub |
| Stdout logging | File/DB logging | Simpler for demo; in prod, use a log aggregator |

## What I de-scoped and why
- Full retrain script — time constraint; CI workflow is wired, script uses hardcoded eval set
- Persistent log storage — stdout is sufficient for demo evaluation
- Shadow deployment — stretch goal, out of time
- Model pre-warming at startup — cold start is ~6s on first request only

## What I'd do differently with another day
- Add Prometheus /metrics endpoint and a Grafana dashboard
- Implement proper model registry (MLflow) instead of CI-based promotion
- Write a load test (Locust) to measure p95 latency under concurrency
- Pre-warm model at startup to eliminate cold start delay