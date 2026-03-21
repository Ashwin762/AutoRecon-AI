import { useState } from "react"
import Hero from "./components/Hero"
import Scanner from "./components/Scanner"
import Results from "./components/Results"
import { useScrollReveal } from "./hooks/useScrollReveal"
import "./index.css"

function App() {
  const [scanResults, setScanResults] = useState(null)
  const [isScanning, setIsScanning] = useState(false)
  useScrollReveal()

  return (
    <div className="app">
      <Hero />
      <Scanner
        setScanResults={setScanResults}
        setIsScanning={setIsScanning}
        isScanning={isScanning}
      />
      {scanResults && (
        <Results results={scanResults} />
      )}
    </div>
  )
}

export default App