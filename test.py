from validator import validate

code = """
import os
print("Hello")
"""
errors = validate(code)
if errors:
    print(errors)
else:
    print("Safe")