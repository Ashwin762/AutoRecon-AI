// Backend base URL. Override with VITE_API_URL in Vercel env vars or a local .env
const DEFAULT_API_URL = "https://autorecon-ai.onrender.com"

function normalizeApiUrl(raw) {
  let url = (raw || DEFAULT_API_URL).trim()
  // Strip any doubled/mangled scheme, e.g. "http://https://host" or "https//host"
  url = url.replace(/^(https?:?\/\/)+/i, "").replace(/^https?\/\//i, "")
  const scheme = /^(localhost|127\.0\.0\.1)(:|\/|$)/.test(url) ? "http" : "https"
  return `${scheme}://${url}`.replace(/\/+$/, "")
}

export const API_URL = normalizeApiUrl(import.meta.env.VITE_API_URL)
