# Hadwiger with independence two through order 32

Frozen statement:

> Every graph \(G\) with \(\alpha(G)\leq2\) and \(|V(G)|\leq32\)
> contains a \(K_{\chi(G)}\) minor.

The proof in [PROOF.md](PROOF.md) closes Carter's isolated order-31
frontier. Carter already proved that a minimal counterexample cannot have
order 32, so the resulting contiguous bound advances from 30 to 32. At
order 31, the exact Ramsey number \(R(3,K_9-e)=31\) supplies a
\(K_9-e\) core. A prescribed seagull and the Chudnovsky--Seymour packing
criterion then reduce the proof to a 21-vertex remainder. Its apparent
six-cut obstruction is impossible.

The executable checker exhausts the local finite obligations in that
reduction: the common-neighbour bound, the \(7+8\) cut split, all local
adjacency patterns at the lifted cut, the capacity arithmetic, the
antimatching bound, and the final branch-set count. It does not
reprove the cited Ramsey number or the Chudnovsky--Seymour theorem.

Run:

```sh
uv sync --dev
uv run hadwiger-alpha2-order31-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```
