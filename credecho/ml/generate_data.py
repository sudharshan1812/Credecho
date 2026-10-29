"""
CredEcho — Synthetic MSME dataset generator.

Generates realistic synthetic records for New-to-Credit / New-to-Bank MSMEs
using their digital footprint (GST, UPI, Account Aggregator, EPFO, utilities,
cash flow). Produces training/testing/validation CSVs and a 0-100 Financial
Health Score plus a 3-class label (Healthy / Moderate / Risky).

Run:  python generate_data.py --n 50000
"""
import argparse
import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

CATEGORIES = ["Retail", "Manufacturing", "Services", "Wholesale", "Agriculture", "Hospitality"]
LOCATIONS = ["Metro", "Tier-1", "Tier-2", "Tier-3", "Rural"]

FEATURES = [
    "gst_monthly_sales", "gst_filing_consistency", "gst_growth_rate",
    "upi_monthly_volume", "upi_txn_count", "bank_balance_trend",
    "cash_flow_stability", "avg_monthly_revenue", "avg_monthly_expenses",
    "profit_margin", "invoice_payment_delay", "customer_diversity",
    "vendor_diversity", "employee_count", "epfo_compliance",
    "utility_bill_timeliness", "loan_history", "credit_utilization",
    "debt_ratio", "seasonality", "business_age", "existing_loans",
    "aa_cashflow", "monthly_inflow", "monthly_outflow", "npa_history",
    "fraud_flag", "returned_payments", "tax_delay", "digital_adoption_score",
]


