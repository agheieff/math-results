# Unique multiset sums in finite abelian groups

This directory records a sharp lower bound for the finite-abelian-group variant
posed in [arXiv:2607.08366v2](https://arxiv.org/abs/2607.08366v2) and
[arXiv:2607.09949v2](https://arxiv.org/abs/2607.09949v2).

## Result

Let \(g_0,\ldots,g_{n-1}\) lie in a finite abelian group \(G\), and suppose the
all-ones multiplicity vector is the only \(k\in\mathbb Z_{\ge0}^n\) satisfying

\[
\sum_i k_i=n,
\qquad
\sum_i k_i g_i=\sum_i g_i.
\]

Then

\[
|G|\ge 2^{n-1}.
\]

For every basepoint \(j\), validity forces the \(n-1\) differences
\(\{g_i-g_j:i\ne j\}\) to be dissociated: their \(2^{n-1}\) subset sums are
pairwise distinct. The bound is therefore immediate by counting. The family
\((0,e_1,\ldots,e_{n-1})\) in \((\mathbb Z_2)^{n-1}\) attains equality, so
\(2^{n-1}\) is the exact minimum group order.

This resolves Open Problem 4 of arXiv:2607.08366v2. In the cyclic case it gives
\(N\ge2^{n-1}\), but it does **not** prove the stronger conjectured bound
\(N\ge2^n-2^{\lfloor\log_2 n\rfloor}\).

The same numerical bound is also implicit in the 2011
Carlini--Catalisano--Geramita formula for the Waring rank of monomials, after
restricting the companion paper's evaluation identity to matrices with equal
rows. The contribution recorded here is the direct finite-group proof.

See [REPORT.md](REPORT.md) for the proof and [PRIOR_ART.md](PRIOR_ART.md) for
the version and novelty audit. [RED_TEAM.md](RED_TEAM.md) records an independent
proof and implementation review.

Status: verified mathematical result and resolution of the all-groups open
question. Public novelty and specialist review remain caveated; the cyclic
conjecture remains open.

## Check

The checker represents every finite abelian group by its primary cyclic
factors. It independently:

1. enumerates all size-\(n\) multiplicity vectors;
2. detects collisions among basepoint-difference subset sums;
3. converts each subset collision into an explicit forbidden multiplicity
   vector; and
4. exhausts all group isomorphism types and normalized \(n\)-element families
   below \(2^{n-1}\) for the requested small orders.

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run ums-check
```

The lower bound is also kernel-checked in Lean 4:

```sh
cd lean
lake update
lake build
lake env lean UniqueMultisetSum.lean
lake env lean CheckAxioms.lean
```

`UniqueMultisetSum.group_card_lower_bound` contains no `sorry`.
