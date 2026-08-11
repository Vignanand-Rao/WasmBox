import subprocess


def check_timeout(code):
    return []


def execute(file):
    try:
        result = subprocess.run(
            ["python", file],
            timeout=5,
            capture_output=True,
            text=True
        )

        return result.stdout

    except subprocess.TimeoutExpired:
        return "Execution Timeout"