# Historical certificate checkpoint

This file preserves the state before proof replay. The full DRAT/LRAT chain
subsequently passed; [REPORT.md](REPORT.md) is authoritative.

Target:

\[
|X|=8,\qquad |\mathcal F|=22.
\]

The deterministic CNF has 17,792 variables, 231,118 clauses, 4,333,092 bytes,
and SHA-256
`572ef916a42a0da50c00aa8711462052b3eb77fe9f9b91e30a54082cff1b1c5f`.

An exploratory Kissat 4.0.4 run exited 20 after 292.57 process-seconds and
reported UNSAT. This is triage evidence only.

The proof-producing replay was started with:

```sh
nice -n 19 timeout --signal=TERM 1800s \
  /tmp/arcadia-kissat404/build/kissat --quiet \
  /tmp/order8-members22.cnf /tmp/order8-members22.raw.drat
```

If it exits 20, the remaining gates are:

1. hash and archive the raw DRAT;
2. replay and trim it with `drat-trim`;
3. replay retained DRAT;
4. convert to LRAT and replay with `lrat-check`;
5. retain compressed certificates and a manifest;
6. run the fresh public verifier and static gates.

At this historical checkpoint the lane remained active and was not eligible
for promotion.
