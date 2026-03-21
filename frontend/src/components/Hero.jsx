import { useEffect, useState } from "react"
import MatrixRain from "./MatrixRain"

function Hero() {
  const [text, setText] = useState("")
  const [showCursor, setShowCursor] = useState(true)
  const fullText = "AUTONOMOUS ATTACK SURFACE INTELLIGENCE"

  useEffect(() => {
    let i = 0
    const typing = setInterval(() => {
      if (i < fullText.length) {
        setText(fullText.slice(0, i + 1))
        i++
      } else {
        clearInterval(typing)
      }
    }, 60)
    return () => clearInterval(typing)
  }, [])

  useEffect(() => {
    const blink = setInterval(() => {
      setShowCursor(prev => !prev)
    }, 500)
    return () => clearInterval(blink)
  }, [])

  return (
    <div style={{
      position: "relative",
      height: "100vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      overflow: "hidden",
      borderBottom: "1px solid #00ff4133"
    }}>
      <MatrixRain />

      {/* Grid overlay */}
      <div style={{
        position: "absolute",
        inset: 0,
        backgroundImage: `
          linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px)
        `,
        backgroundSize: "50px 50px",
        zIndex: 1
      }} />

      {/* Content */}
      <div style={{ position: "relative", zIndex: 2, textAlign: "center", padding: "0 20px" }}>

        {/* Top label */}
        <div style={{
          color: "#00d4ff",
          fontSize: "11px",
          letterSpacing: "6px",
          marginBottom: "24px",
          fontFamily: "'Share Tech Mono', monospace"
        }}>
          [ SYSTEM INITIALIZED ] ── v1.0.0 ── CLEARANCE: LEVEL 5
        </div>

        {/* Main title */}
        <div style={{
          fontFamily: "'Orbitron', monospace",
          fontSize: "clamp(40px, 8vw, 90px)",
          fontWeight: 900,
          color: "#00ff41",
          lineHeight: 1,
          marginBottom: "8px",
          animation: "flicker 8s infinite",
          textShadow: "0 0 30px #00ff41, 0 0 60px #00ff4166"
        }}>
          AUTO
        </div>
        <div style={{
          fontFamily: "'Orbitron', monospace",
          fontSize: "clamp(40px, 8vw, 90px)",
          fontWeight: 900,
          color: "#00d4ff",
          lineHeight: 1,
          marginBottom: "32px",
          textShadow: "0 0 30px #00d4ff, 0 0 60px #00d4ff66"
        }}>
          RECON<span style={{ color: "#ff0040" }}>_</span>AI
        </div>

        {/* Typewriter subtitle */}
        <div style={{
          fontFamily: "'Share Tech Mono', monospace",
          fontSize: "clamp(11px, 2vw, 15px)",
          color: "#00ff41",
          letterSpacing: "4px",
          marginBottom: "48px",
          minHeight: "20px"
        }}>
          {text}
          <span style={{ opacity: showCursor ? 1 : 0, color: "#00d4ff" }}>█</span>
        </div>

        {/* Stats bar */}
        <div style={{
          display: "flex",
          gap: "40px",
          justifyContent: "center",
          marginBottom: "48px",
          flexWrap: "wrap"
        }}>
          {[
            { label: "MODULES", value: "04" },
            { label: "PROTOCOLS", value: "OSINT" },
            { label: "AI ENGINE", value: "LLAMA3" },
            { label: "STATUS", value: "ONLINE" }
          ].map((stat, i) => (
            <div key={i} style={{ textAlign: "center" }}>
              <div style={{
                fontFamily: "'Orbitron', monospace",
                fontSize: "24px",
                fontWeight: 700,
                color: "#00d4ff",
                textShadow: "0 0 10px #00d4ff"
              }}>{stat.value}</div>
              <div style={{
                fontSize: "10px",
                color: "#555",
                letterSpacing: "3px"
              }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Scroll indicator */}
        <div style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "8px",
          animation: "fadeInUp 1s ease 2s both"
        }}>
          <div style={{ fontSize: "11px", color: "#555", letterSpacing: "4px" }}>
            SCROLL TO INITIALIZE SCAN
          </div>
          <div style={{
            width: "1px",
            height: "50px",
            background: "linear-gradient(to bottom, #00ff41, transparent)",
            animation: "blink 2s infinite"
          }} />
        </div>
      </div>

      {/* Corner decorations */}
      {["top-left", "top-right", "bottom-left", "bottom-right"].map((pos, i) => (
        <div key={i} style={{
          position: "absolute",
          [pos.includes("top") ? "top" : "bottom"]: "20px",
          [pos.includes("left") ? "left" : "right"]: "20px",
          width: "40px",
          height: "40px",
          borderTop: pos.includes("top") ? "2px solid #00ff4166" : "none",
          borderBottom: pos.includes("bottom") ? "2px solid #00ff4166" : "none",
          borderLeft: pos.includes("left") ? "2px solid #00ff4166" : "none",
          borderRight: pos.includes("right") ? "2px solid #00ff4166" : "none",
          zIndex: 2
        }} />
      ))}
    </div>
  )
}

export default Hero