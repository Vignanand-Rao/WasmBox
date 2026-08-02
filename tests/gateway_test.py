import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security.gateway import process_code

code = """
eval("2+2")
"""

result = process_code(code)
print(result)