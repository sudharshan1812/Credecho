# CredEcho — AI/ML MSME Financial Health Card

![Track](https://img.shields.io/badge/IDBI%20Hackathon-Track%2003-7c5cff)
![ML](https://img.shields.io/badge/model-XGBoost-22d3ee)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688)
![Frontend](https://img.shields.io/badge/frontend-Next.js%2014-black)
![License](https://img.shields.io/badge/license-MIT-green)

**CredEcho** scores New-to-Credit (NTC) and New-to-Bank (NTB) MSMEs using their
**digital footprint** — GST, UPI, Account Aggregator, EPFO, bank statements,
invoices, cash flow and utility payments — instead of traditional financial
documents. It produces a **multidimensional 0–100 Financial Health Score**, an
**explainable** lending decision (Approve / Approve with Conditions / Reject),
and a downloadable **Financial Health Card**. Designed to plug into **ULI, OCEN
and the Account Aggregator** framework for near real-time credit assessment.

---

## Why it matters
Banks can't lend to thin-file MSMEs because they lack ITRs, balance sheets and
bureau history. CredEcho turns live cash-flow signals into a ranked, auditable
credit view — expanding formal credit access while keeping risk transparent.

---

## Architecture

```
Next.js (TS + Tailwind + Framer Motion + Recharts)
        │  REST + JWT
        ▼
FastAPI (Pydantic)  ──►  XGBoost model + StandardScaler + SHAP-style factors
        │                       (joblib artifacts in /models)
        ▼
PostgreSQL (SQLAlchemy)  +  Redis cache
        ▲
Integration layer: mock ULI / OCEN / AA / GST / UPI / EPFO connectors
```

## Repository structure
```
credecho/
├── ml/           generate_data.py, train_model.py, requirements.txt
├── backend/      FastAPI app, schema.sql, Dockerfile, requirements.txt
├── frontend/     Next.js 14 app (dashboard, health card, radar, SHAP chart)
├── datasets/     training/testing/validation CSVs (generated)
├── models/       model.joblib, scaler.joblib, meta.json (generated)
├── docs/         API + data dictionary + demo script
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Quick start

### 1. Train the model (creates datasets + model artifacts)
```bash
cd ml
pip install -r requirements.txt
python generate_data.py --n 50000
python train_model.py
```

### 2. Run the backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# docs at http://localhost:8000/docs
```

### 3. Run the frontend
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev            # http://localhost:3000
```

### One-command (Docker)
```bash
docker compose up --build
```

> The frontend has an **offline fallback scorer**, so the dashboard still
> demonstrates the full UX even if the backend isn't running.

## Model performance (50k synthetic MSMEs)
| Metric | Value |
|--------|-------|
| Accuracy | ~0.98 |
| Macro F1 | ~0.98 |
| ROC-AUC (OvR) | ~0.99 |
| Inference latency | < 150 ms |

## Key API endpoints
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/login` | JWT auth (officer / MSME) |
| POST | `/predict` | Score + class + dimension scores |
| POST | `/healthcard` | Full health card + AI explanation |
| POST | `/whatif` | What-if scenario simulation |
| GET  | `/analytics` | Feature importance + metrics |
| GET  | `/health` | Liveness + model metrics |

## The 10 score dimensions
Financial Stability · Cash Flow Health · Business Growth · Digital Activity ·
Compliance · Repayment Capability · Fraud Risk · Revenue Consistency ·
Liquidity · Operational Stability.

## License
MIT. Synthetic data only; replace mock connectors with certified ULI/OCEN/AA
endpoints for production.
