"""
CredEcho — FastAPI backend.

Serves the trained MSME Financial Health model with explainability, a loan
recommendation engine, health-card generation and a what-if simulator.

Run:  uvicorn app.main:app --reload --port 8000
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import joblib
import jwt
import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

HERE = os.path.dirname(__file__)
MODELS = os.path.join(HERE, "..", "..", "models")
SECRET = os.environ.get("CREDECHO_SECRET", "dev-secret-change-me")

app = FastAPI(title="CredEcho API", version="1.0.0",
              description="AI/ML MSME Financial Health Card — Track 03")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])

# ---- Load model artifacts ----
_model_path = os.path.join(MODELS, "model.joblib")
if not os.path.exists(_model_path):
    raise RuntimeError(
        "\n\n" + "=" * 64 +
        f"\n  Model artifacts not found at: {os.path.abspath(MODELS)}\n"
        "  You must TRAIN the model before starting the backend:\n\n"
        "      cd ml\n"
        "      pip install -r requirements.txt\n"
        "      python generate_data.py --n 50000\n"
        "      python train_model.py\n\n"
        "  This creates model.joblib, scaler.joblib and meta.json in /models.\n"
        + "=" * 64 + "\n"
    )
model = joblib.load(_model_path)
scaler = joblib.load(os.path.join(MODELS, "scaler.joblib"))
with open(os.path.join(MODELS, "meta.json")) as f:
    META = json.load(f)
FEATURES = META["features"]
CAT_COLS = META["cat_cols"]
CAT_MAPS = META["cat_maps"]
CLASSES = META["classes"]

# Human-readable labels for top factors
NICE = {
    "gst_filing_consistency": "GST filing consistency",
    "cash_flow_stability": "Cash-flow stability",
    "profit_margin": "Profit margin",
    "digital_adoption_score": "Digital adoption",
    "epfo_compliance": "EPFO compliance",
    "debt_ratio": "Debt ratio",
    "npa_history": "NPA history",
    "fraud_flag": "Fraud flag",
    "invoice_payment_delay": "Invoice payment delay",
    "customer_diversity": "Customer diversity",
    "credit_utilization": "Credit utilisation",
    "gst_growth_rate": "GST growth rate",
    "utility_bill_timeliness": "Utility bill timeliness",
    "upi_monthly_volume": "UPI monthly volume",
}


# ---------------- Auth ----------------
security = HTTPBearer(auto_error=False)


class Login(BaseModel):
    username: str
    password: str
    role: str = "officer"


def make_token(username: str, role: str) -> str:
    payload = {"sub": username, "role": role,
               "exp": datetime.utcnow() + timedelta(hours=8)}
    return jwt.encode(payload, SECRET, algorithm="HS256")


def auth(cred: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if cred is None:
        raise HTTPException(401, "Missing token")
    try:
        return jwt.decode(cred.credentials, SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")


@app.post("/login")
def login(body: Login):
    # Demo auth — any non-empty credentials succeed (swap for real user store)
    if not body.username or not body.password:
        raise HTTPException(400, "Username and password required")
    return {"access_token": make_token(body.username, body.role),
            "role": body.role, "username": body.username}


# ------------- Prediction -------------
class MSMEInput(BaseModel):
    business_name: str = "Sample MSME"
    business_category: str = "Retail"
    location: str = "Tier-2"
    owner: str = "Owner"
    features: Dict[str, float] = Field(default_factory=dict)


def _row_from_input(inp: MSMEInput) -> pd.DataFrame:
    row = {f: float(inp.features.get(f, 0.0)) for f in FEATURES}
    r = pd.DataFrame([row])
    for c in CAT_COLS:
        val = getattr(inp, c, None) or (inp.features.get(c))
        r[c] = CAT_MAPS.get(c, {}).get(val, -1)
    return r[FEATURES + CAT_COLS]


def _score_and_factors(r: pd.DataFrame):
    r_s = r.copy()
    r_s[FEATURES] = scaler.transform(r[FEATURES])
    proba = model.predict_proba(r_s)[0]
    cls_idx = int(np.argmax(proba))
    label = CLASSES[cls_idx]

    # 0-100 score = probability-weighted blend (Risky=25, Moderate=60, Healthy=90)
    anchor = {"Risky": 25, "Moderate": 62, "Healthy": 92}
    score = sum(proba[i] * anchor[CLASSES[i]] for i in range(len(CLASSES)))
    default_prob = float(proba[CLASSES.index("Risky")])

    # Factor contributions via per-feature importance x standardized deviation
    imp = META["feature_importance"]
    contribs = []
    for f in FEATURES:
        z = float(r_s[f].iloc[0])
        # features where high = good vs high = bad
        bad = f in ("debt_ratio", "npa_history", "fraud_flag",
                    "invoice_payment_delay", "credit_utilization",
                    "returned_payments", "tax_delay", "existing_loans",
                    "avg_monthly_expenses", "monthly_outflow")
        direction = -1 if bad else 1
        contribs.append((NICE.get(f, f.replace("_", " ")),
                         round(direction * z * imp.get(f, 0.0) * 100, 2)))
    contribs.sort(key=lambda x: x[1], reverse=True)
    positives = [{"factor": n, "impact": v} for n, v in contribs if v > 0][:5]
    negatives = [{"factor": n, "impact": v} for n, v in contribs if v < 0][-5:]
    return label, round(float(score), 1), round(default_prob, 3), positives, negatives, proba


DIMENSIONS = {
    "Financial Stability": ["cash_flow_stability", "bank_balance_trend"],
    "Cash Flow Health": ["aa_cashflow", "monthly_inflow", "monthly_outflow"],
    "Business Growth": ["gst_growth_rate", "business_age"],
    "Digital Activity": ["digital_adoption_score", "upi_monthly_volume"],
    "Compliance": ["gst_filing_consistency", "epfo_compliance", "utility_bill_timeliness"],
    "Repayment Capability": ["loan_history", "profit_margin"],
    "Fraud Risk": ["fraud_flag", "returned_payments"],
    "Revenue Consistency": ["avg_monthly_revenue", "seasonality"],
    "Liquidity": ["credit_utilization", "debt_ratio"],
    "Operational Stability": ["employee_count", "vendor_diversity", "customer_diversity"],
}


def _dimension_scores(inp: MSMEInput) -> Dict[str, int]:
    out = {}
    for dim, feats in DIMENSIONS.items():
        vals = []
        for f in feats:
            v = float(inp.features.get(f, 0))
            if f in ("debt_ratio", "fraud_flag", "returned_payments",
                     "monthly_outflow", "credit_utilization"):
                v = 1 - min(v, 1) if v <= 1 else max(0, 1 - v / 2)
            elif v > 1:  # normalise large monetary values
                v = min(v / 3_000_000, 1)
            vals.append(min(max(v, 0), 1))
        out[dim] = int(round(np.mean(vals) * 100)) if vals else 50
    return out


def _recommendation(label, score, default_prob):
    if label == "Healthy" and default_prob < 0.15:
        decision, conf = "Approve", int((1 - default_prob) * 100)
        rate = round(11.5 + default_prob * 20, 2)
    elif label == "Moderate" or (label == "Healthy" and default_prob < 0.35):
        decision, conf = "Approve with Conditions", int((1 - default_prob) * 100)
        rate = round(14.0 + default_prob * 20, 2)
    else:
        decision, conf = "Reject", int(default_prob * 100)
        rate = None
    loan_amount = None
    if decision != "Reject":
        base = score / 100
        loan_amount = int(round(base * 2_500_000 / 50_000) * 50_000)
    return {"decision": decision, "confidence": conf,
            "suggested_loan_amount": loan_amount, "suggested_interest_rate": rate}


@app.post("/predict")
def predict(inp: MSMEInput, user=Depends(auth)):
    r = _row_from_input(inp)
    label, score, default_prob, pos, neg, proba = _score_and_factors(r)
    dims = _dimension_scores(inp)
    band = ("Excellent" if score >= 85 else "Good" if score >= 70 else
            "Average" if score >= 55 else "Risky" if score >= 40 else "Very Risky")
    return {
        "business_name": inp.business_name,
        "business_category": inp.business_category,
        "owner": inp.owner,
        "label": label, "financial_health_score": score, "band": band,
        "default_probability": default_prob,
        "dimension_scores": dims,
        "top_positive_factors": pos, "top_negative_factors": neg,
        "class_probabilities": {CLASSES[i]: round(float(proba[i]), 3)
                                for i in range(len(CLASSES))},
        "recommendation": _recommendation(label, score, default_prob),
    }


@app.post("/healthcard")
def healthcard(inp: MSMEInput, user=Depends(auth)):
    p = predict(inp, user)
    strengths = [f["factor"] for f in p["top_positive_factors"][:3]]
    weaknesses = [f["factor"] for f in p["top_negative_factors"][:3]]
    p["strengths"] = strengths
    p["weaknesses"] = weaknesses
    p["ai_explanation"] = (
        f"{inp.business_name} scores {p['financial_health_score']}/100 "
        f"({p['band']}). The model classifies it as {p['label']} with a "
        f"{int(p['default_probability']*100)}% estimated default probability. "
        f"Strengths: {', '.join(strengths) or 'n/a'}. "
        f"Watch-outs: {', '.join(weaknesses) or 'n/a'}."
    )
    return p


class WhatIf(BaseModel):
    base: MSMEInput
    overrides: Dict[str, float]


@app.post("/whatif")
def whatif(body: WhatIf, user=Depends(auth)):
    before = predict(body.base, user)
    modified = body.base.copy(deep=True)
    modified.features = {**body.base.features, **body.overrides}
    after = predict(modified, user)
    return {"before": before, "after": after,
            "score_delta": round(after["financial_health_score"] -
                                 before["financial_health_score"], 1)}


@app.get("/health")
def health():
    return {"status": "ok", "model_metrics": META["metrics"]}


@app.get("/analytics")
def analytics(user=Depends(auth)):
    return {"feature_importance": dict(list(META["feature_importance"].items())[:12]),
            "metrics": META["metrics"], "classes": CLASSES}
