# Reproduction

## Environment

```sh
uv sync --group dev
```

The exact certificate alone is fast and does not invoke CP-SAT:

```sh
uv run spherical-zero-sum-h3-check
```

Expected mathematical payload:

```json
{
  "h3": {
    "independence_number": 20,
    "ratio": "2/3",
    "vertices": 30,
    "zero_sum_triples": 20
  }
}
```

The bounded search takes roughly tens of seconds on a typical workstation:

```sh
uv run spherical-zero-sum-h3-check --full-search
```

Its frozen summary is [artifacts/search-summary.json](artifacts/search-summary.json).

## Verification

```sh
uv run --group dev pytest
uv run --group dev ruff check .
uv run --group dev ruff format --check .
uv run --group dev mypy
```

`field.py`, `roots.py`, and `h3.py` provide the exact
\(\mathbb Q(\phi)\) certificate. `geometry.py` and `search.py` form the numerical,
finite-family search layer. `optimizer.py` proves independence numbers for the recovered
hypergraphs by requiring an optimal CP-SAT result.

The exact claim is the \(H_3\) count and independence number. Search-family non-improvement is
reproducible but remains bounded and numerically recovered.
