import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { ApiResponse, PredictionResult } from "../types";

type FormState = {
  symptoms_text: string;
  heart_rate: string;
  systolic_bp: string;
  diastolic_bp: string;
  temperature: string;
  spo2: string;
  glucose: string;
  weight: string;
};

const initialState: FormState = {
  symptoms_text: "",
  heart_rate: "",
  systolic_bp: "",
  diastolic_bp: "",
  temperature: "",
  spo2: "",
  glucose: "",
  weight: ""
};

const templates: Array<{ label: string; patch: Partial<FormState> }> = [
  {
    label: "Respiratory Alert",
    patch: {
      symptoms_text: "high fever, persistent cough, shortness of breath",
      temperature: "39.0",
      spo2: "91",
      heart_rate: "116"
    }
  },
  {
    label: "BP Check",
    patch: {
      symptoms_text: "headache, mild dizziness",
      systolic_bp: "145",
      diastolic_bp: "94",
      heart_rate: "98"
    }
  }
];

export function AddEntryPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<FormState>(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const payload = {
        ...Object.fromEntries(
          Object.entries(form).map(([k, v]) =>
            k === "symptoms_text" ? [k, v] : [k, v === "" ? undefined : Number(v)]
          )
        ),
        save_entry: true
      };
      const { data } = await api.post<ApiResponse<PredictionResult>>("/predict", payload);
      localStorage.setItem("last_prediction", JSON.stringify(data.data));
      navigate("/results", { state: data.data });
    } catch (err: any) {
      setError(err.response?.data?.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel p-5">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold">Add Health Entry</h2>
          <p className="text-sm subtle">Submit vitals and symptoms to generate an explainable AI result.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {templates.map((template) => (
            <button
              key={template.label}
              type="button"
              className="btn-ghost rounded-full px-3 py-1.5 text-xs"
              onClick={() => setForm((prev) => ({ ...prev, ...template.patch }))}
            >
              {template.label}
            </button>
          ))}
        </div>
      </div>

      <form className="grid gap-3 md:grid-cols-2" onSubmit={onSubmit}>
        <textarea
          className="field col-span-full min-h-28"
          placeholder="Describe your symptoms..."
          value={form.symptoms_text}
          onChange={(e) => setForm({ ...form, symptoms_text: e.target.value })}
          required
        />
        {([
          ["heart_rate", "Heart Rate"],
          ["systolic_bp", "Systolic BP"],
          ["diastolic_bp", "Diastolic BP"],
          ["temperature", "Temperature (C)"],
          ["spo2", "SpO2 (%)"],
          ["glucose", "Glucose"],
          ["weight", "Weight (kg)"]
        ] as Array<[keyof FormState, string]>).map(([key, label]) => (
          <input
            key={key}
            type="number"
            step="any"
            placeholder={label}
            className="field"
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        ))}
        {error && <p className="col-span-full text-sm text-[var(--danger)]">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="btn-primary col-span-full rounded-xl px-4 py-2.5"
        >
          {loading ? "Analyzing..." : "Analyze & Save Entry"}
        </button>
      </form>
    </section>
  );
}
