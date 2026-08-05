"""
runtime/runner.py
----------------
Main entry point runner for WasmBox. Handles command-line invocation
and coordinates with the compiler, config, and execution engine.
"""

import sys
import os
import argparse

# Ensure the root directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from runtime.config import SandboxConfig
from runtime.compiler import PythonWasmCompiler
from runtime.executor import WasmExecutor

def main():
    parser = argparse.ArgumentParser(description="WasmBox CLI Runner")
    parser.add_argument("target", help="Path to a compiled .wasm file or a .py script to execute")
    parser.add_argument("--wasm-runtime", default="bin/python.wasm", help="Path to the base Python WASM interpreter binary")
    parser.add_argument("--fuel", type=int, default=1_000_000_000, help="Fuel limit for sandbox execution")
    
    # Parse known arguments to allow passing extra args to the script
    args, extra_args = parser.parse_known_args()

    print("=== WasmBox Runner Initialized ===")
    
    if not os.path.exists(args.target):
        print(f"[-] Error: Target file '{args.target}' not found.")
        return

    # Initialize configuration and executor
    config = SandboxConfig(fuel_limit=args.fuel)
    executor = WasmExecutor(config=config)
    
    target_wasm = args.target
    func_args = extra_args

    # If a Python source script is passed, compile/prepare it using the compiler module
    if args.target.endswith(".py"):
        print(f"[*] Detected Python source script. Preparing via compiler module...")
        compiler = PythonWasmCompiler()
        
        with open(args.target, "r", encoding="utf-8") as f:
            source_code = f.read()
            
        payload = compiler.get_execution_payload(source_code, args.wasm_runtime)
        
        if not payload["success"]:
            print(f"[-] Compilation/Preparation Error: {payload['error']}")
            return
            
        target_wasm = payload["wasm_path"]
        func_args = payload["args"] + extra_args

    print(f"[*] Loading execution engine for: {target_wasm}")
    result = executor.execute(
        wasm_path=target_wasm,
        entry_function="_start",
        func_args=func_args
    )
    
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