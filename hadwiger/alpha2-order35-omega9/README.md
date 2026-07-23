# Hadwiger, order 35, clique-nine obstruction

Frozen result:

> The natural assertion that every locally admissible order-35
> clique-nine configuration contains an outside edge dominating the
> fixed \(K_9\) is false.

[REFUTATION.md](REFUTATION.md) gives a 35-vertex countercertificate
which satisfies the known local properties of a hypothetical minimum
counterexample, including factor-criticality, 25-connectivity, and
18-contraction-criticality. It has no required core-dominating edge.

The same graph has an explicit spanning \(K_{18}\)-model. Thus this is a
refutation of a proof lemma, not a counterexample to Hadwiger's
conjecture, and it does not settle the general clique-nine branch.

The dependency-free checker reconstructs the graph from its support
system and verifies all claims exactly.

Run:

```sh
uv sync --dev
uv run hadwiger-alpha2-order35-omega9-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```
