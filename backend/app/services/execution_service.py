from security.gateway import process_code

def execute_code(code: str):
    """
    Executes the submitted code after passing it
    through the security gateway.
    """

    if not code.strip():
        return {
            "status": "failed",
            "errors": ["Code cannot be empty"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    try:
        security_result = process_code(code)
    except Exception as e:
        return {
            "status": "failed",
            "errors": [str(e)],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    if not security_result["success"]:
        return {
            "status": "failed",
            "errors": security_result["errors"],
            "output": "",
            "execution_time": 0.00,
            "memory_usage": 0.00
        }

    return {
        "status": "success",
        "output": security_result["message"],
        "execution_time": 0.00,
        "memory_usage": 0.00
    }