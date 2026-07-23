# Historical certificate checkpoint

This file preserves the state at solver launch. The full DRAT/LRAT chain
subsequently passed; [REPORT.md](REPORT.md) is authoritative.

Target:

\[
|X|=8,\qquad |\mathcal F|=23.
\]

The deterministic CNF has 17,792 variables, 231,118 clauses, 4,333,092 bytes,
and SHA-256
`53339228c8bb4666bf973cb980dc15dffd2307180c5aeba5fe47a0d79a1659a1`.

Code gates passed before launch: 17 tests, Ruff check, Ruff format, strict
mypy, and byte-for-byte regenerated CNF identity.

The single proof-producing run started at
`2026-07-23T21:35:01.656764054+02:00`:

```sh
time -p nice -n 19 timeout --signal=TERM 1800s \
  /tmp/arcadia-kissat404/build/kissat --quiet \
  artifacts/order8-members23.cnf /tmp/order8-members23.raw.drat
```

At launch, the timeout PID was 477167 and the Kissat PID was 477176. The
executable is Kissat 4.0.4, commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, SHA-256
`43be6166b83812b19e4c83cbbc1536f2772c90c722b24c0d6635707512b45c0e`.

If the run exits 20 with exact output `s UNSATISFIABLE`, the remaining gates
are:

1. stabilize, hash, and archive the raw DRAT;
2. replay and trim it with `drat-trim`;
3. replay the retained DRAT;
4. convert it to LRAT and replay with `lrat-check`;
5. retain compressed certificates and a manifest;
6. run the fresh public verifier and final static gates.

At this historical checkpoint the lane remained active and was not a verified
result.
