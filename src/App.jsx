import { useState } from "react";
import "./App.css";
import Editor from "@monaco-editor/react";
function App() {
const [code, setCode] = useState(`print("Welcome to WasmBox!")`
);

const [output, setOutput] = useState("");
const [error, setError] = useState("");
const [loading, setLoading] = useState(false);
const handleRun = () => {

  setLoading(true);
  setError("");

  setTimeout(() => {

    setOutput(`Running Python Code...

${code}

Execution Completed Successfully.`);

    setLoading(false);

  }, 1500);

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
          minimap: { enabled: false },
          automaticLayout: true,
        }}
      />

        </div>

        <div className="output-section">

          <div className="console">
            <h3>🖥 Output</h3>
            <div className="console-box">
  <pre>{output}</pre>
</div>
          </div>

          <div className="console">
            <h3>⚠ Errors</h3>
            <div className="console-box">
  <pre>{error}</pre>
</div>
          </div>

        </div>

      </main>

    </div>
  );
}

export default App;