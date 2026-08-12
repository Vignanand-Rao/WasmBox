"""
Execution engine for WasmBox utilizing configuration parameters.
"""

import os
import time
import tempfile
from typing import Dict, Any, List, Optional

from runtime.config import SandboxConfig

try:
    import wasmtime
    from wasmtime import (
        Config,
        Engine,
        Store,
        Module,
        Linker,
        WasiConfig,
    )
except ImportError:
    wasmtime = None


class WasmExecutor:

    def __init__(self, config: Optional[SandboxConfig] = None):
        if wasmtime is None:
            raise ImportError(
                "The 'wasmtime' package is required. "
                "Install it using: pip install wasmtime"
            )

        self.sandbox_config = config or SandboxConfig()

        # Configure Wasmtime.
        wasm_config = Config()

        # Enable fuel-based execution limits.
        wasm_config.consume_fuel = True

        self.engine = Engine(wasm_config)

    def execute(
        self,
        wasm_path: str,
        entry_function: str = "_start",
        func_args: Optional[List[Any]] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:

        if not os.path.exists(wasm_path):
            return {
                "success": False,
                "error": f"WASM binary not found at: {wasm_path}",
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "execution_time_ms": 0.0,
            }

        func_args = func_args or []
        env_vars = env_vars or {}

        stdout_fd, stdout_path = tempfile.mkstemp()
        stderr_fd, stderr_path = tempfile.mkstemp()

        start_time = time.perf_counter()

        try:
            # ---------------------------------------------------------
            # WASI configuration
            # ---------------------------------------------------------
            wasi_config = WasiConfig()

            wasi_config.stdout_file = stdout_path
            wasi_config.stderr_file = stderr_path

            # Only expose the temporary execution directory.
            wasi_config.preopen_dir(
                tempfile.gettempdir(),
                "/tmp"
            )

            wasi_config.argv = [
                wasm_path
            ] + [str(a) for a in func_args]

            wasi_config.env = list(env_vars.items())

            # ---------------------------------------------------------
            # Store configuration
            # ---------------------------------------------------------
            store = Store(self.engine)

            store.set_wasi(wasi_config)

            # ---------------------------------------------------------
            # Fuel limit
            # ---------------------------------------------------------
            if self.sandbox_config.fuel_limit > 0:
                store.set_fuel(
                    self.sandbox_config.fuel_limit
                )

            # ---------------------------------------------------------
            # Memory limit
            # ---------------------------------------------------------
            # WebAssembly page = 64 KiB.
            # 256 pages = 16 MiB.
            memory_limit_bytes = (
                self.sandbox_config.MAX_MEMORY_PAGES
                * 64
                * 1024
            )

            store.set_limits(
                memory_size=memory_limit_bytes
            )

            # ---------------------------------------------------------
            # Linker and module
            # ---------------------------------------------------------
            linker = Linker(self.engine)
            linker.define_wasi()

            module = Module.from_file(
                self.engine,
                wasm_path
            )

            instance = linker.instantiate(
                store,
                module
            )

            # ---------------------------------------------------------
            # Execute WASM
            # ---------------------------------------------------------
            if entry_function == "_start":

                start_func = instance.exports(
                    store
                ).get("_start")

                if start_func:
                    start_func(store)
                else:
                    raise RuntimeError(
                        "No '_start' exported function "
                        "in WASM module."
                    )

            else:

                target_func = instance.exports(
                    store
                ).get(entry_function)

                if not target_func:
                    raise RuntimeError(
                        f"Exported function "
                        f"'{entry_function}' not found."
                    )

                target_func(
                    store,
                    *func_args
                )

            execution_time = (
                time.perf_counter() - start_time
            ) * 1000

            stdout_text = self._read_and_clean(
                stdout_path,
                stdout_fd
            )

            stderr_text = self._read_and_clean(
                stderr_path,
                stderr_fd
            )

            return {
                "success": True,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": 0,
                "execution_time_ms": round(
                    execution_time,
                    2
                ),
            }

        except Exception as e:

            execution_time = (
                time.perf_counter() - start_time
            ) * 1000

            stdout_text = self._read_and_clean(
                stdout_path,
                stdout_fd
            )

            stderr_text = self._read_and_clean(
                stderr_path,
                stderr_fd
            )

            return {
                "success": False,
                "error": str(e),
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": 1,
                "execution_time_ms": round(
                    execution_time,
                    2
                ),
            }

    @staticmethod
    def _read_and_clean(
        file_path: str,
        fd: int
    ) -> str:

        try:
            os.close(fd)

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="replace",
            ) as f:
                content = f.read()

            if os.path.exists(file_path):
                os.remove(file_path)

            return content

        except Exception:
            return ""