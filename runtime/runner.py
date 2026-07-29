import subprocess
import sys
import time
import tempfile
import os

def run_python_code(code: str, timeout_seconds: int = 5) -> dict:
    """
    Executes raw Python code inside an isolated subprocess.
    Captures stdout, stderr, execution time, and handles timeouts/exceptions.
    """
    start_time = time.perf_counter()
    
    # Write code to a temporary file for clean execution
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        # Run the code using Python's executable in an isolated subprocess
        process = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        
        execution_time = round((time.perf_counter() - start_time) * 1000, 2)  # in ms
        
        return {
            "status": "success" if process.returncode == 0 else "error",
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode,
            "execution_time_ms": execution_time,
            "memory_usage_mb": None
        }

    except subprocess.TimeoutExpired:
        execution_time = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "status": "timeout",
            "stdout": "",
            "stderr": f"Execution Timed Out: Program exceeded limit of {timeout_seconds} seconds.",
            "exit_code": -1,
            "execution_time_ms": execution_time,
            "memory_usage_mb": None
        }
    except Exception as e:
        return {
            "status": "exception",
            "stdout": "",
            "stderr": f"Runtime Engine Error: {str(e)}",
            "exit_code": -1,
            "execution_time_ms": 0,
            "memory_usage_mb": None
        }
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    sample_code = "print('Hello from WasmBox Runtime!')"
    result = run_python_code(sample_code)
    print("Execution Result:", result)