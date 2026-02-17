import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { HealthEntry } from "../types";

export function DashboardPage() {
  const [entries, setEntries] = useState<HealthEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await api.get("/health-entries");
        setEntries(data.data);
      } catch (err: any) {
        setError(err.response?.data?.message || "Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const latest = entries[0];
  const averageRisk = useMemo(() => {
    if (!entries.length) return 0;
    const valid = entries.filter((e) => typeof e.risk_score === "number");
    if (!valid.length) return 0;
    return Math.round(valid.reduce((sum, e) => sum + (e.risk_score || 0), 0) / valid.length);
  }, [entries]);

  if (loading) return <p>Loading dashboard...</p>;
  if (error) return <p className="text-[var(--danger)]">{error}</p>;

  const riskBar = Math.max(4, Math.min(100, averageRisk || 4));

  return (
    <div className="space-y-4">
      <section className="panel p-5">
        <p className="text-xs uppercase tracking-[0.2em] subtle">Overview</p>
        <h2 className="mt-1 text-2xl font-semibold">Health Intelligence Dashboard</h2>
        <p className="mt-2 subtle">
          Track trends, monitor current risk, and quickly start a fresh diagnostic analysis.
        </p>
        <div className="mt-4">
          <p className="mb-2 text-xs subtle">Average risk trend</p>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${riskBar}%` }} />
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <article className="panel panel-hover p-4">
          <p className="text-sm subtle">Entries Logged</p>
          <p className="text-3xl font-bold">{entries.length}</p>
        </article>
        <article className="panel panel-hover p-4">
          <p className="text-sm subtle">Average Risk</p>
          <p className="text-3xl font-bold">{averageRisk}/100</p>
        </article>
        <article className="panel panel-hover p-4">
          <p className="text-sm subtle">Latest Risk Level</p>
          <p className="text-3xl font-bold">{latest?.risk_level || "N/A"}</p>
        </article>
      </section>

      <section className="panel p-4">
        <h2 className="mb-2 text-lg font-semibold">Latest Health Snapshot</h2>
        {latest ? (
          <div className="grid gap-3 text-sm md:grid-cols-2">
            <p>
              <span className="font-medium">Symptoms:</span> {latest.symptoms_text}
            </p>
            <p>
              <span className="font-medium">Heart Rate:</span> {latest.heart_rate ?? "-"} bpm
            </p>
            <p>
              <span className="font-medium">Blood Pressure:</span> {latest.systolic_bp ?? "-"} /{" "}
              {latest.diastolic_bp ?? "-"}
            </p>
            <p>
              <span className="font-medium">Temperature:</span> {latest.temperature ?? "-"} C
            </p>
            <p className="md:col-span-2">
              <span className="chip">{(latest.symptom_tags || []).join(" • ") || "no tags yet"}</span>
            </p>
          </div>
        ) : (
          <p className="subtle">No records yet. Add your first entry.</p>
        )}
        <div className="mt-4 flex flex-wrap gap-2">
          <Link to="/entry" className="btn-primary rounded-xl px-4 py-2 text-sm">
            Add Entry
          </Link>
          <Link to="/history" className="btn-secondary rounded-xl px-4 py-2 text-sm">
            View Trends
          </Link>
        </div>
      </section>
    </div>
  );
}
