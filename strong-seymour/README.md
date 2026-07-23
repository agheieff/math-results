# strong-seymour

Exact SAT search for a tournament with no strong Seymour vertex.

The checked result is that none exists through order 13. See `REPORT.md`.

```bash
uv sync
uv run ruff check src tests
uv run mypy src tests
uv run python -m unittest discover -s tests -v
uv run strong-seymour-search --order 13
```

Proof replay instructions are in `proof/verification.md`.

