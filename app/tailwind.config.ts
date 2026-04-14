import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "-apple-system", "Segoe UI", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
        serif: ["Charter", "Iowan Old Style", "Palatino", "Georgia", "serif"],
      },
      colors: {
        paper: "#fafaf7",
        ink: "#1a1a1a",
        muted: "#8a8a82",
        accent: "#d97706",
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "72ch",
            lineHeight: "1.7",
          },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
