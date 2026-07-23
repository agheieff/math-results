# Zero forcing for every \(P(n,3)\)

This package proves

\[
Z(P(n,3))=8\qquad\text{for every }n\ge13.
\]

The finite lower certificate at \(n=13\), the three exact pathwidth base certificates, the
three-column minor reduction, and the uniform upper witness can all be replayed with:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-petersen-all-orders-check
```

See `THEOREM.md` for the proof and `AUDIT.md` for the certificate semantics.
