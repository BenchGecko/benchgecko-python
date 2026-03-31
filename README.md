# BenchGecko Python SDK

Official Python client for the [BenchGecko](https://benchgecko.ai) API. Query AI model data, benchmark scores, and run side-by-side comparisons programmatically.

BenchGecko tracks every major AI model, benchmark, and provider. This SDK wraps the public REST API so you can integrate AI model intelligence into your own tools, dashboards, and research workflows.

## Installation

```bash
pip install benchgecko
```

Requires Python 3.8 or later.

## Quick Start

```python
from benchgecko import BenchGecko

client = BenchGecko()

# List all tracked AI models
models = client.models()
print(f"Tracking {len(models)} models")

# List all benchmarks
benchmarks = client.benchmarks()
for b in benchmarks[:5]:
    print(b["name"])

# Compare two models head-to-head
comparison = client.compare(["gpt-4o", "claude-opus-4"])
for model_data in comparison["models"]:
    print(model_data["name"], model_data.get("scores", {}))
```

## API Reference

### `BenchGecko(base_url=None, timeout=30)`

Create a client instance. The default base URL points to the production BenchGecko API.

**Parameters:**
- `base_url` (str, optional): Override the API base URL. Useful for testing.
- `timeout` (int): Request timeout in seconds. Defaults to 30.

### `client.models() -> list`

Fetch all AI models tracked by BenchGecko. Returns a list of dictionaries, each containing model metadata such as name, provider, parameter count, pricing tiers, and benchmark scores.

### `client.benchmarks() -> list`

Fetch all benchmarks tracked by BenchGecko. Returns a list of dictionaries with benchmark name, category, description, and the number of models scored on each benchmark.

### `client.compare(models: list) -> dict`

Compare two or more models side by side. Pass a list of model slugs (e.g., `["gpt-4o", "claude-opus-4"]`). Returns a structured comparison with per-model scores, pricing, speed metrics, and capability breakdowns.

**Parameters:**
- `models` (list of str): At least 2 model slugs to compare.

**Raises:**
- `ValueError` if fewer than 2 models are provided.
- `BenchGeckoError` on API errors.

## Error Handling

All API errors raise `BenchGeckoError` with a human-readable message and optional HTTP status code:

```python
from benchgecko import BenchGecko
from benchgecko.client import BenchGeckoError

client = BenchGecko()
try:
    models = client.models()
except BenchGeckoError as e:
    print(f"API error: {e} (status: {e.status_code})")
```

## Configuration

You can point the client to a different API server for local development or testing:

```python
client = BenchGecko(base_url="http://localhost:3000", timeout=10)
```

## Data Attribution

Data provided by [BenchGecko](https://benchgecko.ai). Model benchmark scores are sourced from official evaluation suites and validated against published results. Pricing data is updated daily from provider APIs.

## Links

- [BenchGecko](https://benchgecko.ai) - AI model benchmarks, pricing, and rankings
- [API Documentation](https://benchgecko.ai/api-docs)
- [GitHub Repository](https://github.com/BenchGecko/benchgecko-python)

## License

MIT License. See [LICENSE](LICENSE) for details.
