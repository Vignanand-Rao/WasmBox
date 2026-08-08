import logging

from security.gateway import process_code


logger = logging.getLogger(__name__)


def execute_code(code: str):
    """
    Executes the submitted code after passing it
    through the security gateway.
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

    return {
        "status": "success",
        "output": security_result["message"],
        "execution_time": 0.00,
        "memory_usage": 0.00
    }