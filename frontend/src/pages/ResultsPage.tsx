import { useLocation } from "react-router-dom";
import { PredictionResult } from "../types";

export function ResultsPage() {
  const location = useLocation();
  const fallback = localStorage.getItem("last_prediction");
  const data: PredictionResult | null =
    (location.state as PredictionResult | undefined) || (fallback ? JSON.parse(fallback) : null);

  if (!data) {
    return <p className="subtle">No prediction result found. Submit an entry first.</p>;
  }

  return (
    <div className="space-y-4">
      <section className="panel p-5">
        <h2 className="mb-3 text-lg font-semibold">Prediction Results</h2>
        <div className="mb-3 grid gap-3 md:grid-cols-2">
          <div>
            <p className="text-xs uppercase tracking-[0.16em] subtle">Risk Score</p>
            <p className="text-4xl font-bold">{data.risk_score}<span className="text-base font-medium">/100</span></p>
            <div className="mt-3 progress-track">
              <div className="progress-fill" style={{ width: `${data.risk_score}%` }} />
            </div>
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.16em] subtle">Risk Level</p>
            <p className="text-3xl font-bold">{data.risk_level}</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {data.symptom_tags.map((tag) => (
                <span key={tag} className="chip">
                  {tag.replace(/_/g, " ")}
                </span>
              ))}
            </div>
          </div>
        </div>
        {data.emergency_warning && (
          <p className="mb-2 rounded-xl border border-[var(--danger)]/50 bg-[var(--danger)]/10 p-2 text-sm text-[var(--danger)]">
            {data.warning_message}
          </p>
        )}
        <p className="text-xs subtle">{data.disclaimer}</p>
      </section>

      <section className="panel p-4">
        <h3 className="mb-2 font-semibold">Top 3 Probable Conditions</h3>
        <div className="space-y-2">
          {data.predictions.map((row) => (
            <article key={row.condition} className="panel-hover rounded-xl border border-[var(--border)] bg-[var(--surface-2)] p-3">
              <p className="font-medium">{row.condition}</p>
              <p className="mb-2 text-sm subtle">Confidence: {(row.confidence * 100).toFixed(1)}%</p>
              <div className="mb-2 progress-track">
                <div className="progress-fill" style={{ width: `${Math.min(100, row.confidence * 100)}%` }} />
              </div>
              <ul className="ml-5 list-disc text-sm subtle">
                {row.recommended_next_steps.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section className="panel p-4">
        <h3 className="mb-2 font-semibold">Why this prediction?</h3>
        <div className="flex flex-wrap gap-2">
          {data.top_contributing_features.map((feature) => (
            <span key={feature} className="chip">
              {feature}
            </span>
          ))}
        </div>
      </section>
    </div>
  );
}
