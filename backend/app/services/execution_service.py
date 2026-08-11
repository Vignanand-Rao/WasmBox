import logging
import os

from security.gateway import process_code
from runtime.config import SandboxConfig
from runtime.compiler import PythonWasmCompiler
from runtime.executor import WasmExecutor

logger = logging.getLogger(__name__)


# WasmBox project root:
# WasmBox/backend/app/services/execution_service.py
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

PYTHON_WASM_PATH = os.path.join(
    PROJECT_ROOT,
    "bin",
    "python.wasm"
)


def execute_code(code: str):
    """
    Validate and execute submitted Python code inside the WasmBox
    WebAssembly runtime.
    """

    logger.info("Code execution request received")

    if not code.strip():
        logger.warning("Code execution rejected: empty code")

        return {
            "status": "failed",
            "errors": ["Code cannot be empty"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    # Step 1: Security validation
    try:
        security_result = process_code(code)

    except Exception:
        logger.exception("Security gateway failed while processing code")

        return {
            "status": "failed",
            "errors": ["Security validation failed"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    if not security_result["success"]:
        logger.warning("Code execution rejected by security gateway")

        return {
            "status": "failed",
            "errors": security_result["errors"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    logger.info("Code passed security validation")

    # Step 2: Prepare Python source for WASM execution
    try:
        compiler = PythonWasmCompiler()

        payload = compiler.get_execution_payload(
            code,
            PYTHON_WASM_PATH
        )

        if not payload["success"]:
            logger.error("WASM preparation failed: %s", payload["error"])

            return {
                "status": "failed",
                "errors": [payload["error"]],
                "output": "",
                "execution_time": 0.00,
                "memory_usage": 0.00
            }

    except Exception:
        logger.exception("Failed to prepare Python code for WASM execution")

        return {
            "status": "failed",
            "errors": ["Failed to prepare code for execution"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    # Step 3: Execute Python code through Wasmtime
    try:
        config = SandboxConfig()
        executor = WasmExecutor(config=config)

        execution_result = executor.execute(
            wasm_path=payload["wasm_path"],
            entry_function="_start",
            func_args=payload["args"]
        )

    except Exception:
        logger.exception("WASM execution engine failed")

        return {
            "status": "failed",
            "errors": ["WASM execution failed"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    # Step 4: Convert runtime result to API response
    if not execution_result["success"]:
        errors = []

        if execution_result.get("stderr"):
            errors.append(execution_result["stderr"])

        if execution_result.get("error"):
            errors.append(execution_result["error"])

        return {
            "status": "failed",
            "errors": errors or ["Code execution failed"],
            "output": execution_result.get("stdout", ""),
            "execution_time": execution_result.get(
                "execution_time_ms", 0.0
            ) / 1000,
            "memory_usage": 0.00
        }

    return {
        "status": "success",
        "errors": (
            [execution_result["stderr"]]
            if execution_result.get("stderr")
            else None
        ),
        "output": execution_result.get("stdout", ""),
        "execution_time": execution_result.get(
            "execution_time_ms", 0.0
        ) / 1000,
        "memory_usage": 0.00
    }
