const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

if (typeof window !== "undefined") {
  // Helps debugging the "backend offline" banner — check the browser console
  console.info("[CredEcho] API base URL:", BASE);
}

let token: string | null = null;

export async function login(username: string, password: string, role = "officer") {
  try {
    const r = await fetch(`${BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, role }),
    });
    if (!r.ok) throw new Error(`Login failed: HTTP ${r.status}`);
    const data = await r.json();
    token = data.access_token;
    return data;
  } catch (e) {
    console.error(
      "[CredEcho] Cannot reach backend at",
      BASE,
      "- is uvicorn running on that port? Falling back to demo mode.",
      e
    );
    throw e;
  }
}

async function post(path: string, body: unknown) {
  const r = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`Request failed: ${path}`);
  return r.json();
}

export const healthcard = (payload: unknown) => post("/healthcard", payload);
export const predict = (payload: unknown) => post("/predict", payload);
export const whatif = (payload: unknown) => post("/whatif", payload);

// Sample MSMEs for demo / offline mode
export const SAMPLE_MSMES = [
  {
    business_name: "Sri Traders", business_category: "Retail",
    location: "Tier-2", owner: "A. Kumar",
    features: {
      gst_filing_consistency: 0.92, cash_flow_stability: 0.85, profit_margin: 0.22,
      digital_adoption_score: 0.8, epfo_compliance: 0.9, debt_ratio: 0.3,
      npa_history: 0, fraud_flag: 0, invoice_payment_delay: 10, customer_diversity: 0.7,
      credit_utilization: 0.3, gst_growth_rate: 0.15, avg_monthly_revenue: 800000,
      avg_monthly_expenses: 600000, upi_monthly_volume: 500000, business_age: 6,
      aa_cashflow: 200000, monthly_inflow: 850000, monthly_outflow: 620000,
      loan_history: 0.7, utility_bill_timeliness: 0.9, employee_count: 20,
      vendor_diversity: 0.6, seasonality: 0.4,
    },
  },
  {
    business_name: "Vel Fabrics", business_category: "Manufacturing",
    location: "Tier-3", owner: "S. Devi",
    features: {
      gst_filing_consistency: 0.55, cash_flow_stability: 0.5, profit_margin: 0.08,
      digital_adoption_score: 0.45, epfo_compliance: 0.6, debt_ratio: 0.7,
      npa_history: 0, fraud_flag: 0, invoice_payment_delay: 35, customer_diversity: 0.4,
      credit_utilization: 0.6, gst_growth_rate: 0.03, avg_monthly_revenue: 350000,
      avg_monthly_expenses: 320000, upi_monthly_volume: 120000, business_age: 3,
      aa_cashflow: 30000, monthly_inflow: 360000, monthly_outflow: 330000,
      loan_history: 0.5, utility_bill_timeliness: 0.6, employee_count: 8,
      vendor_diversity: 0.4, seasonality: 0.6,
    },
  },
  {
    business_name: "QuickMart Kiosk", business_category: "Services",
    location: "Rural", owner: "R. Singh",
    features: {
      gst_filing_consistency: 0.3, cash_flow_stability: 0.28, profit_margin: -0.05,
      digital_adoption_score: 0.25, epfo_compliance: 0.3, debt_ratio: 1.1,
      npa_history: 1, fraud_flag: 0, invoice_payment_delay: 55, customer_diversity: 0.25,
      credit_utilization: 0.85, gst_growth_rate: -0.08, avg_monthly_revenue: 120000,
      avg_monthly_expenses: 130000, upi_monthly_volume: 40000, business_age: 1.2,
      aa_cashflow: -10000, monthly_inflow: 125000, monthly_outflow: 135000,
      loan_history: 0.4, utility_bill_timeliness: 0.35, employee_count: 3,
      vendor_diversity: 0.3, seasonality: 0.5,
    },
  },
];
