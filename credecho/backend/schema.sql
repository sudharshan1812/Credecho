-- CredEcho PostgreSQL schema
CREATE TABLE users (
  id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'officer',
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE businesses (
  id SERIAL PRIMARY KEY, name TEXT NOT NULL, owner TEXT,
  category TEXT, location TEXT, business_age NUMERIC,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE gst_records (
  id SERIAL PRIMARY KEY, business_id INT REFERENCES businesses(id),
  month DATE, monthly_sales NUMERIC, filed BOOLEAN, growth_rate NUMERIC
);
CREATE TABLE upi_records (
  id SERIAL PRIMARY KEY, business_id INT REFERENCES businesses(id),
  month DATE, volume NUMERIC, txn_count INT
);
CREATE TABLE cashflow (
  id SERIAL PRIMARY KEY, business_id INT REFERENCES businesses(id),
  month DATE, inflow NUMERIC, outflow NUMERIC, aa_cashflow NUMERIC
);
CREATE TABLE scores (
  id SERIAL PRIMARY KEY, business_id INT REFERENCES businesses(id),
  financial_health_score NUMERIC, band TEXT, label TEXT,
  default_probability NUMERIC, dimension_scores JSONB, scored_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE predictions (
  id SERIAL PRIMARY KEY, business_id INT REFERENCES businesses(id),
  class_probabilities JSONB, top_positive JSONB, top_negative JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE loans (
  id SERIAL PRIMARY KEY, business_id INT REFERENCES businesses(id),
  decision TEXT, confidence INT, suggested_amount NUMERIC,
  suggested_rate NUMERIC, created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id),
  action TEXT, entity TEXT, entity_id INT, meta JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);
