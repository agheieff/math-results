# Eventual zero forcing for \(P(n,6)\)

This package proves

\[
\boxed{Z(P(35,6))=14,\qquad Z(P(n,6))=14\quad(n\ge37).}
\]

The same exact computation proves the isolated order 35 and gives
\(\operatorname{pw}(P(n,6))\ge14\) at the six consecutive orders
\(37,\ldots,42\). A six-column topological-minor reduction propagates those residue
classes, and an explicit 14-vertex forcing schedule gives the matching upper bound.

Replay with:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-k6-eventual-check
```

The native exact DP requires a C++20 compiler, about 1 GiB of memory, and roughly two
minutes on the development machine.
