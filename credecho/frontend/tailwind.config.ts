import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: { extend: {
    colors: { ink:"#0a0e1a", panel:"#111726", violet:"#7c5cff", aqua:"#22d3ee",
      rose:"#fb7185", good:"#34d399", warn:"#fbbf24", bad:"#f87171" },
    fontFamily: { sans: ["Inter","system-ui","sans-serif"] },
  }},
  plugins: [],
};
export default config;
