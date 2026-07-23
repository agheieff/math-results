# Clean tight union-closed families on eight elements

Certified bounded result: under the paper's standing convention `empty in F`, there is no clean,
tight, union-closed family on eight elements with `2 <= |F| <= 15`.

This supports van der Hout--Roos Conjectures 6.1 and 6.3 only in that finite range. It does not
settle the full eight-element case, either conjecture, or Frankl's conjecture. See `REPORT.md`.

## Check

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run uctight verify --checker /path/to/drat-trim
```

For a second proof format, compile `lrat-check` from the same `drat-trim` checkout and run:

```sh
uv run uctight verify \
  --checker /path/to/drat-trim \
  --lrat-checker /path/to/lrat-check
```

The latter converts and checks one LRAT proof at a time in a temporary directory.

## Rebuild certificates

CaDiCaL writes binary DRAT; `drat-trim` checks and trims it before XZ compression.

```sh
uv run uctight certify \
  --solver /path/to/cadical \
  --checker /path/to/drat-trim
```

The checked artifacts and their CNF/proof SHA-256 hashes are in `certificates/`.

