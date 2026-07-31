"""
runtime/executor.py
-------------------
Execution engine for WasmBox. Handles WebAssembly binary loading,
WASI sandbox isolation, argument passing, memory/time constraints,
and output capture.
"""

import os
import sys
import time
import tempfile
from typing import Dict, Any, List, Optional
try:
    import wasmtime
    from wasmtime import Engine, Store, Module, Linker, WasiConfig, Config, WasmtimeError
except ImportError:
    wasmtime = None


class WasmExecutor:
    """
    Sandboxed WebAssembly Executor using Wasmtime.
    """

    def __init__(self, epoch_interruption: bool = False, max_memory_bytes: Optional[int] = None):
        if wasmtime is None:
            raise ImportError(
                "The 'wasmtime' package is required. Install it using: pip install wasmtime"
            )
        
        self.config = Config()
        # Enable consume_fuel if you want strict CPU/instruction limits
        self.config.consume_fuel = True
        
        self.engine = Engine(self.config)

    def execute(
        self,
        wasm_path: str,
        entry_function: str = "_start",
        func_args: Optional[List[Any]] = None,
        env_vars: Optional[Dict[str, str]] = None,
        fuel_limit: int = 1_000_000_000,  # Default execution fuel cap
    ) -> Dict[str, Any]:
        """
        Executes a WASM binary within a sandboxed environment.

        :param wasm_path: Path to the .wasm binary file.
        :param entry_function: Function to invoke (default '_start' for WASI CLI apps).
        :param func_args: Arguments to pass to WASM functions.
        :param env_vars: Environment variables exposed inside the sandbox.
        :param fuel_limit: Maximum allowed CPU fuel/instructions.
        :return: Execution results dictionary.
        """
        if not os.path.exists(wasm_path):
            return {
                "success": False,
                "error": f"WASM binary not found at: {wasm_path}",
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "execution_time_ms": 0.0
            }

        func_args = func_args or []
        env_vars = env_vars or {}

        # Set up temporary files to capture stdout and stderr safely
        stdout_fd, stdout_path = tempfile.mkstemp()
        stderr_fd, stderr_path = tempfile.mkstemp()

        start_time = time.perf_counter()

        try:
            # 1. Setup WASI configuration
            wasi_config = WasiConfig()
            wasi_config.stdout_file = stdout_path
            wasi_config.stderr_file = stderr_path
            
            # Pass command line arguments to WASI
            wasi_args = [wasm_path] + [str(a) for a in func_args]
            wasi_config.argv = wasi_args

            # Pass environment variables
            wasi_config.env = list(env_vars.items())

            # 2. Setup Store & Linker
            store = Store(self.engine)
            store.set_wasi(wasi_config)
            
            # Set fuel limit for CPU safety
            if fuel_limit > 0:
                store.add_fuel(fuel_limit)

            linker = Linker(self.engine)
            linker.define_wasi()

            # 3. Load Module and Instantiate
            module = Module.from_file(self.engine, wasm_path)
            instance = linker.instantiate(store, module)

            # 4. Invoke Entry Point
            exit_code = 0
            ret_val = None

            if entry_function == "_start":
                # Standard WASI entry point
                start_func = instance.exports(store).get("_start")
                if start_func:
                    start_func(store)
                else:
                    raise RuntimeError("No '_start' exported function found in WASM module.")
            else:
                # Custom function execution
                target_func = instance.exports(store).get(entry_function)
                if not target_func:
                    raise RuntimeError(f"Exported function '{entry_function}' not found.")
                ret_val = target_func(store, *func_args)

            execution_time = (time.perf_counter() - start_time) * 1000

            # Read captured outputs
            stdout_text = self._read_and_clean(stdout_path, stdout_fd)
            stderr_text = self._read_and_clean(stderr_path, stderr_fd)

            return {
                "success": True,
                "result": ret_val,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": exit_code,
                "execution_time_ms": round(execution_time, 2)
            }

        except WasmtimeError as e:
            execution_time = (time.perf_counter() - start_time) * 1000
            stdout_text = self._read_and_clean(stdout_path, stdout_fd)
            stderr_text = self._read_and_clean(stderr_path, stderr_fd)
            
            return {
                "success": False,
                "error": f"WASM Execution Trap/Trap Error: {str(e)}",
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": 1,
                "execution_time_ms": round(execution_time, 2)
            }

        except Exception as e:
            execution_time = (time.perf_counter() - start_time) * 1000
            stdout_text = self._read_and_clean(stdout_path, stdout_fd)
            stderr_text = self._read_and_clean(stderr_path, stderr_fd)

            return {
                "success": False,
                "error": str(e),
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": -1,
                "execution_time_ms": round(execution_time, 2)
            }

    @staticmethod
    def _read_and_clean(file_path: str, fd: int) -> str:
        """Reads output from temp file and cleans up file descriptors."""
        try:
            os.close(fd)
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if os.path.exists(file_path):
                os.remove(file_path)
            return content
        except Exception:
            return ""


if __name__ == "__main__":
    # Quick standalone test execution
    print("Initializing WasmBox Executor...")
    executor = WasmExecutor()
    print("Executor ready.")