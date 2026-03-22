import { useState, useRef } from "react"
import axios from "axios"

function Scanner({ setScanResults, setIsScanning, isScanning }) {
  const [domain, setDomain] = useState("")
  const [scanLog, setScanLog] = useState([])
  const [progress, setProgress] = useState(0)
  const logRef = useRef(null)

  const addLog = (msg, type = "info") => {
    const colors = {
      info: "#00ff41",
      success: "#00d4ff",
      warning: "#ffd700",
      error: "#ff0040"
    }
    setScanLog(prev => [...prev, {
      msg,
      color: colors[type],
      time: new Date().toLocaleTimeString()
    }])
    setTimeout(() => {
      if (logRef.current) {
        logRef.current.scrollTop = logRef.current.scrollHeight
      }
    }, 50)
  }

  const handleScan = async () => {
    if (!domain || isScanning) return

    setScanLog([])
    setScanResults(null)
    setIsScanning(true)
    setProgress(0)

    addLog(`[INIT] Target acquired: ${domain}`, "warning")
    addLog("[SYS] Initializing AutoRecon AI modules...", "info")

    try {
      setProgress(10)
      addLog("[MOD1] Subdomain enumeration via crt.sh...", "info")
      await new Promise(r => setTimeout(r, 500))
      setProgress(25)

      addLog("[MOD2] DNS intelligence gathering...", "info")
      await new Promise(r => setTimeout(r, 500))
      setProgress(40)

      addLog("[MOD3] Port & service reconnaissance...", "info")
      await new Promise(r => setTimeout(r, 500))
      setProgress(55)

      addLog("[MOD4] Breach database correlation...", "info")
      await new Promise(r => setTimeout(r, 500))
      setProgress(70)

      addLog("[AI] Initializing LLaMA3 threat analysis engine...", "warning")

      const response = await axios.post("https://autorecon-ai.onrender.com/api/scan/full", {
        domain: domain.trim()
      })

      setProgress(100)
      addLog(`[SUCCESS] Scan complete — ${response.data.subdomains.length} subdomains discovered`, "success")
      addLog(`[AI] Threat report generated — Risk Score: ${response.data.ai_report.risk_score}/100`, "success")
      addLog("[SYS] All modules completed successfully", "success")

      setScanResults(response.data)

    } catch (err) {
      addLog(`[ERROR] Scan failed: ${err.message}`, "error")
    } finally {
      setIsScanning(false)
    }
  }

  const getRiskColor = (score) => {
    if (score >= 70) return "#ff0040"
    if (score >= 40) return "#ffd700"
    return "#00ff41"
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "80px 20px",
      position: "relative"
    }}>
      {/* Section label */}
      <div style={{
        color: "#555",
        fontSize: "11px",
        letterSpacing: "6px",
        marginBottom: "48px"
      }}>
        ── SCAN INTERFACE ──
      </div>

      {/* Input area */}
      <div style={{
        width: "100%",
        maxWidth: "700px",
        marginBottom: "32px"
      }}>
        <div style={{
          fontSize: "11px",
          color: "#00ff41",
          letterSpacing: "3px",
          marginBottom: "12px"
        }}>
          TARGET_DOMAIN:
        </div>

        <div style={{
          display: "flex",
          gap: "0",
          border: "1px solid #00ff4166",
          background: "#050505",
          boxShadow: isScanning ? "0 0 30px #00ff4133" : "none",
          transition: "box-shadow 0.3s"
        }}>
          <span style={{
            padding: "16px 20px",
            color: "#00ff41",
            fontSize: "18px",
            borderRight: "1px solid #00ff4133"
          }}>$</span>

          <input
            type="text"
            value={domain}
            onChange={e => setDomain(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleScan()}
            placeholder="target.com"
            disabled={isScanning}
            style={{
              flex: 1,
              background: "transparent",
              border: "none",
              outline: "none",
              color: "#00ff41",
              fontFamily: "'Share Tech Mono', monospace",
              fontSize: "18px",
              padding: "16px 20px",
              letterSpacing: "2px"
            }}
          />

          <button
            onClick={handleScan}
            disabled={isScanning || !domain}
            style={{
              background: isScanning ? "#111" : "#00ff41",
              color: isScanning ? "#00ff41" : "#000",
              border: "none",
              padding: "16px 32px",
              fontFamily: "'Orbitron', monospace",
              fontSize: "12px",
              fontWeight: 700,
              letterSpacing: "3px",
              cursor: isScanning ? "not-allowed" : "pointer",
              transition: "all 0.2s"
            }}
          >
            {isScanning ? "SCANNING..." : "EXECUTE"}
          </button>
        </div>

        {/* Progress bar */}
        {isScanning && (
          <div style={{
            marginTop: "8px",
            height: "2px",
            background: "#111",
            overflow: "hidden"
          }}>
            <div style={{
              height: "100%",
              width: `${progress}%`,
              background: "linear-gradient(90deg, #00ff41, #00d4ff)",
              transition: "width 0.5s ease",
              boxShadow: "0 0 10px #00ff41"
            }} />
          </div>
        )}
      </div>

      {/* Terminal log */}
      {scanLog.length > 0 && (
        <div style={{
          width: "100%",
          maxWidth: "700px",
          background: "#050505",
          border: "1px solid #00ff4122",
          padding: "20px",
          marginBottom: "32px"
        }}>
          <div style={{
            fontSize: "10px",
            color: "#555",
            letterSpacing: "3px",
            marginBottom: "12px",
            borderBottom: "1px solid #111",
            paddingBottom: "8px"
          }}>
            TERMINAL OUTPUT
          </div>
          <div
            ref={logRef}
            style={{
              maxHeight: "200px",
              overflowY: "auto",
              fontFamily: "'Share Tech Mono', monospace",
              fontSize: "12px",
              lineHeight: "1.8"
            }}
          >
            {scanLog.map((log, i) => (
              <div key={i} style={{ color: log.color }}>
                <span style={{ color: "#333" }}>[{log.time}] </span>
                {log.msg}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Feature grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
        gap: "1px",
        width: "100%",
        maxWidth: "700px",
        background: "#00ff4111",
        border: "1px solid #00ff4122"
      }}>
        {[
          { icon: "◈", label: "SUBDOMAIN ENUM", desc: "SSL cert transparency logs" },
          { icon: "◉", label: "DNS RECON", desc: "MX, NS, IP resolution" },
          { icon: "◎", label: "PORT SCAN", desc: "Shodan InternetDB" },
          { icon: "◆", label: "AI REPORT", desc: "LLaMA3 threat analysis" }
        ].map((f, i) => (
          <div key={i} style={{
            background: "#000",
            padding: "20px",
            textAlign: "center"
          }}>
            <div style={{
              fontSize: "24px",
              color: "#00d4ff",
              marginBottom: "8px"
            }}>{f.icon}</div>
            <div style={{
              fontSize: "10px",
              color: "#00ff41",
              letterSpacing: "2px",
              marginBottom: "4px"
            }}>{f.label}</div>
            <div style={{
              fontSize: "10px",
              color: "#333"
            }}>{f.desc}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Scanner