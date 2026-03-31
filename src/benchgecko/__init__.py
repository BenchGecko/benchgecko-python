"""
BenchGecko - AI Model Data Platform Client

Compare LLM benchmarks, estimate inference costs, and explore pricing
across 55+ providers. Data sourced from benchgecko.ai.
"""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = [
    "get_model",
    "compare_models",
    "get_pricing",
    "list_benchmarks",
    "list_models",
    "list_providers",
    "estimate_cost",
]

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Internal catalogue (snapshot -- use the API for live data)
# ---------------------------------------------------------------------------

_MODELS: Dict[str, Dict[str, Any]] = {
    "gpt-4o": {
        "name": "GPT-4o",
        "provider": "OpenAI",
        "context_window": 128_000,
        "input_price_per_1m": 2.50,
        "output_price_per_1m": 10.00,
        "benchmarks": {"mmlu": 88.7, "humaneval": 90.2, "gpqa": 53.6, "math": 76.6},
    },
    "gpt-4o-mini": {
        "name": "GPT-4o Mini",
        "provider": "OpenAI",
        "context_window": 128_000,
        "input_price_per_1m": 0.15,
        "output_price_per_1m": 0.60,
        "benchmarks": {"mmlu": 82.0, "humaneval": 87.0, "gpqa": 40.2, "math": 70.2},
    },
    "claude-3-5-sonnet": {
        "name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "context_window": 200_000,
        "input_price_per_1m": 3.00,
        "output_price_per_1m": 15.00,
        "benchmarks": {"mmlu": 88.7, "humaneval": 92.0, "gpqa": 59.4, "math": 78.3},
    },
    "claude-3-haiku": {
        "name": "Claude 3 Haiku",
        "provider": "Anthropic",
        "context_window": 200_000,
        "input_price_per_1m": 0.25,
        "output_price_per_1m": 1.25,
        "benchmarks": {"mmlu": 75.2, "humaneval": 75.9, "gpqa": 33.3, "math": 38.9},
    },
    "gemini-1-5-pro": {
        "name": "Gemini 1.5 Pro",
        "provider": "Google",
        "context_window": 2_000_000,
        "input_price_per_1m": 1.25,
        "output_price_per_1m": 5.00,
        "benchmarks": {"mmlu": 85.9, "humaneval": 84.1, "gpqa": 46.2, "math": 67.7},
    },
    "gemini-2-0-flash": {
        "name": "Gemini 2.0 Flash",
        "provider": "Google",
        "context_window": 1_000_000,
        "input_price_per_1m": 0.10,
        "output_price_per_1m": 0.40,
        "benchmarks": {"mmlu": 83.2, "humaneval": 82.6, "gpqa": 43.1, "math": 64.2},
    },
    "llama-3-1-405b": {
        "name": "Llama 3.1 405B",
        "provider": "Meta",
        "context_window": 128_000,
        "input_price_per_1m": 3.00,
        "output_price_per_1m": 3.00,
        "benchmarks": {"mmlu": 87.3, "humaneval": 89.0, "gpqa": 51.1, "math": 73.8},
    },
    "mistral-large": {
        "name": "Mistral Large",
        "provider": "Mistral",
        "context_window": 128_000,
        "input_price_per_1m": 2.00,
        "output_price_per_1m": 6.00,
        "benchmarks": {"mmlu": 84.0, "humaneval": 82.7, "gpqa": 45.3, "math": 69.1},
    },
    "deepseek-v3": {
        "name": "DeepSeek V3",
        "provider": "DeepSeek",
        "context_window": 128_000,
        "input_price_per_1m": 0.27,
        "output_price_per_1m": 1.10,
        "benchmarks": {"mmlu": 87.1, "humaneval": 82.6, "gpqa": 59.1, "math": 90.2},
    },
    "command-r-plus": {
        "name": "Command R+",
        "provider": "Cohere",
        "context_window": 128_000,
        "input_price_per_1m": 2.50,
        "output_price_per_1m": 10.00,
        "benchmarks": {"mmlu": 75.7, "humaneval": 70.1, "gpqa": 33.8, "math": 48.5},
    },
}

