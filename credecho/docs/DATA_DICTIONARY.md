# Feature Data Dictionary — why each signal influences lending

| Feature | Meaning | Lending relevance |
|---------|---------|-------------------|
| gst_monthly_sales | Declared monthly GST sales | Proxy for true turnover |
| gst_filing_consistency | Fraction of months filed on time (0-1) | Discipline + genuineness |
| gst_growth_rate | MoM sales growth | Business trajectory |
| upi_monthly_volume | UPI value/month | Real digital cash flow |
| upi_txn_count | UPI transactions/month | Customer footfall |
| bank_balance_trend | Balance slope | Reserve buildup |
| cash_flow_stability | Volatility of net flow (0-1) | Repayment reliability |
| avg_monthly_revenue / expenses | Income & cost base | Margin & capacity |
| profit_margin | (rev-exp)/rev | Sustainability |
| invoice_payment_delay | Avg days late | Working-capital stress |
| customer_diversity / vendor_diversity | Concentration (0-1) | Dependency risk |
| employee_count | Team size | Scale & EPFO base |
| epfo_compliance | EPFO filing regularity | Formalisation |
| utility_bill_timeliness | On-time utility pay (0-1) | Payment behaviour |
| loan_history | Prior repayment track (0-1) | Credit behaviour |
| credit_utilization | Used/available credit | Leverage stress |
| debt_ratio | Debt/assets | Solvency |
| seasonality | Revenue seasonality index | Cash-flow timing |
| business_age | Years operating | Survival likelihood |
| existing_loans | Count of open loans | Debt load |
| aa_cashflow | Net AA cash flow | Verified liquidity |
| monthly_inflow / outflow | AA-verified flows | Cash cycle |
| npa_history | Prior NPA (0/1) | Strong negative signal |
| fraud_flag | Fraud indicator (0/1) | Hard reject signal |
| returned_payments | Bounced payments count | Liquidity risk |
| tax_delay | Days of tax delay | Compliance stress |
| digital_adoption_score | Digital maturity (0-1) | Data richness & modernity |
| business_category / location | Sector & geography | Sector/region risk calibration |

**Target:** `financial_health_score` (0-100) and `label` (Healthy/Moderate/Risky).

## Feature engineering notes
- StandardScaler fit on **training data only** (no leakage).
- Categorical `business_category` / `location` integer-encoded via saved maps.
- Composite score is a weighted blend validated to correlate with the latent
  "true health" that drives the synthetic generator.
