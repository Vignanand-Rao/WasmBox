import sys
import os

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from security.gateway import process_code

def execute_code(code: str):

    security_result = process_code(code)

    if not security_result["success"]:
        return {
            "status": "failed",
            "errors": security_result["errors"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    # TODO:
    # Call compiler.py here when available
    # Then pass the generated .wasm file to runtime.executor

    return {
        "status": "success",
        "output": security_result["message"],
        "execution_time": 0.00,
        "memory_usage": 0.00
    }