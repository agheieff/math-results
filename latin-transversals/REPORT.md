# Report: explicit transversals in `H_{4k}`

## Result

Let `k >= 9` be odd and `n = 4k`. The Ghafari--Wanless square `H_n` has four
explicit transversals with empty intersection. Hence it has no pinned entry.
Lemma 8 of their paper says that every transversal of `H_n` contains at least
two of

```text
A=(1,1,5), B=(6,5,14), C=(11,9,23),
```

so no two transversals are disjoint. Therefore Conjecture 3 holds for every

```text
n = 4 (mod 8), n >= 36,
```

without the paper's upper cutoff `n <= 10000` in this congruence class.

This appears to be new relative to arXiv:2607.17547v1, which explicitly says
that no general argument guaranteeing the required transversals was known.
It should still be treated as a new proof candidate until peer reviewed.

## Construction

Put

```text
u = (1,6,-2,3),
c0(r) = r + u[r mod 4] (mod n),
c1(r) = c0(r) + 4 (mod n).
```

Both `c0` and `c1` are column permutations. A donor cycle
`(r0,...,rm)` means that row `ri` takes the base column of `r(i+1)`.

Three finite repairs of `c0` give transversals `T_A,T_B,T_C`, where `T_X`
omits `X` and includes the other two forced entries. A finite repair of `c1`
gives a fourth transversal `T_A+`. The uniform cycles for odd `k >= 19` and
the five collision-boundary repairs are encoded verbatim in `explicit.py`.

The proof has four finite checks:

1. The donor cycles permute the base columns.
2. Direct substitution gives the rowwise maximum delta profile used in
   Lemma 8.
3. On the base `c0` diagonal, the excess and omitted symbol multisets are

   ```text
   D0={2,5,17,25,n-39,n-31,n-23,n-15,n-7},
   O0={3,11,19,27,n-37,n-29,n-21,n-13,n-5}.
   ```

   Each phase-zero repair removes exactly `D0` and inserts exactly `O0`.
   The analogous phase-one cancellation is recorded in `CERTIFICATES.md`.
4. Outside the finite cycle supports, `T_A,T_B,T_C` use `c0`, while `T_A+`
   uses `c1 != c0`. The only rows in the supports where the first three
   columns agree are listed in `CERTIFICATES.md`; `T_A+` differs at each.

For `k in {9,11,13,15,17}`, explicit donor cycles replace the colliding
uniform phase-zero cycles. The exact verifier checks rows, columns, symbols,
delta profiles, forced entries, and the empty four-way intersection.

A Lean formalization was not proportionate for these long piecewise affine tables. The
fallback requested in `PLAN.md` was used instead: two independently written exact verifiers,
the symbolic tables in `CERTIFICATES.md`, and a separate sweep through odd `k <= 4999`.

## Why the same bulk map stops at odd `k`

For generic rows, symbols under `c0` advance by `8` modulo `4k`. After
dividing by the fixed residue class this is multiplication by `2` modulo
`k`. It is invertible for odd `k`, leaving only nine boundary defects. For
even `k`, it has a kernel of size two and creates linearly many defects, so a
bounded donor repair cannot work. The remaining `n = 0 (mod 8)` case needs a
different bulk map, not a longer finite search.

## `G_n` and order 30

No all-orders formula was obtained for `G_n`. Its admissible delta profiles
are less rigid than those of `H_n`.

The paper's two displayed transversals in `G_30` were independently checked
and are disjoint. Thus the raw `G_n` construction cannot settle order 30;
that case needs a different Latin trade or a different square. No large
enumeration was used or proposed here.
