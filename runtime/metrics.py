import tracemalloc

def start_memory_tracking():
    """Starts tracking memory allocations."""
    tracemalloc.start()

def stop_memory_tracking() -> float:
    """
    Stops memory tracking and returns peak memory usage in Megabytes (MB).
    """
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = round(peak / (1024 * 1024), 2)
    return peak_mb
