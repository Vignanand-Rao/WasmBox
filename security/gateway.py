from security.blocked import check_blocked
from security.validator import validate
from security.timeout import check_timeout

def process_code(code):
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

    timeout = check_timeout(code)
    if timeout:
        return {
            "success": False,
            "errors": timeout
        }

    return {
        "success": True,
        "message": "Code passed validation."
    }