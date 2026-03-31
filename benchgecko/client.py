"""BenchGecko API client for Python.

Provides a clean interface to the BenchGecko REST API for querying
AI model data, benchmark scores, and model comparisons.
"""

import requests
from typing import Any, Dict, List, Optional


class BenchGeckoError(Exception):
    """Base exception for BenchGecko API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class BenchGecko:
    """Client for the BenchGecko API.

    Provides methods to query AI models, benchmarks, and perform
    side-by-side model comparisons.

    Args:
        base_url: API base URL. Defaults to https://benchgecko.ai.
        timeout: Request timeout in seconds. Defaults to 30.

    Example:
        >>> client = BenchGecko()
        >>> models = client.models()
        >>> print(len(models))
        346
    """

    DEFAULT_BASE_URL = "https://benchgecko.ai"

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": f"benchgecko-python/0.1.0",
            "Accept": "application/json",
        })

    def _request(self, method: str, path: str, params: Optional[Dict] = None) -> Any:
        """Send a request to the BenchGecko API.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: API endpoint path (e.g., /api/v1/models).
            params: Optional query parameters.

        Returns:
            Parsed JSON response.

        Raises:
            BenchGeckoError: If the API returns a non-2xx status code.
        """
        url = f"{self.base_url}{path}"
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise BenchGeckoError(
                f"API request failed: {e}",
                status_code=e.response.status_code if e.response else None,
            ) from e
        except requests.exceptions.ConnectionError as e:
            raise BenchGeckoError(f"Connection failed: {e}") from e
        except requests.exceptions.Timeout as e:
            raise BenchGeckoError(f"Request timed out after {self.timeout}s") from e

    def models(self) -> List[Dict[str, Any]]:
        """List all AI models tracked by BenchGecko.

        Returns a list of model objects, each containing metadata like
        name, provider, parameter count, pricing, and benchmark scores.

        Returns:
            List of model dictionaries.

        Example:
            >>> client = BenchGecko()
            >>> models = client.models()
            >>> for m in models[:3]:
            ...     print(m["name"])
        """
        return self._request("GET", "/api/v1/models")

    def benchmarks(self) -> List[Dict[str, Any]]:
        """List all benchmarks tracked by BenchGecko.

        Returns a list of benchmark objects, each containing metadata
        like name, category, description, and associated scores.

        Returns:
            List of benchmark dictionaries.

        Example:
            >>> client = BenchGecko()
            >>> benchmarks = client.benchmarks()
            >>> for b in benchmarks[:3]:
            ...     print(b["name"])
        """
        return self._request("GET", "/api/v1/benchmarks")

    def compare(self, models: List[str]) -> Dict[str, Any]:
        """Compare two or more AI models side by side.

        Accepts a list of model identifiers (slugs or names) and returns
        a structured comparison including benchmark scores, pricing, and
        capability differences.

        Args:
            models: List of model slugs to compare (e.g., ["gpt-4o", "claude-opus-4"]).

        Returns:
            Comparison result dictionary with per-model data.

        Raises:
            ValueError: If fewer than 2 models are provided.

        Example:
            >>> client = BenchGecko()
            >>> result = client.compare(["gpt-4o", "claude-opus-4"])
            >>> for model_data in result["models"]:
            ...     print(model_data["name"], model_data.get("scores", {}))
        """
        if len(models) < 2:
            raise ValueError("At least 2 models are required for comparison.")
        return self._request("GET", "/api/v1/compare", params={
            "models": ",".join(models),
        })

    def __repr__(self) -> str:
        return f"BenchGecko(base_url={self.base_url!r})"
