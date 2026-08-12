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

  const handleRun = async () => {
    setError("");
    setOutput("");

    // Check for empty code before sending the request
    if (!code.trim()) {
      setStatus("Failed");
      setError("Code block is empty");
      setExecutionTime("0.00 ms");
      setMemoryUsage("0.00 MB");
      return;
    }

    setLoading(true);
    setStatus("Running");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/execute",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            code: code,
            language: "python",
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        let errorMessage = "Execution failed";

        if (Array.isArray(result.detail)) {
            errorMessage = result.detail
            .map((item) => item.msg || "Invalid request")
            .join("\n");
          } else if (typeof result.detail === "string") {
            errorMessage = result.detail;
          }

          throw new Error(errorMessage);
      }

      setOutput(result.output || "");

      setExecutionTime(
        `${Number(result.execution_time || 0).toFixed(2)} ms`
      );

      setMemoryUsage(
        `${Number(result.memory_usage || 0).toFixed(2)} MB`
      );

      if (result.status === "success") {
        setStatus("Success");
        setError("");
      } else {
        setStatus("Failed");

        setError(
          result.errors?.join("\n") || "Execution failed"
        );
      }
    } catch (err) {
      setStatus("Failed");

      setError(
        err.message || "Unable to connect to backend"
      );

      setOutput("");
      setExecutionTime("0.00 ms");
      setMemoryUsage("0.00 MB");
    } finally {
      setLoading(false);
    }
  };

  const handleEditorMount = (editor) => {
    editor.addCommand(2048 | 3, handleRun);
  };

  const handleClear = () => {
    setOutput("");
    setError("");
    setStatus("Idle");
    setExecutionTime("0.00 ms");
    setMemoryUsage("0.00 MB");
  };

  const handleReset = () => {
    setCode(`print("Welcome to WasmBox!")`);
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

  const handleDownload = () => {
    if (!output) return;

    const blob = new Blob([output], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "output.txt";
    link.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>⚡ WasmBox</h1>

        <div className="header-actions">
          <button
            className="run-btn"
            onClick={handleRun}
            disabled={loading}
          >
            {loading ? "Running..." : "Run ▶"}
          </button>

          <button
            className="reset-btn"
            onClick={handleReset}
            disabled={loading}
          >
            Reset
          </button>
        </div>
      </header>

      <div className="status">
        Status:
        <span
          className={`status-badge ${status.toLowerCase()}`}
        >
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

          <p className="editor-hint">
            Press Ctrl + Enter to run your code
          </p>

          <Editor
            height="600px"
            language="python"
            theme="vs-dark"
            value={code}
            onChange={(value) => setCode(value || "")}
            onMount={handleEditorMount}
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
                  className="download-btn"
                  onClick={handleDownload}
                >
                  Download
                </button>

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
              execute  </button>
              </div>
            </div>

            <div className="console-box">
              <pre className="output-text">
                {output ||
                  "Program output will appear here..."}
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
