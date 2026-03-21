function RiskGauge({ score }) {
  const getColor = (s) => {
    if (s >= 70) return "#ff0040"
    if (s >= 40) return "#ffd700"
    return "#00ff41"
  }

  const getLabel = (s) => {
    if (s >= 70) return "CRITICAL"
    if (s >= 40) return "MEDIUM"
    return "LOW"
  }

  const color = getColor(score)
  const circumference = 2 * Math.PI * 54
  const strokeDash = (score / 100) * circumference

  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ position: "relative", display: "inline-block" }}>
        <svg width="140" height="140" style={{ transform: "rotate(-90deg)" }}>
          <circle
            cx="70" cy="70" r="54"
            fill="none"
            stroke="#111"
            strokeWidth="8"
          />
          <circle
            cx="70" cy="70" r="54"
            fill="none"
            stroke={color}
            strokeWidth="8"
            strokeDasharray={`${strokeDash} ${circumference}`}
            strokeLinecap="round"
            style={{
              filter: `drop-shadow(0 0 8px ${color})`,
              transition: "stroke-dasharray 1s ease"
            }}
          />
        </svg>
        <div style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center"
        }}>
          <div style={{
            fontFamily: "'Orbitron', monospace",
            fontSize: "28px",
            fontWeight: 900,
            color,
            textShadow: `0 0 20px ${color}`
          }}>{score}</div>
          <div style={{
            fontSize: "9px",
            color: "#555",
            letterSpacing: "2px"
          }}>/100</div>
        </div>
      </div>
      <div style={{
        fontFamily: "'Orbitron', monospace",
        fontSize: "12px",
        fontWeight: 700,
        color,
        letterSpacing: "4px",
        marginTop: "8px",
        textShadow: `0 0 10px ${color}`
      }}>{getLabel(score)}</div>
    </div>
  )
}

export default RiskGauge