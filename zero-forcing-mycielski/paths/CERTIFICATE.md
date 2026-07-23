# Exact checker

The checker independently performs four finite duties:

1. constructs \(M(P_n)\) directly from the edge definition;
2. replays the displayed three-vertex forcing sequence;
3. checks every two-vertex initial set in the requested finite range;
4. verifies the three disjoint forts at \(n=3,5\) and the selected path
   eigenvalue identities in the generic cases.

Run:

```sh
uv run zero-forcing-mycielski-paths-check --maximum-order 16
```

The finite sweep is corroboration. The all-\(n\) lower bound is the
symmetric-matrix argument and the two fort certificates in
[THEOREM.md](THEOREM.md).
