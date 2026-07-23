# Balanced separators in \(P(n,4)\)

This package proves that every \(n\)-vertex subset of \(P(n,4)\), for \(n\ge23\), has at
least ten vertices adjacent to its complement. The threshold is exact: a displayed half-set
of \(P(22,4)\) has internal boundary nine.

The proof combines an exact 1,481-state transfer computation for \(23\le n\le162\) with a
clean-run deletion reducing every hypothetical larger counterexample by two columns.
Together with the exact finite bridge in
[`../zero-forcing-petersen-k4`](../zero-forcing-petersen-k4/README.md) and its uniform
ten-vertex forcing set, this proves

\[
Z(P(n,4))=10\qquad(n\ge18).
\]

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-k4-separator-check
```

See [THEOREM.md](THEOREM.md) for the proof and [AUDIT.md](AUDIT.md) for the certificate
semantics.
