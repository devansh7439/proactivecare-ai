import { ReactNode } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { tokenStore } from "../api/client";
import { ThemeToggle } from "./ThemeToggle";

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const navigate = useNavigate();
  const logout = () => {
    tokenStore.clear();
    navigate("/login");
  };

  return (
    <div className="app-shell overflow-hidden">
      <div className="ambient-orb one" />
      <div className="ambient-orb two" />

      <header className="sticky top-0 z-20 border-b border-[var(--border)] bg-[color:var(--surface)]/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
          <div>
            <h1 className="bg-gradient-to-r from-[var(--accent)] to-[var(--accent-2)] bg-clip-text text-xl font-semibold text-transparent">
              ProactiveCare AI
            </h1>
            <p className="text-xs subtle">Smart Health Monitoring Portal</p>
          </div>

          <nav className="flex flex-wrap items-center gap-2 text-sm">
            {[
              ["/dashboard", "Dashboard"],
              ["/entry", "Add Entry"],
              ["/history", "History"],
              ["/profile", "Profile"]
            ].map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `rounded-full px-3 py-1.5 ${isActive ? "bg-[var(--surface-2)] text-[var(--text)] border border-[var(--border)]" : "text-[var(--muted)] hover:text-[var(--text)]"}`
                }
              >
                {label}
              </NavLink>
            ))}
            <ThemeToggle />
            <button onClick={logout} className="btn-secondary rounded-full px-3 py-1.5">
              Logout
            </button>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl p-4 pb-10">
        <div className="fade-in">{children}</div>
      </main>
    </div>
  );
}
