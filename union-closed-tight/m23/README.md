# Clean-tight union-closed gate at exactly 23 members

This package certifies:

> No clean tight union-closed family of exactly 23 distinct subsets exists on
> an eight-element ground set.

The deterministic CNF is UNSAT. Retained DRAT and LRAT certificates are
hashed, compressed, and independently replayable. See [REPORT.md](REPORT.md)
for the encoding, proof chain, scope, and exact hashes.

Quick verification:

```sh
uv sync --all-groups
uv run uctight-m23 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check
```
