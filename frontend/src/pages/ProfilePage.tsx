import { FormEvent, useEffect, useState } from "react";
import { api } from "../api/client";
import { UserProfile } from "../types";

export function ProfilePage() {
  const [form, setForm] = useState<Partial<UserProfile>>({});
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await api.get("/profile/me");
        setForm(data.data);
      } catch (err: any) {
        setError(err.response?.data?.message || "Failed to load profile");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setStatus("");
    try {
      await api.put("/profile/me", {
        age: form.age ? Number(form.age) : undefined,
        sex: form.sex,
        height: form.height ? Number(form.height) : undefined,
        weight: form.weight ? Number(form.weight) : undefined,
        known_conditions: (form.known_conditions || []).filter(Boolean),
        medications: (form.medications || []).filter(Boolean)
      });
      setStatus("Profile updated");
    } catch (err: any) {
      setError(err.response?.data?.message || "Failed to update profile");
    }
  };

  if (loading) return <p>Loading profile...</p>;

  return (
    <section className="panel p-5">
      <h2 className="mb-1 text-xl font-semibold">Profile Settings</h2>
      <p className="mb-4 text-sm subtle">
        Keep your medical profile updated for better risk scoring and recommendations.
      </p>
      <form className="grid gap-3 md:grid-cols-2" onSubmit={onSubmit}>
        <input
          disabled
          className="field"
          value={form.email || ""}
          placeholder="Email"
        />
        <input
          type="number"
          className="field"
          placeholder="Age"
          value={form.age || ""}
          onChange={(e) => setForm({ ...form, age: Number(e.target.value) })}
        />
        <select
          className="field"
          value={form.sex || "other"}
          onChange={(e) => setForm({ ...form, sex: e.target.value as UserProfile["sex"] })}
        >
          <option value="female">Female</option>
          <option value="male">Male</option>
          <option value="other">Other</option>
        </select>
        <input
          type="number"
          className="field"
          placeholder="Height (cm)"
          value={form.height || ""}
          onChange={(e) => setForm({ ...form, height: Number(e.target.value) })}
        />
        <input
          type="number"
          className="field"
          placeholder="Weight (kg)"
          value={form.weight || ""}
          onChange={(e) => setForm({ ...form, weight: Number(e.target.value) })}
        />
        <input
          className="field"
          placeholder="Known conditions (comma-separated)"
          value={(form.known_conditions || []).join(", ")}
          onChange={(e) =>
            setForm({
              ...form,
              known_conditions: e.target.value
                .split(",")
                .map((x) => x.trim())
                .filter(Boolean)
            })
          }
        />
        <input
          className="field"
          placeholder="Medications (comma-separated)"
          value={(form.medications || []).join(", ")}
          onChange={(e) =>
            setForm({
              ...form,
              medications: e.target.value
                .split(",")
                .map((x) => x.trim())
                .filter(Boolean)
            })
          }
        />
        {error && <p className="col-span-full text-[var(--danger)]">{error}</p>}
        {status && <p className="col-span-full text-[var(--accent)]">{status}</p>}
        <button type="submit" className="btn-primary col-span-full rounded-xl px-4 py-2.5">
          Save Profile
        </button>
      </form>
    </section>
  );
}
