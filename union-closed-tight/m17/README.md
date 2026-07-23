# Clean-tight union-closed gate at exactly 17 members

This package certifies the finite statement:

> No clean tight union-closed family of exactly 17 distinct subsets exists on
> an eight-element ground set.

The deterministic CNF is UNSAT. A trimmed binary DRAT proof and a textual LRAT
proof are retained, hashed, and independently replayed. The CNF SHA-256 is
`9814d5a35f5c447bc0f1733d6ba1cdb651abb4e4206442fd0546c660440b4b52`.

See [REPORT.md](REPORT.md) for the semantic audit, exact encoding, proof chain,
hashes, scope, and reproduction commands.

Quick verification:

```sh
uv sync --all-groups
uv run uctight-m17 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check
```
