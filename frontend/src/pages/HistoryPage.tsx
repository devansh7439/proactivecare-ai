import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { TrendChart } from "../components/TrendChart";
import { HealthEntry } from "../types";

export function HistoryPage() {
  const [entries, setEntries] = useState<HealthEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await api.get("/health-entries");
        setEntries(data.data);
      } catch (err: any) {
        setError(err.response?.data?.message || "Failed to load history");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const chartData = useMemo(
    () =>
      [...entries]
        .reverse()
        .map((e) => ({
          date: new Date(e.recorded_at).toLocaleDateString(),
          heart_rate: e.heart_rate || 0,
          systolic_bp: e.systolic_bp || 0,
          diastolic_bp: e.diastolic_bp || 0,
          temperature: e.temperature || 0,
          weight: e.weight || 0
        })),
    [entries]
  );

  if (loading) return <p>Loading history...</p>;
  if (error) return <p className="text-[var(--danger)]">{error}</p>;

  return (
    <div className="grid gap-4">
      <section className="panel p-5">
        <h2 className="text-xl font-semibold">Health History Trends</h2>
        <p className="mt-1 text-sm subtle">
          Monitor progression across blood pressure, heart rate, temperature, and weight over time.
        </p>
      </section>
      <TrendChart
        title="Blood Pressure Trend"
        data={chartData}
        lines={[
          { key: "systolic_bp", color: "#ef4444", name: "Systolic" },
          { key: "diastolic_bp", color: "#f97316", name: "Diastolic" }
        ]}
      />
      <TrendChart
        title="Heart Rate Trend"
        data={chartData}
        lines={[{ key: "heart_rate", color: "#0ea5e9", name: "Heart Rate" }]}
      />
      <TrendChart
        title="Temperature Trend"
        data={chartData}
        lines={[{ key: "temperature", color: "#dc2626", name: "Temperature C" }]}
      />
      <TrendChart
        title="Weight Trend"
        data={chartData}
        lines={[{ key: "weight", color: "#16a34a", name: "Weight kg" }]}
      />
    </div>
  );
}
