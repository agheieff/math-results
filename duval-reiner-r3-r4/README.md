# Duval--Reiner \(r=3,4\) small-order census

For every 3-uniform family on at most six vertices, this package exactly verifies

\[
s_3(F)\leq D_3(F),\qquad s_4(F)\leq D_4(F).
\]

The six-vertex universe has \(2^{20}=1,048,576\) labeled families and 2,136 classes under
vertex relabeling. All classes are certified from integer characteristic polynomials using
exact rational root isolation or exact factor traces; floating-point eigenvalues only rank
screening cases.

No counterexample occurs:

| Index | Equality classes | Strict classes |
|---|---:|---:|
| \(r=3\) | 510 | 1,626 |
| \(r=4\) | 315 | 1,821 |

This does not settle either universal inequality. Seven vertices already has
34,359,738,368 labeled families and exactly 7,013,320 isomorphism classes, beyond the
implemented exhaustive generator.

```sh
uv run duval-reiner-r3-r4-check
```

See [REPORT.md](REPORT.md) for the exact gate, [SEARCH.md](SEARCH.md) for its boundary, and
[CERTIFICATE.md](CERTIFICATE.md) for reproduction.
