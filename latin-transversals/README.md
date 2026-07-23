# Explicit transversals for the Ghafari--Wanless squares

This lane checks the near-cyclic squares in
[Ghafari--Wanless, arXiv:2607.17547](https://arxiv.org/abs/2607.17547) and
gives explicit transversals in their `H_n` family.

Main result: if `n = 4k`, where `k >= 9` is odd, four parameterized
transversals of `H_n` have empty intersection. Together with Lemma 8 of the
paper, this proves Conjecture 3 for every `n = 4 (mod 8)`, `n >= 36`, with no
upper bound.

```bash
uv run pytest -q
uv run ruff check .
uv run mypy
```

The formulas and exact verifier are in
[`explicit.py`](src/latin_transversals/explicit.py). The proof is summarized
in [`REPORT.md`](REPORT.md); full affine audit tables are in
[`CERTIFICATES.md`](CERTIFICATES.md), and the current novelty check is in
[`PRIOR_ART.md`](PRIOR_ART.md).

[`G38_NOTE.md`](G38_NOTE.md) records a separate counterexample to one
intermediate claim in the source paper; it does not refute the paper's main theorem.
