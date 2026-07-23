# Hadwiger, \(\alpha=2\), \(\chi=7\): the 13-vertex base case

Frozen statement:

> Every 13-vertex graph \(G\) with \(\alpha(G)\leq 2\) and
> \(\chi(G)=7\) contains a \(K_7\) minor.

Equivalently, if \(F=\overline G\), then \(F\) is triangle-free,
\(\nu(F)=6\), and \(\overline F\) contains a \(K_7\) minor.

The proof in [PROOF.md](PROOF.md) is non-computational. It reduces a hypothetical
minimal counterexample to a \(K_4\) and three disjoint dominating seagulls, using
Chudnovsky--Seymour's seagull-packing theorem.

The executable verifier performs two finite checks used to keep the reduction honest:

- it implements the complement-side matching criterion and validates the returned
  \(K_4\)-plus-three-seagull branch sets on the complement of \(C_{13}\);
- \(F=K_{6,7}\) is an exact counterexample to the tempting stronger reduction to
  six paired branch sets and one leftover singleton, even though
  \(\overline F=K_6\mathbin{\dot\cup}K_7\) contains \(K_7\).

Run:

```sh
uv sync --dev
uv run hadwiger-alpha2-chi7-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```
