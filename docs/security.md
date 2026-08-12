# WasmBox Security

WasmBox executes user-submitted Python code inside a WebAssembly-based sandbox.

The security architecture has multiple layers:

```text
User Code
    │
    ▼
Security Gateway
    │
    ├── Blocked module/function checks
    │
    └── AST validation
    │
    ▼
Python WASM Runtime
    │
    ▼
Wasmtime Sandbox
    │
    ├── Fuel Limit
    ├── Memory Limit
    └── WASI Filesystem Isolation
    │
    ▼
Execution Result
