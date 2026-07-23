# Reproduction

```sh
uv sync --group dev
uv run zero-forcing-petersen-k4-check
```

The command compiles the auditable fixed-weight necklace census, replays orders \(17\) through
\(22\), replays the uniform upper schedule through order 200, and compares the result with
[artifacts/certificate-summary.json](artifacts/certificate-summary.json).

Quality gates:

```sh
uv run --group dev pytest
uv run --group dev ruff check .
uv run --group dev ruff format --check .
uv run --group dev mypy
uv lock --check
```

The tests independently:

- derive the expected cyclic-orbit totals from Burnside's lemma;
- reproduce the complete \(n=9\) native transcript in Python;
- check the frozen counts and SHA-256 transcript digests for \(17\le n\le22\);
- verify the \(n=17\) forcing control directly; and
- replay the parameterized upper schedule at boundary and distant orders.
