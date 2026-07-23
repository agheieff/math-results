# Hadwiger with independence two through order 34

Frozen statement:

> Every graph \(G\) with \(\alpha(G)\leq2\) and \(|V(G)|\leq34\)
> contains a \(K_{\chi(G)}\) minor.

The proof in [PROOF.md](PROOF.md) closes the next possible
minimum-counterexample order after the order-31 lane. At order 33, a
\(K_9-e\) supplies nine core branches. A new incidence lemma forces an
edge that dominates its seven-clique, allowing a ten-branch core and a
seven-seagull factor on the remaining 21 vertices. Since every
minimum-order counterexample has odd order, order 34 follows.

The executable checker audits the local finite obligations: the
common-neighbour count, the incidence lemma's sharp degree bounds, the
only possible five- and six-cut splits, the capacity and antimatching
arithmetic, and the final branch-set count. It does not reprove the cited
Ramsey number or Chudnovsky--Seymour's seagull theorem.

Run:

```sh
uv sync --dev
uv run hadwiger-alpha2-order33-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```
