# Exceptional Laplacian hooks through eleven deletions

For every odd \(n\ge9\), write \(n=2r+1\) and
\(\lambda=(r+1,1^r)\). This package proves that the
\(\lambda\)-Laplacian immanantal polynomial determines every \(K_n-H\)
with \(|E(H)|\le11\).

Eight normalized coefficients suffice uniformly, and eight is minimal.
The exact stable census has 22,093 complement types and 244,039,278 pairs.

See [REPORT.md](REPORT.md) for the proof and [CERTIFICATE.md](CERTIFICATE.md)
for the replay contract.

## Replay

```sh
uv lock --check
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run laplacian-hook-eleven-check
```
