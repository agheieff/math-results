# Corrected all-hook theorem

This directory verifies:

> For every \(n>7\), every \(1\le k\le n\), and every graph \(G\) obtained
> from \(K_n\) by deleting at most five edges, the Laplacian
> hook-immanantal polynomial for \((k,1^{n-k})\) determines \(G\) among all
> simple graphs.

This re-establishes the nonexceptional result claimed in Li--Wang,
arXiv:2607.19411v1, using the corrected three-cycle character, and also
settles their excluded line \(n=2k-1\).

```sh
uv sync --locked
uv run --locked laplacian-hook-all-check
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
```

The finite certificate covers all 46 complement types and all 1,035 pairs.
