# CredEcho API Reference

Base URL: `http://localhost:8000`  ·  Auth: Bearer JWT (from `/login`)

## POST /login
Request: `{ "username": "officer", "password": "demo", "role": "officer" }`
Response: `{ "access_token": "...", "role": "officer", "username": "officer" }`

## POST /predict  (auth)
Request:
```json
{
  "business_name": "Sri Traders", "business_category": "Retail",
  "location": "Tier-2", "owner": "A. Kumar",
  "features": { "gst_filing_consistency": 0.92, "cash_flow_stability": 0.85, ... }
}
```
Response: financial_health_score, band, label, default_probability,
dimension_scores, top_positive_factors, top_negative_factors,
class_probabilities, recommendation.

## POST /healthcard  (auth)
Same input as /predict; adds strengths, weaknesses, ai_explanation.

## POST /whatif  (auth)
Request: `{ "base": <MSMEInput>, "overrides": { "gst_filing_consistency": 0.99 } }`
Response: `{ before, after, score_delta }`

## GET /analytics  (auth)
Feature importance (top 12) + model metrics.

## GET /health
Liveness + model metrics (no auth).
