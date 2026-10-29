"use client";
import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  ShieldCheck, TrendingUp, Activity, Gauge, Wallet, Building2,
  ArrowUpRight, ArrowDownRight, Sparkles,
} from "lucide-react";
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
} from "recharts";
import { login, healthcard, SAMPLE_MSMES } from "@/lib/api";

type Card = any;

const bandColor = (band: string) =>
  band === "Excellent" || band === "Good" ? "#34d399"
  : band === "Average" ? "#fbbf24" : "#f87171";

function ScoreRing({ score, band }: { score: number; band: string }) {
  const r = 70, c = 2 * Math.PI * r;
  const off = c * (1 - score / 100);
  return (
    <div className="relative w-[180px] h-[180px]">
      <svg width="180" height="180" className="-rotate-90">
        <circle cx="90" cy="90" r={r} stroke="rgba(255,255,255,.08)" strokeWidth="14" fill="none" />
        <motion.circle
          cx="90" cy="90" r={r} stroke={bandColor(band)} strokeWidth="14" fill="none"
          strokeLinecap="round" strokeDasharray={c}
          initial={{ strokeDashoffset: c }} animate={{ strokeDashoffset: off }}
          transition={{ duration: 1.1, ease: "easeOut" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-bold">{score}</span>
        <span className="text-xs text-white/50">/ 100</span>
        <span className="mt-1 text-sm font-semibold" style={{ color: bandColor(band) }}>{band}</span>
      </div>
    </div>
  );
}

export default function Page() {
  const [cards, setCards] = useState<Card[]>([]);
  const [active, setActive] = useState(0);
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        await login("officer", "demo", "officer");
        const results = await Promise.all(SAMPLE_MSMES.map((m) => healthcard(m)));
        setCards(results);
      } catch {
        setOffline(true);
        setCards(SAMPLE_MSMES.map(mockScore));
      }
    })();
  }, []);

  const card = cards[active];
  const radarData = useMemo(
    () => card ? Object.entries(card.dimension_scores).map(([k, v]) => ({ dim: k, v })) : [],
    [card]
  );
  const factorData = useMemo(() => {
    if (!card) return [];
    return [...card.top_positive_factors, ...card.top_negative_factors]
      .map((f: any) => ({ name: f.factor, impact: f.impact }))
      .sort((a, b) => b.impact - a.impact);
  }, [card]);

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <header className="flex items-center justify-between mb-8">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="text-violet" size={22} />
            <h1 className="text-2xl font-bold grad-text">CredEcho</h1>
          </div>
          <p className="text-white/50 text-sm">MSME Financial Health Card · Track 03 · ULI / OCEN / AA</p>
        </div>
        <div className="text-right text-xs text-white/50">
          <p>Bank Officer Dashboard</p>
          <p className={offline ? "text-warn" : "text-good"}>
            {offline ? "Demo mode (backend offline)" : "Live · FastAPI + XGBoost"}
          </p>
        </div>
      </header>

      {/* Applicant queue */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {cards.map((c, i) => (
          <button key={i} onClick={() => setActive(i)}
            className={`glass p-4 text-left transition ${i === active ? "ring-2 ring-violet" : "hover:bg-white/[.06]"}`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Building2 size={18} className="text-aqua" />
                <span className="font-semibold">{c.business_name}</span>
              </div>
              <span className="text-lg font-bold" style={{ color: bandColor(c.band) }}>
                {c.financial_health_score}
              </span>
            </div>
            <p className="text-xs text-white/50 mt-1">{c.business_category} · {c.recommendation.decision}</p>
          </button>
        ))}
      </div>

      {card && (
        <motion.div key={active} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }} className="grid grid-cols-1 lg:grid-cols-3 gap-4">

          {/* Health card */}
          <div className="glass p-6 flex flex-col items-center">
            <h2 className="self-start text-lg font-semibold mb-1">{card.business_name}</h2>
            <p className="self-start text-xs text-white/50 mb-4">{card.owner} · {card.business_category}</p>
            <ScoreRing score={card.financial_health_score} band={card.band} />
            <div className="grid grid-cols-2 gap-3 w-full mt-6 text-sm">
              <Stat icon={<Gauge size={16} />} label="Default prob." value={`${Math.round(card.default_probability * 100)}%`} />
              <Stat icon={<ShieldCheck size={16} />} label="Class" value={card.label} />
              <Stat icon={<Wallet size={16} />} label="Suggested loan"
                value={card.recommendation.suggested_loan_amount ? `₹${(card.recommendation.suggested_loan_amount/100000).toFixed(1)}L` : "—"} />
              <Stat icon={<TrendingUp size={16} />} label="Rate"
                value={card.recommendation.suggested_interest_rate ? `${card.recommendation.suggested_interest_rate}%` : "—"} />
            </div>
          </div>

          {/* Recommendation + factors */}
          <div className="glass p-6 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-xs text-white/50">AI Recommendation</p>
                <p className="text-xl font-bold" style={{ color: bandColor(card.band) }}>
                  {card.recommendation.decision}
                </p>
              </div>
              <div className="text-right">
                <p className="text-xs text-white/50">Confidence</p>
                <p className="text-xl font-bold">{card.recommendation.confidence}%</p>
              </div>
            </div>
            <p className="text-sm text-white/70 mb-4">{card.ai_explanation}</p>
            <p className="text-xs text-white/50 mb-2">Feature contributions (SHAP-style)</p>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={factorData} layout="vertical" margin={{ left: 20, right: 20 }}>
                <XAxis type="number" hide />
                <YAxis type="category" dataKey="name" width={140}
                  tick={{ fill: "#9aa4bf", fontSize: 11 }} />
                <Tooltip contentStyle={{ background: "#111726", border: "none", borderRadius: 12 }} />
                <Bar dataKey="impact" radius={[0, 6, 6, 0]}>
                  {factorData.map((d: any, i: number) => (
                    <Cell key={i} fill={d.impact >= 0 ? "#34d399" : "#f87171"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Radar */}
          <div className="glass p-6">
            <div className="flex items-center gap-2 mb-2">
              <Activity size={18} className="text-aqua" />
              <p className="font-semibold">Score breakdown</p>
            </div>
            <ResponsiveContainer width="100%" height={260}>
              <RadarChart data={radarData} outerRadius={90}>
                <PolarGrid stroke="rgba(255,255,255,.12)" />
                <PolarAngleAxis dataKey="dim" tick={{ fill: "#9aa4bf", fontSize: 9 }} />
                <Radar dataKey="v" stroke="#7c5cff" fill="#7c5cff" fillOpacity={0.35} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          {/* Strengths / weaknesses */}
          <div className="glass p-6 lg:col-span-2 grid grid-cols-2 gap-6">
            <div>
              <p className="flex items-center gap-2 text-good font-semibold mb-3">
                <ArrowUpRight size={18} /> Strengths
              </p>
              {card.strengths.map((s: string) => (
                <p key={s} className="text-sm text-white/70 py-1 border-b border-white/5">{s}</p>
              ))}
            </div>
            <div>
              <p className="flex items-center gap-2 text-bad font-semibold mb-3">
                <ArrowDownRight size={18} /> Watch-outs
              </p>
              {card.weaknesses.map((s: string) => (
                <p key={s} className="text-sm text-white/70 py-1 border-b border-white/5">{s}</p>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      <footer className="text-center text-xs text-white/30 mt-10">
        CredEcho · alternate-data credit assessment · demo data is synthetic
      </footer>
    </div>
  );
}

function Stat({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="glass p-3">
      <div className="flex items-center gap-1 text-white/50 text-xs mb-1">{icon}{label}</div>
      <p className="font-semibold">{value}</p>
    </div>
  );
}

// Offline fallback scorer (keeps the demo alive without the backend)
function mockScore(m: any) {
  const f = m.features;
  const score = Math.round(
    22 * f.gst_filing_consistency + 18 * f.cash_flow_stability +
    12 * Math.min(Math.max(f.profit_margin + 0.5, 0), 1) + 10 * f.digital_adoption_score +
    10 * f.epfo_compliance + 8 * f.utility_bill_timeliness +
    8 * (1 - Math.min(f.debt_ratio, 1.5) / 1.5) - 12 * f.npa_history - 15 * f.fraud_flag
  );
  const s = Math.max(0, Math.min(100, score));
  const band = s >= 85 ? "Excellent" : s >= 70 ? "Good" : s >= 55 ? "Average" : s >= 40 ? "Risky" : "Very Risky";
  const label = s >= 70 ? "Healthy" : s >= 45 ? "Moderate" : "Risky";
  const dp = Math.max(0.02, Math.min(0.95, (100 - s) / 130 + f.npa_history * 0.2));
  const dec = label === "Healthy" && dp < 0.15 ? "Approve"
    : label === "Risky" ? "Reject" : "Approve with Conditions";
  return {
    ...m, label, financial_health_score: s, band, default_probability: +dp.toFixed(2),
    dimension_scores: {
      "Financial Stability": Math.round(f.cash_flow_stability * 100),
      "Cash Flow Health": Math.round(Math.min(Math.max(f.aa_cashflow / 200000, 0), 1) * 100),
      "Business Growth": Math.round(Math.min(Math.max((f.gst_growth_rate + 0.1) * 5, 0), 1) * 100),
      "Digital Activity": Math.round(f.digital_adoption_score * 100),
      "Compliance": Math.round(f.gst_filing_consistency * 100),
      "Repayment": Math.round(f.loan_history * 100),
      "Fraud Risk": Math.round((1 - f.fraud_flag) * 100),
      "Revenue": Math.round(Math.min(f.avg_monthly_revenue / 1000000, 1) * 100),
      "Liquidity": Math.round((1 - Math.min(f.credit_utilization, 1)) * 100),
      "Operations": Math.round(f.vendor_diversity * 100),
    },
    top_positive_factors: [
      { factor: "GST filing consistency", impact: +(f.gst_filing_consistency * 20).toFixed(1) },
      { factor: "Cash-flow stability", impact: +(f.cash_flow_stability * 16).toFixed(1) },
      { factor: "Digital adoption", impact: +(f.digital_adoption_score * 10).toFixed(1) },
    ],
    top_negative_factors: [
      { factor: "Debt ratio", impact: -+(f.debt_ratio * 10).toFixed(1) },
      { factor: "Invoice payment delay", impact: -+(f.invoice_payment_delay / 6).toFixed(1) },
    ],
    strengths: ["GST filing consistency", "Cash-flow stability", "Digital adoption"],
    weaknesses: ["Debt ratio", "Invoice payment delay", "Credit utilisation"],
    recommendation: {
      decision: dec, confidence: Math.round((dec === "Reject" ? dp : 1 - dp) * 100),
      suggested_loan_amount: dec === "Reject" ? null : Math.round((s / 100) * 2500000 / 50000) * 50000,
      suggested_interest_rate: dec === "Reject" ? null : +(11.5 + dp * 20).toFixed(2),
    },
    ai_explanation: `${m.business_name} scores ${s}/100 (${band}), classified ${label} with ~${Math.round(dp * 100)}% default probability.`,
  };
}
