# Maximal graphs avoiding \(k+1\) spanning-tree packings

This directory records a short proof of Wang--Tian Conjecture 1, immediately
preceding Theorem 3.8 in [arXiv:2606.28198v1](https://arxiv.org/abs/2606.28198).

## Frozen theorem

Let \(k\ge 1\) and \(n\ge 2k+2\). If a finite simple \(n\)-vertex graph \(G\)
contains no subgraph with \(k+1\) edge-disjoint spanning trees, but adding any
missing edge creates such a subgraph, then

\[
|E(G)|=(k+1)(n-1)-1.
\]

The proof identifies the admissible edge sets with the independent sets of the
\((k+1,k+2)\)-sparsity matroid restricted to the simple complete graph. Maximal
admissible graphs are therefore bases. An explicit tight simple graph determines
the restricted rank. See [REPORT.md](REPORT.md) for the complete argument and
[PRIOR_ART.md](PRIOR_ART.md) for the source audit.

## Check

The checker independently compares:

1. the sparsity inequalities; and
2. the original spanning-tree-packing condition, tested by exhaustive
   Nash--Williams--Tutte partition checks on every vertex subset.

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run tau-k-check
```

The default exhaustive instances are \((q,n)=(2,4),(2,5),(2,6),(3,6)\), where
\(q=k+1\).
