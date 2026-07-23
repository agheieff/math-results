# Zero forcing on the bi-infinite Petersen strip

This package proves a structural theorem adjacent to, but strictly weaker than, the open
conjecture \(Z(P(n,3))=8\) for every finite \(n\ge13\).

Let \(\mathcal P_3\) have vertices \(u_i,v_i\) for \(i\in\mathbb Z\), with edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+3}.
\]

Under the finite-initial-set, finite-time-per-vertex convention,

\[
\boxed{Z_{\mathrm{fin}}(\mathcal P_3)=8.}
\]

The lower bound is an exact eight-dimensional adjacency-kernel obstruction. The upper bound
uses eight consecutive outer vertices and an explicit two-sided propagation lemma.

The package also proves \(P(n-3,3)\) is a minor of \(P(n,3)\) for every \(n\ge10\). Neither
result transfers the lower bound to finite cyclic quotients by itself, and this package does
not claim the finite conjecture.

## Replay

```sh
uv lock --check
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-infinite-check
```
