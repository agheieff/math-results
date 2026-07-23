# Clean-tight union-closed gate at exactly 18 members

This package certifies the finite statement:

> No clean tight union-closed family of exactly 18 distinct subsets exists on
> an eight-element ground set.

The deterministic CNF is UNSAT. A trimmed binary DRAT proof and a textual LRAT
proof are retained, hashed, and independently replayed. The CNF SHA-256 is
`7663e2133354c68bfee72db4fc1841a1c5ea98060b739afd8bc68635ced6e05c`.

See [REPORT.md](REPORT.md) for the semantic audit, exact encoding, proof chain,
hashes, scope, and reproduction commands.

Quick verification:

```sh
uv sync --all-groups
uv run uctight-m18 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check
```
