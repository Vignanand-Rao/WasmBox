"""
runtime/runner.py
----------------
Main entry point runner for WasmBox. Handles command-line invocation
and coordinates with the execution engine.
"""
import sys
import os

# Ensure the root directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from security.gateway import process_code
from runtime.executor import WasmExecutor

def main():
    print("=== WasmBox Runner Initialized ===")
    
    # Target .wasm file to run (adjust path as needed for your project tests)
    target_wasm = sys.argv[1] if len(sys.argv) > 1 else "sample.wasm"
    
    if not os.path.exists(target_wasm):
        print(f"[-] Warning: Target WASM file '{target_wasm}' not found.")
        print("[*] Place a compiled .wasm file in your directory or pass its path as an argument.")
        print("    Example: python runtime/runner.py path/to/module.wasm")
        return

    print(f"[*] Loading execution engine for: {target_wasm}")
    executor = WasmExecutor()
    
    user_code = 'print("Hello")'
    
    security_result = process_code(user_code)
    if not security_result["success"]:
        print("\n--- Security Report ---")
        print(security_result["errors"])
        return
    
    
    # Execute the module
    result = executor.execute(target_wasm)
    
    print("\n--- Execution Report ---")
    print(f"Success: {result['success']}")
    print(f"Exit Code: {result['exit_code']}")
    print(f"Execution Time: {result['execution_time_ms']} ms")
    
    if result["stdout"]:
        print("\n[STDOUT]:")
        print(result["stdout"].strip())
        
    if result["stderr"]:
        print("\n[STDERR]:")
        print(result["stderr"].strip())
        
    if not result["success"] and result["error"]:
        print("\n[ERROR]:")
        print(result["error"])

if __name__ == "__main__":
    main()