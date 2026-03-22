import { useEffect, useRef } from "react"
import RiskGauge from "./RiskGauge"
import { useScrollReveal } from "../hooks/useScrollReveal"

function Results({ results }) {
  const reportRef = useRef(null)
  useScrollReveal()

  useEffect(() => {
    if (reportRef.current) {
      reportRef.current.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }, [results])

  const { domain, subdomains, dns_info, port_scan, ai_report } = results

  return (
    <div ref={reportRef} style={{ padding: "80px 20px", maxWidth: "1100px", margin: "0 auto" }}>

      {/* Header */}
      <div className="reveal" style={{ textAlign: "center", marginBottom: "64px" }}>
        <div style={{ fontSize: "11px", color: "#555", letterSpacing: "6px", marginBottom: "16px" }}>
          ── THREAT INTELLIGENCE REPORT ──
        </div>
        <div style={{
          fontFamily: "'Orbitron', monospace",
          fontSize: "clamp(24px, 4vw, 42px)",
          fontWeight: 900,
          color: "#00d4ff",
          textShadow: "0 0 30px #00d4ff66"
        }}>{domain.toUpperCase()}</div>

        {/* Download PDF button */}
        <div style={{ marginTop: "24px" }}>
          <button
            onClick={async () => {
              const response = await fetch("https://autorecon-ai.onrender.com/api/report/pdf", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ domain })
              })
              const blob = await response.blob()
              const url = window.URL.createObjectURL(blob)
              const a = document.createElement("a")
              a.href = url
              a.download = `AutoRecon_${domain}_report.pdf`
              a.click()
            }}
            style={{
              background: "transparent",
              border: "1px solid #00d4ff",
              color: "#00d4ff",
              fontFamily: "'Orbitron', monospace",
              fontSize: "11px",
              letterSpacing: "3px",
              padding: "12px 32px",
              cursor: "pointer",
              transition: "all 0.2s"
            }}
            onMouseEnter={e => {
              e.target.style.background = "#00d4ff"
              e.target.style.color = "#000"
            }}
            onMouseLeave={e => {
              e.target.style.background = "transparent"
              e.target.style.color = "#00d4ff"
            }}
          >
            ↓ DOWNLOAD PDF REPORT
          </button>
        </div>
      </div>

      {/* Stats row */}
      <div className="reveal" style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
        gap: "1px",
        background: "#00ff4111",
        border: "1px solid #00ff4122",
        marginBottom: "2px"
      }}>
        {[
          { label: "SUBDOMAINS", value: subdomains.length, color: "#00ff41" },
          { label: "IP ADDRESSES", value: dns_info.ip_addresses.length, color: "#00d4ff" },
          { label: "OPEN PORTS", value: port_scan.total_open_ports, color: "#ffd700" },
          { label: "BREACHES", value: results.breach_results.length, color: "#ff0040" },
          { label: "VULNS", value: port_scan.vulnerabilities.length, color: "#ff0040" }
        ].map((stat, i) => (
          <div key={i} style={{ background: "#000", padding: "24px 16px", textAlign: "center" }}>
            <div style={{
              fontFamily: "'Orbitron', monospace",
              fontSize: "32px",
              fontWeight: 900,
              color: stat.color,
              textShadow: `0 0 15px ${stat.color}66`
            }}>{stat.value}</div>
            <div style={{ fontSize: "9px", color: "#555", letterSpacing: "3px", marginTop: "4px" }}>
              {stat.label}
            </div>
          </div>
        ))}
      </div>

      {/* Risk + DNS row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: "2px", marginBottom: "2px" }}>

        {/* Risk gauge */}
        <div className="reveal-left" style={{
          background: "#050505",
          border: "1px solid #00ff4122",
          padding: "32px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: "16px"
        }}>
          <div style={{ fontSize: "10px", color: "#555", letterSpacing: "4px" }}>RISK SCORE</div>
          <RiskGauge score={ai_report.risk_score} />
        </div>

        {/* DNS info */}
        <div className="reveal-right" style={{
          background: "#050505",
          border: "1px solid #00ff4122",
          padding: "32px"
        }}>
          <div style={{ fontSize: "10px", color: "#555", letterSpacing: "4px", marginBottom: "20px" }}>
            DNS INTELLIGENCE
          </div>
          <div style={{ marginBottom: "16px" }}>
            <div style={{ fontSize: "10px", color: "#00d4ff", letterSpacing: "2px", marginBottom: "8px" }}>
              IP ADDRESSES
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
              {dns_info.ip_addresses.slice(0, 6).map((ip, i) => (
                <span key={i} style={{
                  background: "#0a0a0a",
                  border: "1px solid #00ff4122",
                  padding: "4px 10px",
                  fontSize: "11px",
                  color: "#00ff41",
                  fontFamily: "'Share Tech Mono', monospace"
                }}>{ip}</span>
              ))}
            </div>
          </div>
          <div style={{ marginBottom: "16px" }}>
            <div style={{ fontSize: "10px", color: "#00d4ff", letterSpacing: "2px", marginBottom: "8px" }}>
              MAIL SERVERS
            </div>
            {dns_info.mail_servers.map((mx, i) => (
              <div key={i} style={{
                fontSize: "11px", color: "#00ff41",
                fontFamily: "'Share Tech Mono', monospace", marginBottom: "4px"
              }}>◈ {mx}</div>
            ))}
          </div>
          <div>
            <div style={{ fontSize: "10px", color: "#00d4ff", letterSpacing: "2px", marginBottom: "8px" }}>
              NAMESERVERS
            </div>
            {dns_info.nameservers.slice(0, 3).map((ns, i) => (
              <div key={i} style={{
                fontSize: "11px", color: "#555",
                fontFamily: "'Share Tech Mono', monospace", marginBottom: "4px"
              }}>◉ {ns}</div>
            ))}
          </div>
        </div>
      </div>

      {/* Subdomains */}
      <div className="reveal" style={{
        background: "#050505",
        border: "1px solid #00ff4122",
        padding: "32px",
        marginBottom: "2px"
      }}>
        <div style={{
          display: "flex", justifyContent: "space-between",
          alignItems: "center", marginBottom: "20px"
        }}>
          <div style={{ fontSize: "10px", color: "#555", letterSpacing: "4px" }}>
            SUBDOMAIN ENUMERATION
          </div>
          <div style={{ fontFamily: "'Orbitron', monospace", fontSize: "12px", color: "#00d4ff" }}>
            {subdomains.length} FOUND
          </div>
        </div>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
          gap: "4px",
          maxHeight: "300px",
          overflowY: "auto"
        }}>
          {subdomains.slice(0, 60).map((sub, i) => (
            <div key={i} style={{
              fontSize: "11px",
              color: sub.includes("dev") || sub.includes("stage") || sub.includes("test") || sub.includes("admin")
                ? "#ffd700" : "#00ff4177",
              fontFamily: "'Share Tech Mono', monospace",
              padding: "3px 0",
              borderBottom: "1px solid #0a0a0a",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap"
            }}>
              {sub.includes("dev") || sub.includes("stage") || sub.includes("test") || sub.includes("admin")
                ? "⚠ " : "◈ "}{sub}
            </div>
          ))}
        </div>
        {subdomains.length > 60 && (
          <div style={{ marginTop: "12px", fontSize: "11px", color: "#555", textAlign: "center" }}>
            ... and {subdomains.length - 60} more subdomains
          </div>
        )}
      </div>

      {/* Port scan */}
      <div className="reveal-left" style={{
        background: "#050505",
        border: "1px solid #ffd70022",
        padding: "32px",
        marginBottom: "2px"
      }}>
        <div style={{ fontSize: "10px", color: "#555", letterSpacing: "4px", marginBottom: "20px" }}>
          PORT & SERVICE RECON
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "12px" }}>
          {port_scan.exposed_services.map((service, i) => (
            <div key={i} style={{
              background: "#0a0a0a",
              border: "1px solid #ffd70022",
              padding: "16px"
            }}>
              <div style={{ fontSize: "12px", color: "#ffd700", marginBottom: "8px", fontFamily: "'Share Tech Mono'" }}>
                ◆ {service.ip}
              </div>
              <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginBottom: "8px" }}>
                {service.open_ports.map((port, j) => (
                  <span key={j} style={{
                    background: "#ffd70011",
                    border: "1px solid #ffd70033",
                    color: "#ffd700",
                    padding: "2px 8px",
                    fontSize: "11px"
                  }}>:{port}</span>
                ))}
              </div>
              <div style={{ fontSize: "10px", color: "#555" }}>
                {service.tags.join(" · ").toUpperCase()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI Report */}
      <div className="reveal" style={{
        background: "#050505",
        border: "1px solid #00d4ff33",
        padding: "32px"
      }}>
        <div style={{
          fontSize: "10px", color: "#555", letterSpacing: "4px",
          marginBottom: "24px", display: "flex", alignItems: "center", gap: "12px"
        }}>
          <span>── AI THREAT ANALYSIS</span>
          <span style={{
            background: "#00d4ff22", border: "1px solid #00d4ff44",
            color: "#00d4ff", padding: "2px 10px", fontSize: "9px", letterSpacing: "2px"
          }}>LLAMA3 · 70B</span>
        </div>
        <div style={{
          fontFamily: "'Share Tech Mono', monospace",
          fontSize: "13px", lineHeight: "1.9",
          color: "#00ff41cc"
        }}>
          {ai_report.report.split('\n').map((line, i) => {
            if (line.startsWith('##')) {
              return (
                <div key={i} style={{
                  fontFamily: "'Orbitron', monospace",
                  fontSize: "11px", color: "#00d4ff",
                  letterSpacing: "4px", margin: "24px 0 12px",
                  borderBottom: "1px solid #00d4ff22", paddingBottom: "8px"
                }}>{line.replace('##', '').trim()}</div>
              )
            }
            if (line.startsWith('*')) {
              return (
                <div key={i} style={{ color: "#00ff41", paddingLeft: "16px" }}>
                  ◈ {line.replace(/^\*+/, '').trim()}
                </div>
              )
            }
            return <div key={i}>{line}</div>
          })}
        </div>
      </div>

    </div>
  )
}

export default Results