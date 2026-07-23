# Independent audit

Audit date: 2026-07-23.

## Verdict

The theorem and certificates pass. One tooling defect was found and fixed:
the advertised bare `uv run mypy` command initially had no target. The
configuration now checks `src` and `tests` in strict mode.

## Forcing sequence

Starting from \(\{v_0,v_1,u_0\}\), the first four forces leave

\[
\{v_0,v_1,v_2,u_0,u_1,u_2,w\}
\]

black. Inductively, before the pair indexed by \(i\), all \(v_j,u_j\) with
\(j\le i\), together with \(w\), are black. Then \(u_i\) has the unique white
neighbor \(v_{i+1}\), after which \(v_i\) has the unique white neighbor
\(u_{i+1}\). This proves the displayed sequence for every \(n\ge3\), including
the empty induction range at \(n=3\).

A separate edge-list implementation replayed the sequence for
\(3\le n\le100\).

## Exceptional forts

For \(n=3,5\), the path endpoints are even-indexed. In the three listed sets:

- outside vertices see either zero or two members of the even-original fort;
- outside vertices see zero, two, or at least three members of the
  even-shadow fort, with the apex seeing all even shadows; and
- an outside even original sees two or four members of the odd/apex fort,
  while an outside even shadow sees two or three.

Thus every outside vertex has a fort-neighbor count different from one. The
three forts are pairwise disjoint and cover all vertices, so every zero
forcing set has size at least three. A separate implementation checked all
outside-neighbor counts directly at both orders.

## Symmetric-matrix certificate

On a \(\lambda\)-eigenspace of the path adjacency matrix, \(H\) reduces to

\[
B_\lambda=
\begin{pmatrix}a+b\lambda&\lambda\\ \lambda&1\end{pmatrix},
\qquad
\det B_\lambda=-(\lambda-r)(\lambda-s).
\]

The lower-right entry is \(1\), so the blocks at \(r=\lambda_2\) and
\(s=\lambda_4\) have rank one, not zero. All other blocks are invertible.
Since the path spectrum is simple, \(\operatorname{null}H=2\) exactly.

The only generic-order support exception is \(b=r+s=0\). The identity

\[
b=4\cos\frac{3\pi}{n+1}\cos\frac{\pi}{n+1}
\]

shows that for \(n\ge4\) this occurs exactly at \(n=5\). Hence every required
original-path off-diagonal entry is nonzero outside the stated exception.
The \(P\) cross-block gives exactly the original--shadow edges, and
\(g=(0,\boldsymbol1)^\mathsf T\) gives exactly the apex--shadow edges.
All remaining nonedge off-diagonal entries vanish.

For even \(k\), reflection pairs the path eigenvector coordinates with
opposite signs; a possible midpoint coordinate is zero. Therefore
\(\boldsymbol1^\mathsf T x^{(k)}=0\) for \(k=2,4\), and \(g\) is orthogonal
to both kernel modes \((x^{(k)},-\lambda_kx^{(k)})\). Symmetry then gives
\(g\in\operatorname{im}H\).

If \(Hz=g\) and \(f=g^\mathsf Tz\), every solution of

\[
\begin{pmatrix}H&g\\g^\mathsf T&f\end{pmatrix}
\binom{x}{t}=0
\]

has \(x=-tz+k\) with \(k\in\ker H\). Conversely every such pair is a
solution. The extended matrix consequently has nullity exactly \(3\).

Independent floating-point rank, kernel-residual, apex-orthogonality, and
off-diagonal-support checks passed for every nonexceptional \(4\le n\le30\)
and for \(n=40,60\).

## Replay

The following all pass:

```sh
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-mycielski-paths-check --maximum-order 80
```

There are seven passing tests, and the CLI reports `PASS` for every order
from \(2\) through \(80\).
