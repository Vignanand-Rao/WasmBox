from security.blocked import check_blocked
from security.validator import validate

def process_code(code):
    """
    Validates user code before execution.
    """

    blocked = check_blocked(code)
    if blocked:
        return {
            "success": False,
            "errors": blocked
        }

    errors = validate(code)
    if errors:
        return {
            "success": False,
            "errors": errors
        }

    return {
        "success": True,
        "message": "Code passed validation."
    }