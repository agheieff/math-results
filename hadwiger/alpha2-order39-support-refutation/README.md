# Order-39 local support implication — REFUTED

This directory contains an exact 39-vertex countercertificate showing that
the listed local structural consequences at the \(\omega(G)=10\) frontier do
not imply the existence of an outside edge dominating a fixed ten-clique.

The reconstructed graph has \(\alpha(G)=2\), \(\omega(G)=10\),
\(\chi(G)=20\), factor-critical complement, \(\kappa(G)=28\),
20-contraction-criticality, and no dominating edge. Nevertheless, no edge
outside the fixed ten-clique dominates that clique.

This refutes the implication from those local properties and hence that
support-only proof route. It does not refute a stronger lemma which retains
\(K_{20}\)-minor-freeness as a hypothesis, and it does not refute Hadwiger's
conjecture. The same graph has an explicit spanning \(K_{20}\)-model. See
[REFUTATION.md](REFUTATION.md).

[PRIOR_ART.md](PRIOR_ART.md) records the reduction context, including the
recent Scully--Song preprint. The finite countercertificate itself is
independent of that preprint.

Run:

```sh
uv sync --dev
uv run hadwiger-alpha2-order39-support-search-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```

The older cut search remains available as
`uv run hadwiger-alpha2-order39-support-search`; its certificate hint now
reaches a Hall-feasible model. The radius-seven breadth-first search is
reproducible with `uv run hadwiger-alpha2-order39-support-switch-search`.
