# All-\(k\) exact half-boundary family

For every \(k,m\ge3\), this package constructs an explicit half-set
\(X\subseteq V(P(km,k))\) with

\[
|\partial_X X|=2m.
\]

Taking \(m=k\) gives infinitely many graphs \(P(k^2,k)\) with half-boundary \(2k\).
For every \(k\ge6\), \(k^2\ge6k-1\), so this is an infinite exact refutation of the
proposed uniform bound \(2k+2\) beyond that order threshold.

Replay with:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-all-k-boundary-family-check
```
