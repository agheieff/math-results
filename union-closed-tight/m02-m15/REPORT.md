# Bounded certificate for the clean-tight conjecture

Cutoff: 2026-07-23.

## Result

Let `X` have eight elements. Under the standing convention of van der Hout and Roos that the
empty set belongs to `F`, there is no family `F` satisfying all of the following:

- `2 <= |F| <= 15`;
- `F` is union-closed;
- `F` is tight: every element occurs in at most half of its members;
- `F` is clean: no element is idle and distinct elements have distinct incidence columns.

Thus Conjectures 6.1 and 6.3 hold in this bounded scope, vacuously: there is no clean tight family
to be a counterexample. Since `|F| < 256`, the power set of `X` is outside the search range.

Without the empty-set convention, the same nonexistence conclusion holds through `|F| = 14`.
Indeed, adjoining the empty set preserves union closure, cleanliness, and tightness, and increases
the family size by one.

No claim is made for `|F| >= 16`, for the complete eight-element case, for either full conjecture,
or for Frankl's union-closed sets conjecture.

## Match to the paper

The source paper defines tightness by `|F_x| <= |F| / 2` for every element. It calls two elements
equivalent when their incidence columns agree, calls the equivalence classes blocks, and calls a
family clean when all blocks are singletons and there are no idle elements. Conjecture 6.1 says a
clean tight union-closed family is a power set; Conjecture 6.3 says all its element frequencies are
exactly half. The authors report experiments for ground-set orders two through seven.

Source: [van der Hout and Roos, JANO 8 (2026), 11--18](https://doi.org/10.23952/jano.8.2026.1.02)
and its [published PDF](https://pure.tudelft.nl/ws/portalfiles/portal/282508754/JANO2026-1-2.pdf).

## Encoding and completeness

For each integer `m` from 2 through 15, a separate deterministic CNF has 17,792 variables and
231,118 clauses. Its first 256 variables are `p_A`, one for each subset `A` of `X`.

- Unit clauses require the empty and full sets. The full set is already a consequence of finite
  union closure and the no-idle condition; requiring it is therefore harmless.
- For every incomparable pair `A,B`, the clause `not p_A or not p_B or p_(A union B)` encodes
  union closure. Comparable pairs need no clause.
- A totalizer requires exactly `m` family members.
- Eight totalizers require each element frequency to be at most `floor(m / 2)`.
- For every element pair, one disjunction requires a selected set separating their incidence
  columns. The full-set unit excludes idle elements.
- Frequencies are constrained to nondecreasing order. This is a complete symmetry break: any
  candidate family can be relabeled by sorting its eight elements by frequency.

The independent predicate in `semantics.py` does not reuse CNF clauses. Tests exhaustively compare
it with the SAT encoding for every family on a three-element ground set and every possible family
size. All odd and even `m` are certified; no parity assumption is used.

## Certificate chain

The formulas use PySAT 1.9.dev7 totalizers. CaDiCaL 2.2.1 at commit
`4198d817d0dcde5b1240eefbff70b555b7df2af9` generated binary DRAT proofs. `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` then:

1. replayed every raw proof;
2. extracted a trimmed binary proof;
3. replayed every trimmed proof before compression.

After the build, all 14 retained XZ-compressed proofs were decompressed and replayed again against
freshly regenerated, hash-checked CNFs. Every case returned `s VERIFIED`.

As an independent second-format pass, the retained DRAT for every `m = 2,...,15` was converted to
LRAT by that `drat-trim` revision and checked by its separately compiled `lrat-check`; every case
returned `c VERIFIED`. LRAT files were temporary because they are much larger (the `m = 15`
working directory reached 417 MiB). The retained certificate directory is 37 MiB. Formula and
compressed-proof SHA-256 hashes are recorded in `certificates/manifest.json`.

## Novelty status

The exact-phrase and citation searches performed at the cutoff found the 2026 source paper but no
later public treatment of its new Conjectures 6.1--6.3. The paper itself reports computations only
through seven ground elements. This result is therefore best described as a reproducible candidate
new bounded extension to eight elements, not as a peer-reviewed novelty claim.

Lean formalization was not attempted: the mathematical reduction was checked independently in
code, and every finite UNSAT claim has both DRAT and LRAT replay evidence.

