BLOCKED_MODULES = [
"os",
"sys",
"socket",
"subprocess",
"shutil",
"pathlib",
"ctypes",
"multiprocessing"
]

BLOCKED_FUNCTIONS = [
"eval",
"exec",
"compile",
"open",
"__import__"
]

def check_blocked(code):
    """
    Checks if the code contains blocked modules or functions.
    Returns a list of detected issues.
    """

    issues = []

    # Check blocked modules
    for module in BLOCKED_MODULES:
        if f"import {module}" in code or f"from {module}" in code:
            issues.append(f"Blocked module used: {module}")

    # Check blocked functions
    for func in BLOCKED_FUNCTIONS:
        if f"{func}(" in code:
            issues.append(f"Blocked function used: {func}")

    return issues