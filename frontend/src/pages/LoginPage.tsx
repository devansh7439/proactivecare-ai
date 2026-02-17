import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, tokenStore } from "../api/client";
import { ThemeToggle } from "../components/ThemeToggle";
import { ApiResponse, Tokens } from "../types";

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data } = await api.post<ApiResponse<Tokens>>("/auth/login", { email, password });
      tokenStore.set(data.data.access_token, data.data.refresh_token);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.message || "Login failed");
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
        <h2 className="mb-1 text-2xl font-semibold">Welcome Back</h2>
        <p className="mb-5 subtle">Sign in to continue your proactive monitoring.</p>
        <label className="mb-2 block text-sm subtle">Email</label>
        <input
          type="email"
          className="field mb-4"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label className="mb-2 block text-sm subtle">Password</label>
        <input
          type="password"
          className="field mb-4"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
        />
        {error && <p className="mb-3 text-sm text-[var(--danger)]">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full rounded-xl px-4 py-2.5"
        >
          {loading ? "Signing in..." : "Sign In"}
        </button>
        <p className="mt-4 text-sm subtle">
          No account?{" "}
          <Link to="/register" className="font-medium text-[var(--accent-2)] hover:underline">
            Register
          </Link>
        </p>
      </form>
    </div>
  );
}
