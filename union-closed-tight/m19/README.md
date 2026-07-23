# Clean-tight union-closed gate at exactly 19 members

This package certifies the finite statement:

> No clean tight union-closed family of exactly 19 distinct subsets exists on
> an eight-element ground set.

The deterministic CNF is UNSAT. A trimmed binary DRAT proof and a textual LRAT
proof are retained, hashed, and independently replayed. The CNF SHA-256 is
`65e77adfc1c4114a5e6f86f322b183dcc4301f0d85000f612f61695992314ec7`.

See [REPORT.md](REPORT.md) for the semantic audit, exact encoding, proof chain,
hashes, scope, and reproduction commands.

Quick verification:

```sh
uv sync --all-groups
uv run uctight-m19 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check
```
