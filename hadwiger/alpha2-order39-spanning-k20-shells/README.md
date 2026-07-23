# Order-39 spanning-\(K_{20}\) support search — ACTIVE

This lane investigates whether the explicit local order-39 support-system
properties force a spanning \(K_{20}\)-model with one singleton branch and
nineteen two-vertex branches.

The exact assertion and its boundary are frozen in
[ASSERTION.md](ASSERTION.md). No universal result has yet been established.

The exact bounded checkpoint in [REPORT.md](REPORT.md) exhausts the
multiplicity-\(L^1\) shells at distances four and six from the seed. It finds
nine Hall-valid endpoints; every one passes the frozen graph properties and
has an exact spanning model. This does not settle the universal assertion.

```console
uv sync --all-groups
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-shells
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-successors
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-successors-2
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-successors-3
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-successors-4
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-successors-5
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-successors-6
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-successors-7
nice -n 10 uv run hadwiger-alpha2-order39-spanning-k20-labeled-catchup
```
