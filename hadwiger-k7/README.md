# K7-minor-free 7-colour lane

The rung-4 parent target is:

> Every finite simple graph with no \(K_7\) minor is 7-colourable.

This lane does **not** prove or refute that target. It records an authoritative-frontier audit,
the minimal-counterexample reductions, and an exact counterexample to the first frozen local lemma.
See `RECONNAISSANCE.md` for the mathematical scope, `PRIOR_ART.md` for the source audit, and
`RED_TEAM.md` for the independent reconstruction.

Reproduce the finite check:

```sh
uv sync --dev
uv run hadwiger-k7-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```
