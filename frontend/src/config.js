// Backend base URL. Override with VITE_API_URL in Vercel env vars or a local .env
export const API_URL = (import.meta.env.VITE_API_URL || "https://autorecon-ai.onrender.com").replace(/\/+$/, "")
