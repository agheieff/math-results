# Eventual zero forcing for \(P(n,7)\)

This package proves

\[
\boxed{Z(P(n,7))=16\quad(45\le n\le48\ \text{or}\ n\ge50).}
\]

An exact balanced-separator computation gives
\(\operatorname{pw}(P(n,7))\ge16\) at the seven consecutive orders
\(50,\ldots,56\), plus the isolated orders \(45,\ldots,48\). A seven-column
topological-minor reduction propagates the consecutive bases, and an explicit 16-vertex
forcing schedule gives the matching upper bound.

Replay with:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-k7-eventual-check
```

The native exact DP requires a C++20 compiler, about 8 GiB of memory, and roughly
15 minutes on the development machine.
