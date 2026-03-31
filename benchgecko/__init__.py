"""BenchGecko - Official Python SDK for the BenchGecko API.

Compare AI models, benchmarks, and pricing programmatically.

Usage:
    from benchgecko import BenchGecko

    client = BenchGecko()
    models = client.models()
    benchmarks = client.benchmarks()
    comparison = client.compare(["gpt-4o", "claude-opus-4"])
"""

from benchgecko.client import BenchGecko

__version__ = "0.1.0"
__all__ = ["BenchGecko"]
