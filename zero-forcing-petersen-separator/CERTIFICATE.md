# Reproduction

```sh
uv sync --group dev
uv run zero-forcing-petersen-separator-check
```

The compact frozen output is
[artifacts/certificate-summary.json](artifacts/certificate-summary.json).

Quality gates:

```sh
uv run --group dev pytest
uv run --group dev ruff check .
uv run --group dev ruff format --check .
uv run --group dev mypy
uv lock --check
```

The tests independently brute-force labeled half-sets at \(n=7,8,9\), replay the full transfer
range, verify the \(n=16\) counterexample, exercise the clean-run deletion, and compare the
frozen artifact with a fresh certificate.
