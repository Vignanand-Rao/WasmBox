import { useState } from "react";
import "./App.css";
import Editor from "@monaco-editor/react";

function App() {
  const [code, setCode] = useState(`print("Welcome to WasmBox!")`);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("Idle");
  const [executionTime, setExecutionTime] = useState("0.00 ms");
  const [memoryUsage, setMemoryUsage] = useState("0.00 MB");

  const handleRun = () => {
    setLoading(true);
    setStatus("Running");
    setError("");

    setTimeout(() => {
      setOutput(`Running Python Code...

${code}

Execution Completed Successfully.`);

      setExecutionTime("42.15 ms");
      setMemoryUsage("3.84 MB");

      setLoading(false);
      setStatus("Success");
    }, 1500);
  };

  const handleClear = () => {
    setOutput("");
    setError("");
    setStatus("Idle");
    setExecutionTime("0.00 ms");
    setMemoryUsage("0.00 MB");
  };

  const handleCopy = async () => {
  if (!output) return;

      try {
        await navigator.clipboard.writeText(output);
        alert("Output copied to clipboard!");
      } catch (err) {
        alert("Failed to copy output.");
      }
    };

  return (
    <div className="container">
      <header className="header">
        <h1>⚡ WasmBox</h1>

        <button
          className="run-btn"
          onClick={handleRun}
          disabled={loading}
        >
          {loading ? "Running..." : "Run ▶"}
        </button>
      </header>

      <div className="status">
        Status:
        <span className={`status-badge ${status.toLowerCase()}`}>
          {status}
        </span>
      </div>

      <div className="metrics">
        <div className="metric-card">
          <h4>Execution Time</h4>
          <p>{executionTime}</p>
        </div>

        <div className="metric-card">
          <h4>Memory Usage</h4>
          <p>{memoryUsage}</p>
        </div>
      </div>

      <main className="main-content">
        <div className="editor-section">
          <h3>🐍 Python Editor</h3>

          <Editor
            height="600px"
            language="python"
            theme="vs-dark"
            value={code}
            onChange={(value) => setCode(value || "")}
            options={{
              fontSize: 16,
              fontFamily: "Consolas",
              minimap: { enabled: false },
              automaticLayout: true,
              wordWrap: "on",
              scrollBeyondLastLine: false,
              lineNumbers: "on",
              roundedSelection: true,
              cursorBlinking: "smooth",
              cursorSmoothCaretAnimation: "on",
              renderLineHighlight: "all",
              padding: {
                top: 12,
                bottom: 12,
              },
            }}
          />
        </div>

        <div className="output-section">
          <div className="console">
<div className="console-header">
  <h3>🖥 Output</h3>

  <div className="console-actions">
    <button
            className="copy-btn"
            onClick={handleCopy}
          >
            Copy
          </button>

          <button
            className="clear-btn"
            onClick={handleClear}
          >
            Clear
          </button>
        </div>
      </div>

            <div className="console-box">
              <pre className="output-text">
                {output || "Program output will appear here..."}
              </pre>
            </div>
          </div>

          <div className="console">
            <h3>⚠ Errors</h3>

            <div className="console-box">
              <pre className="error-text">
                {error || "No errors"}
              </pre>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;