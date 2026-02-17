import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#effcf6",
          100: "#d7f7e7",
          500: "#16a34a",
          600: "#15803d",
          700: "#166534"
        }
      }
    }
  },
  plugins: []
} satisfies Config;
