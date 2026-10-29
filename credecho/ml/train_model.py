"""
CredEcho — ML training pipeline.

Trains an XGBoost classifier (Healthy / Moderate / Risky) plus stores the
StandardScaler and feature list. Reports accuracy, F1, precision, recall and
ROC-AUC, and saves everything under ../models for the FastAPI backend.

Run:  python train_model.py
"""
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier

from generate_data import FEATURES

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "datasets")
MODELS = os.path.join(HERE, "..", "models")
CAT_COLS = ["business_category", "location"]


def load(split):
    return pd.read_csv(os.path.join(DATA, f"{split}_data.csv"))


def prep(df, cat_maps=None, fit=False):
    df = df.copy()
    if cat_maps is None:
        cat_maps = {}
    for c in CAT_COLS:
        if fit:
            cats = sorted(df[c].unique())
            cat_maps[c] = {v: i for i, v in enumerate(cats)}
        df[c] = df[c].map(cat_maps[c]).fillna(-1).astype(int)
    cols = FEATURES + CAT_COLS
    return df[cols], cat_maps


def main():
    os.makedirs(MODELS, exist_ok=True)
    train, test = load("training"), load("testing")

    Xtr, cat_maps = prep(train, fit=True)
    Xte, _ = prep(test, cat_maps=cat_maps)

    le = LabelEncoder().fit(["Risky", "Moderate", "Healthy"])
    ytr = le.transform(train["label"])
    yte = le.transform(test["label"])

    scaler = StandardScaler().fit(Xtr[FEATURES])
    Xtr_s = Xtr.copy(); Xtr_s[FEATURES] = scaler.transform(Xtr[FEATURES])
    Xte_s = Xte.copy(); Xte_s[FEATURES] = scaler.transform(Xte[FEATURES])

    model = XGBClassifier(
        n_estimators=400, max_depth=6, learning_rate=0.08,
        subsample=0.9, colsample_bytree=0.8, objective="multi:softprob",
        num_class=3, eval_metric="mlogloss", n_jobs=-1, random_state=42,
    )
    model.fit(Xtr_s, ytr)

    pred = model.predict(Xte_s)
    proba = model.predict_proba(Xte_s)

    metrics = {
        "accuracy": round(float(accuracy_score(yte, pred)), 4),
        "f1_macro": round(float(f1_score(yte, pred, average="macro")), 4),
        "precision_macro": round(float(precision_score(yte, pred, average="macro")), 4),
        "recall_macro": round(float(recall_score(yte, pred, average="macro")), 4),
        "roc_auc_ovr_macro": round(float(roc_auc_score(yte, proba, multi_class="ovr")), 4),
        "n_train": int(len(train)), "n_test": int(len(test)),
    }

    joblib.dump(model, os.path.join(MODELS, "model.joblib"))
    joblib.dump(scaler, os.path.join(MODELS, "scaler.joblib"))
    with open(os.path.join(MODELS, "meta.json"), "w") as f:
        json.dump({
            "features": FEATURES, "cat_cols": CAT_COLS, "cat_maps": cat_maps,
            "classes": list(le.classes_),
            "feature_importance": dict(sorted(
                zip(FEATURES + CAT_COLS, [float(x) for x in model.feature_importances_]),
                key=lambda kv: kv[1], reverse=True)),
            "metrics": metrics,
        }, f, indent=2)

    print("=== Test metrics ===")
    print(json.dumps(metrics, indent=2))
    print(classification_report(yte, pred, target_names=le.classes_))


if __name__ == "__main__":
    main()
