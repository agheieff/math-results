# Generalized Petersen transfer lemmas

For every \(k\ge1\), this package proves:

\[
Z(P(n,k))\le 2k+2\qquad(n\ge2k+1),
\]

and

\[
P(n-k,k)\preccurlyeq P(n,k)\qquad(n\ge3k+1).
\]

The first statement has an explicit force-by-force schedule. The second is a topological-minor
construction obtained by deleting \(k\) spokes and suppressing \(2k\) degree-two vertices.
Together they reduce an eventual exact zero-forcing theorem at fixed \(k\) to \(k\)
consecutive pathwidth lower certificates.

Replay the finite regression certificate with:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-general-transfer-check
```

The infinite scope comes from the symbolic proofs in `THEOREM.md`; the replay grid is an
independent implementation check.
