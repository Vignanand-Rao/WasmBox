"""
runtime/config.py
-----------------
Global configuration settings and limits for WasmBox execution.
"""

class SandboxConfig:
    # Default execution constraints
    DEFAULT_FUEL_LIMIT: int = 1_000_000_000
    DEFAULT_TIMEOUT_SECONDS: float = 5.0
    MAX_MEMORY_PAGES: int = 256  # 16MB default memory limit (64KB per page)
    
    def __init__(self, fuel_limit: int = None, timeout: float = None):
        self.fuel_limit = fuel_limit or self.DEFAULT_FUEL_LIMIT
        self.timeout = timeout or self.DEFAULT_TIMEOUT_SECONDS