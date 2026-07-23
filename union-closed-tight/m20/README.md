# Clean-tight union-closed gate at exactly 20 members

This package certifies the finite statement:

> No clean tight union-closed family of exactly 20 distinct subsets exists on
> an eight-element ground set.

The deterministic CNF is UNSAT. A trimmed binary DRAT proof and a textual LRAT
proof are retained, hashed, and independently replayed. The CNF SHA-256 is
`bf3bf0267d86d737cb40b45ad6d0b5bb2bd68e3c18f3c1c46e3f451e9767c300`.

See [REPORT.md](REPORT.md) for the semantic audit, exact encoding, proof chain,
hashes, scope, and reproduction commands.

Quick verification:

```sh
uv sync --all-groups
uv run uctight-m20 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check
```
