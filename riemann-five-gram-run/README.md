# Five ordinary Gram points between consecutive zeta zeros

Hiary's Turing-checked table near

\[
T=10121598453421191913984785
\]

contains a consecutive critical-zero gap with exactly five ordinary Gram
points. Their real-zeta signs are

\[
+,-,+,-,+.
\]

This package freezes the source hashes and witness rows and independently
recomputes the Riemann--Siegel theta classification.

```console
uv sync --all-groups
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run riemann-five-gram-check
```

See [RESULT.md](RESULT.md) for the statement, calculation, sources, and scope.
