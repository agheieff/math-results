# Exact \(n=20\) signed-circulant gate

This lane checks the first case not covered by the computation reported in
[arXiv:2607.18334v1](https://arxiv.org/abs/2607.18334).

## Frozen statement

Let \(C_{20}(1,2)\) have vertex set \(\mathbb Z/20\mathbb Z\) and edges
\(\{i,i+1\}\) and \(\{i,i+2\}\). For a signing
\(\sigma:E\to\{-1,1\}\), let \(A_\sigma\) be its signed adjacency matrix. Then

\[
\min_\sigma \rho(A_\sigma)
=2\sqrt{\cos^2(\pi/20)+\cos^2(\pi/10)}.
\]

The exact exhaustion proves this statement and finds exactly the two twisted
switching classes described by the source paper. It does **not** prove the
paper's conjecture for all even \(n\).

## Certificate

The path edges \(01,12,\ldots,18\,19\) are switched positive. The remaining
Hamilton edge and twenty step-2 edges give \(21\) bits, hence exactly
\(2^{21}=2{,}097{,}152\) switching classes.

For every non-twisted class, the checker constructs an integer vector \(x\)
with

\[
\frac{\lVert A_\sigma x\rVert^2}{\lVert x\rVert^2}>\frac{38}{5}
>
4\left(\cos^2(\pi/20)+\cos^2(\pi/10)\right).
\]

The two remaining matrices are checked independently by an exact
characteristic-polynomial computation. See [REPORT.md](REPORT.md) and
[CERTIFICATE.md](CERTIFICATE.md); the separate reproduction is recorded in
[RED_TEAM.md](RED_TEAM.md).

## Run

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run signed-circulant-check
```
