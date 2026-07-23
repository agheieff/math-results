# Hadwiger with independence two through order 38

Frozen statement:

> Every graph \(G\) with \(\alpha(G)\leq2\) and at most 38 vertices
> satisfies Hadwiger's conjecture.

[PROOF.md](PROOF.md) closes the order-37 frontier. Its new ingredient is
a support-system argument producing two disjoint, mutually touching
edge branches that each dominate a fixed nine-clique. Those eleven core
branches leave 24 vertices, which Chudnovsky--Seymour's criterion packs
into eight seagulls, giving a \(K_{19}\) minor.

[DEPENDENCIES.md](DEPENDENCIES.md) records the proof graph and external
trust boundary. The checker verifies the finite arithmetic in the
support counts and the two remainder arguments; it does not formalize
the cited Ramsey number or seagull theorem.

Run:

```sh
uv sync --dev
uv run hadwiger-alpha2-order37-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```
