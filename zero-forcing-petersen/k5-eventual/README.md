# Eventual zero forcing for \(P(n,5)\)

This package proves

\[
\boxed{Z(P(n,5))=12\qquad(n\ge29).}
\]

Five exact balanced-separator computations give
\(\operatorname{pw}(P(n,5))\ge12\) at \(n=29,\ldots,33\). The five-column
topological-minor reduction propagates those residue classes indefinitely, and an explicit
12-vertex forcing schedule supplies the matching upper bound.

Replay with:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-k5-eventual-check
```

The native exact DP uses a C++20 compiler and may take about two minutes.