def generate(n: int) -> pd.DataFrame:
    # Latent "true health" drives correlated features (0 = weak, 1 = strong)
    health = RNG.beta(2.2, 2.2, n)

    def sig(base_low, base_high, boost, noise):
        return np.clip(
            base_low + (base_high - base_low) * (boost * health + (1 - boost) * RNG.random(n))
            + RNG.normal(0, noise, n), 0, None
        )

    df = pd.DataFrame()
    df["gst_monthly_sales"] = sig(50_000, 4_000_000, 0.7, 40_000).round(0)
    df["gst_filing_consistency"] = np.clip(0.3 + 0.7 * health + RNG.normal(0, 0.08, n), 0, 1).round(3)
    df["gst_growth_rate"] = (RNG.normal(0, 0.12, n) + 0.25 * (health - 0.5)).round(3)
    df["upi_monthly_volume"] = sig(20_000, 3_000_000, 0.65, 30_000).round(0)
    df["upi_txn_count"] = sig(20, 4000, 0.6, 40).round(0)
    df["bank_balance_trend"] = (RNG.normal(0, 0.1, n) + 0.3 * (health - 0.5)).round(3)
    df["cash_flow_stability"] = np.clip(0.2 + 0.8 * health + RNG.normal(0, 0.09, n), 0, 1).round(3)
    df["avg_monthly_revenue"] = df["gst_monthly_sales"] * RNG.uniform(0.8, 1.1, n)
    df["avg_monthly_expenses"] = df["avg_monthly_revenue"] * RNG.uniform(0.55, 0.95, n)
    df["profit_margin"] = ((df["avg_monthly_revenue"] - df["avg_monthly_expenses"])
                           / df["avg_monthly_revenue"].clip(lower=1)).round(3)
    df["invoice_payment_delay"] = np.clip(60 - 50 * health + RNG.normal(0, 8, n), 0, None).round(0)
    df["customer_diversity"] = np.clip(0.2 + 0.8 * health + RNG.normal(0, 0.1, n), 0, 1).round(3)
    df["vendor_diversity"] = np.clip(0.2 + 0.8 * health + RNG.normal(0, 0.1, n), 0, 1).round(3)
    df["employee_count"] = np.clip((2 + 60 * health + RNG.normal(0, 5, n)), 1, None).round(0)
    df["epfo_compliance"] = np.clip(0.2 + 0.8 * health + RNG.normal(0, 0.12, n), 0, 1).round(3)
    df["utility_bill_timeliness"] = np.clip(0.3 + 0.7 * health + RNG.normal(0, 0.1, n), 0, 1).round(3)
    df["loan_history"] = np.clip(0.4 + 0.6 * health + RNG.normal(0, 0.15, n), 0, 1).round(3)
    df["credit_utilization"] = np.clip(0.9 - 0.6 * health + RNG.normal(0, 0.1, n), 0, 1).round(3)
    df["debt_ratio"] = np.clip(0.8 - 0.55 * health + RNG.normal(0, 0.1, n), 0, 2).round(3)
    df["seasonality"] = RNG.uniform(0, 1, n).round(3)
    df["business_age"] = np.clip((0.5 + 12 * health + RNG.normal(0, 2, n)), 0.2, None).round(1)
    df["existing_loans"] = RNG.poisson(np.clip(2.5 - 2 * health, 0.1, None)).round(0)
    df["aa_cashflow"] = (df["avg_monthly_revenue"] - df["avg_monthly_expenses"]).round(0)
    df["monthly_inflow"] = (df["avg_monthly_revenue"] * RNG.uniform(0.9, 1.2, n)).round(0)
    df["monthly_outflow"] = (df["avg_monthly_expenses"] * RNG.uniform(0.9, 1.2, n)).round(0)
    df["npa_history"] = (RNG.random(n) > (0.35 + 0.6 * health)).astype(int)
    df["fraud_flag"] = (RNG.random(n) > (0.5 + 0.49 * health)).astype(int)
    df["returned_payments"] = np.clip(RNG.poisson(np.clip(4 - 3.5 * health, 0.1, None)), 0, None).round(0)
    df["tax_delay"] = np.clip(90 - 80 * health + RNG.normal(0, 12, n), 0, None).round(0)
    df["digital_adoption_score"] = np.clip(0.2 + 0.8 * health + RNG.normal(0, 0.1, n), 0, 1).round(3)

    # Categorical
    df["business_category"] = RNG.choice(CATEGORIES, n)
    df["location"] = RNG.choice(LOCATIONS, n, p=[0.22, 0.25, 0.28, 0.15, 0.10])

    # ----- Composite 0-100 Financial Health Score -----
    score = (
        22 * df["gst_filing_consistency"] +
        18 * df["cash_flow_stability"] +
        12 * df["profit_margin"].clip(-0.5, 0.6).add(0.5) +
        10 * df["digital_adoption_score"] +
        10 * df["epfo_compliance"] +
        8 * df["utility_bill_timeliness"] +
        8 * (1 - df["debt_ratio"].clip(0, 1.5) / 1.5) +
        6 * df["customer_diversity"] +
        6 * df["loan_history"] -
        12 * df["npa_history"] -
        15 * df["fraud_flag"] -
        0.05 * df["invoice_payment_delay"].clip(0, 90)
    )
    # Normalise to 0-100
    score = (score - score.min()) / (score.max() - score.min()) * 100
    df["financial_health_score"] = score.round(1)

    # 3-class label from score
    df["label"] = pd.cut(df["financial_health_score"],
                         bins=[-1, 45, 70, 101],
                         labels=["Risky", "Moderate", "Healthy"]).astype(str)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50_000)
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(__file__), "..", "datasets"))
    args = ap.parse_args()

    df = generate(args.n)
    os.makedirs(args.outdir, exist_ok=True)

    train = df.sample(frac=0.7, random_state=1)
    rest = df.drop(train.index)
    test = rest.sample(frac=0.67, random_state=1)
    val = rest.drop(test.index)

    train.to_csv(os.path.join(args.outdir, "training_data.csv"), index=False)
    test.to_csv(os.path.join(args.outdir, "testing_data.csv"), index=False)
    val.to_csv(os.path.join(args.outdir, "validation_data.csv"), index=False)

    print(f"Generated {len(df)} rows -> train {len(train)}, test {len(test)}, val {len(val)}")
    print(df["label"].value_counts())


if __name__ == "__main__":
    main()
