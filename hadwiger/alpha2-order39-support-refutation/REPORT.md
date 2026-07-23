# Superseded inconclusive checkpoint

The first corrected cut run found eleven locally feasible support multisets,
rejected all eleven by exact Hall separation, accumulated 298 valid cuts, and
then returned solver status `UNKNOWN` after 120 seconds on iteration 12.

That run remains recorded in `artifacts/corrected-run.txt`. Its implementation
also corrected an earlier disjoint-triple enumeration bug: both independent
enumerations found exactly 4,900 triples of pairwise-disjoint support types.

The `UNKNOWN` status was never evidence of infeasibility. A later exact local
switch search found the Hall-feasible support certificate in
[REFUTATION.md](REFUTATION.md), so this checkpoint is now superseded.

The old standalone script had SHA-256:

```text
7479edff78201ea10bf357edd75f4f425f2e2f3b64d02d31a07899fd047be07a
```
