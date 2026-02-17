import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { ThemeToggle } from "../components/ThemeToggle";

export function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    password: "",
    age: "",
    sex: "other"
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.post("/auth/register", {
        email: form.email,
        password: form.password,
        age: form.age ? Number(form.age) : undefined,
        sex: form.sex
      });
      navigate("/login");
    } catch (err: any) {
      setError(err.response?.data?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell flex min-h-screen items-center justify-center p-4">
      <div className="absolute right-4 top-4">
        <ThemeToggle />
      </div>
      <div className="ambient-orb one" />
      <div className="ambient-orb two" />

      <form onSubmit={onSubmit} className="panel fade-in w-full max-w-md p-7">
        <h2 className="mb-1 text-2xl font-semibold">Create Account</h2>
        <p className="mb-5 subtle">Set up your health profile to start tracking.</p>
        <input
          type="email"
          className="field mb-3"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          type="password"
          className="field mb-3"
          placeholder="Password (min 8 chars)"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          minLength={8}
          required
        />
        <div className="mb-3 grid grid-cols-2 gap-2">
          <input
            type="number"
            className="field"
            placeholder="Age"
            value={form.age}
            onChange={(e) => setForm({ ...form, age: e.target.value })}
          />
          <select
            className="field"
            value={form.sex}
            onChange={(e) => setForm({ ...form, sex: e.target.value })}
          >
            <option value="female">Female</option>
            <option value="male">Male</option>
            <option value="other">Other</option>
          </select>
        </div>
        {error && <p className="mb-3 text-sm text-[var(--danger)]">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full rounded-xl px-4 py-2.5"
        >
          {loading ? "Creating..." : "Register"}
        </button>
        <p className="mt-4 text-sm subtle">
          Already have an account?{" "}
          <Link to="/login" className="font-medium text-[var(--accent-2)] hover:underline">
            Login
          </Link>
        </p>
      </form>
    </div>
  );
}
