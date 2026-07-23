# Clean-tight union-closed gate at exactly 16 members

This independent continuation lane tests one finite statement:

> No clean tight union-closed family of exactly 16 distinct subsets exists on an
> eight-element ground set.

The statement is **UNSAT**. Both a trimmed binary DRAT proof and a textual LRAT
proof are retained and independently replayed. The deterministic CNF has SHA-256
`9b1b28bf74ef19a77310e2c5dcdb1f98ba74e634e8ea33b5daea858e44645676`.

See [`REPORT.md`](REPORT.md) for the semantic audit, encoding, exact hashes,
resource bounds, and reproduction commands. The command line intentionally
exposes no other search size.

Quick verification:

```sh
uv sync --all-groups
uv run uctight-m16 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check
```