_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "mmlu": {
        "name": "MMLU",
        "full_name": "Massive Multitask Language Understanding",
        "description": (
            "Tests knowledge across 57 subjects including STEM, "
            "humanities, and social sciences."
        ),
        "scale": {"min": 0, "max": 100},
    },
    "humaneval": {
        "name": "HumanEval",
        "full_name": "HumanEval Code Generation",
        "description": (
            "Measures functional correctness of code generated "
            "from docstrings (164 problems)."
        ),
        "scale": {"min": 0, "max": 100},
    },
    "gpqa": {
        "name": "GPQA",
        "full_name": "Graduate-Level Google-Proof Q&A",
        "description": (
            "PhD-level questions in biology, physics, and chemistry "
            "designed to resist web search."
        ),
        "scale": {"min": 0, "max": 100},
    },
    "math": {
        "name": "MATH",
        "full_name": "Mathematics Problem Solving",
        "description": (
            "Competition-level mathematics problems spanning "
            "algebra through calculus."
        ),
        "scale": {"min": 0, "max": 100},
    },
}

_PROVIDERS: Dict[str, Dict[str, Any]] = {
    "openai": {
        "name": "OpenAI",
        "website": "https://openai.com",
        "models": ["gpt-4o", "gpt-4o-mini"],
    },
    "anthropic": {
        "name": "Anthropic",
        "website": "https://anthropic.com",
        "models": ["claude-3-5-sonnet", "claude-3-haiku"],
    },
    "google": {
        "name": "Google",
        "website": "https://ai.google.dev",
        "models": ["gemini-1-5-pro", "gemini-2-0-flash"],
    },
    "meta": {
        "name": "Meta",
        "website": "https://llama.meta.com",
        "models": ["llama-3-1-405b"],
    },
    "mistral": {
        "name": "Mistral",
        "website": "https://mistral.ai",
        "models": ["mistral-large"],
    },
    "deepseek": {
        "name": "DeepSeek",
        "website": "https://deepseek.com",
        "models": ["deepseek-v3"],
    },
    "cohere": {
        "name": "Cohere",
        "website": "https://cohere.com",
        "models": ["command-r-plus"],
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_model(slug: str) -> Optional[Dict[str, Any]]:
    """Look up a model by its slug.

    Args:
        slug: Model identifier (e.g. ``"gpt-4o"``, ``"claude-3-5-sonnet"``).

    Returns:
        Model data dictionary or ``None`` if not found.

    Example::

        >>> import benchgecko as bg
        >>> model = bg.get_model("claude-3-5-sonnet")
        >>> model["name"]
        'Claude 3.5 Sonnet'
        >>> model["benchmarks"]["mmlu"]
        88.7
    """
    model = _MODELS.get(slug)
    if model is None:
        return None
    return {"slug": slug, **model}


def compare_models(slug_a: str, slug_b: str) -> Dict[str, Any]:
    """Compare two models side-by-side across all tracked benchmarks.

    Args:
        slug_a: First model slug.
        slug_b: Second model slug.

    Returns:
        Comparison dict with per-benchmark deltas and a cost ratio.

    Raises:
        KeyError: If either model slug is not found.

    Example::

        >>> import benchgecko as bg
        >>> cmp = bg.compare_models("gpt-4o", "claude-3-5-sonnet")
        >>> cmp["benchmarks"]["humaneval"]
        {'a': 90.2, 'b': 92.0, 'delta': -1.8, 'winner': 'claude-3-5-sonnet'}
    """
    a = _MODELS.get(slug_a)
    b = _MODELS.get(slug_b)
    if a is None or b is None:
        missing = slug_a if a is None else slug_b
        raise KeyError(
            f"Model not found: {missing}. Use list_models() for available slugs."
        )

    benchmarks: Dict[str, Dict[str, Any]] = {}
    all_keys = set(a["benchmarks"]) | set(b["benchmarks"])
    for key in sorted(all_keys):
        va = a["benchmarks"].get(key)
        vb = b["benchmarks"].get(key)
        delta = None
        winner = None
        if va is not None and vb is not None:
            delta = round(va - vb, 2)
            winner = slug_a if delta > 0 else (slug_b if delta < 0 else "tie")
        benchmarks[key] = {"a": va, "b": vb, "delta": delta, "winner": winner}

    cost_a = a["input_price_per_1m"] + a["output_price_per_1m"]
    cost_b = b["input_price_per_1m"] + b["output_price_per_1m"]
    cost_ratio = round(cost_a / cost_b, 3)

    return {
        "model_a": {"slug": slug_a, "name": a["name"], "provider": a["provider"]},
        "model_b": {"slug": slug_b, "name": b["name"], "provider": b["provider"]},
        "benchmarks": benchmarks,
        "pricing": {
            "a": {"input": a["input_price_per_1m"], "output": a["output_price_per_1m"]},
            "b": {"input": b["input_price_per_1m"], "output": b["output_price_per_1m"]},
            "cost_ratio": cost_ratio,
            "cheaper_model": slug_a if cost_ratio < 1 else (slug_b if cost_ratio > 1 else "equal"),
        },
    }


def get_pricing(provider: str) -> List[Dict[str, Any]]:
    """Get pricing details for all models from a given provider.

    Args:
        provider: Provider key (e.g. ``"openai"``, ``"anthropic"``).

    Returns:
        List of pricing dictionaries.

    Raises:
        KeyError: If the provider is not found.

    Example::

        >>> import benchgecko as bg
        >>> for m in bg.get_pricing("anthropic"):
        ...     print(f"{m['name']}: ${m['input_price_per_1m']}/M in")
        Claude 3.5 Sonnet: $3.0/M in
        Claude 3 Haiku: $0.25/M in
    """
    key = provider.lower()
    p = _PROVIDERS.get(key)
    if p is None:
        raise KeyError(
            f"Provider not found: {provider}. "
            f"Available: {', '.join(sorted(_PROVIDERS))}"
        )
    result = []
    for slug in p["models"]:
        m = _MODELS[slug]
        result.append({
            "slug": slug,
            "name": m["name"],
            "input_price_per_1m": m["input_price_per_1m"],
            "output_price_per_1m": m["output_price_per_1m"],
            "context_window": m["context_window"],
        })
    return result


def list_benchmarks() -> List[Dict[str, Any]]:
    """List every tracked benchmark with its metadata.

    Returns:
        List of benchmark descriptor dictionaries.

    Example::

        >>> import benchgecko as bg
        >>> for b in bg.list_benchmarks():
        ...     print(f"{b['name']}: {b['description']}")
    """
    return [{"key": k, **v} for k, v in sorted(_BENCHMARKS.items())]


def list_models() -> List[str]:
    """List all available model slugs.

    Returns:
        Sorted list of model slug strings.
    """
    return sorted(_MODELS)


def list_providers() -> List[str]:
    """List all available provider keys.

    Returns:
        Sorted list of provider key strings.
    """
    return sorted(_PROVIDERS)


def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> Dict[str, Any]:
    """Estimate the cost of a single inference call.

    Args:
        model: Model slug.
        input_tokens: Number of input (prompt) tokens.
        output_tokens: Number of output (completion) tokens.

    Returns:
        Dictionary with ``input_cost``, ``output_cost``, and ``total_cost``
        in USD.

    Raises:
        KeyError: If the model slug is not found.

    Example::

        >>> import benchgecko as bg
        >>> cost = bg.estimate_cost("gpt-4o", input_tokens=2000, output_tokens=500)
        >>> cost["total_cost"]
        0.01
    """
    m = _MODELS.get(model)
    if m is None:
        raise KeyError(
            f"Model not found: {model}. Use list_models() for available slugs."
        )
    input_cost = round((input_tokens / 1_000_000) * m["input_price_per_1m"], 6)
    output_cost = round((output_tokens / 1_000_000) * m["output_price_per_1m"], 6)
    total_cost = round(input_cost + output_cost, 6)

    return {
        "model": model,
        "provider": m["provider"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "currency": "USD",
    }
