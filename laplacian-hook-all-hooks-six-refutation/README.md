# Six-deletion all-hooks refutation

An extension asserting determination for every hook parameter after six edge
deletions is false. At \(k=1\), the hook character is the sign character, so

\[
\Phi_1(L(G),x)=\det(xI-L(G)).
\]

This package gives three classes of nonisomorphic six-edge complements whose
Laplacian spectra agree after arbitrary isolate padding. Their dense
complements are therefore \(k=1\)-indistinguishable for every \(n\ge8\).

See [REPORT.md](REPORT.md) for the exact witnesses.

## Replay

```sh
uv lock --check
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run laplacian-hook-six-refutation-check
```
