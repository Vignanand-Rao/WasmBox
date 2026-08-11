"""
runtime/compiler.py
-------------------
Handles preparation and packaging of Python source code 
for execution inside the WasmBox sandbox environment.
"""

import os
import uuid
import tempfile
from typing import Dict, Any

class PythonWasmCompiler:
    def __init__(self, workspace_dir: str = None):
        self.workspace_dir = workspace_dir or tempfile.gettempdir()
        os.makedirs(self.workspace_dir, exist_ok=True)

    def prepare_script(self, python_code_source: str) -> str:
        """
        Receives raw Python source code from the frontend, saves it into a 
        temporary execution script, and returns the file path.
        """
        # Generate a unique filename for the isolated run
        job_id = uuid.uuid4().hex[:8]
        script_filename = f"job_{job_id}.py"
        script_path = os.path.join(self.workspace_dir, script_filename)

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(python_code_source)

        return script_path

    def get_execution_payload(self, python_code_source: str, python_wasm_binary_path: str) -> Dict[str, Any]:
        """
        Prepares the payload linking the base Python WASM runtime interpreter 
        with the user's custom source script.
        """
        script_path = self.prepare_script(python_code_source)

        if not os.path.exists(python_wasm_binary_path):
            return {
                "success": False,
                "error": f"Base Python WASM binary not found at: {python_wasm_binary_path}",
                "wasm_path": None,
                "args": []
            }

        # The WASM binary (Python interpreter) is executed, passing the user script as an argument
        return {
            "success": True,
            "error": None,
            "wasm_path": python_wasm_binary_path,
            "script_path": script_path,
            "guest_script_path": f"/tmp/{os.path.basename(script_path)}",
            "args": [f"/tmp/{os.path.basename(script_path)}"]
        }