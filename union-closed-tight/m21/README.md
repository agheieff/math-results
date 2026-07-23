# Clean-tight union-closed gate at exactly 21 members

This package certifies:

> No clean tight union-closed family of exactly 21 distinct subsets exists on
> an eight-element ground set.

The deterministic CNF is UNSAT. Retained DRAT and LRAT certificates are
hashed, compressed, and independently replayable. See [REPORT.md](REPORT.md)
for the encoding, proof chain, scope, and exact hashes.

Quick verification:

```sh
uv sync --all-groups
uv run uctight-m21 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check
```
