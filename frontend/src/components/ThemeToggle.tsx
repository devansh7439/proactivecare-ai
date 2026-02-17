import { useTheme } from "../theme/ThemeProvider";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className="btn-ghost inline-flex items-center gap-2 rounded-full px-3 py-2 text-sm font-medium"
      aria-label="Toggle theme"
    >
      <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-[var(--surface-2)]">
        {theme === "light" ? "L" : "D"}
      </span>
      {theme === "light" ? "Light" : "Dark"}
    </button>
  );
}
