# Exact order-eight, \(m=18\) report

## Result

There is no clean tight union-closed family of exactly 18 distinct subsets of
an eight-element ground set:

\[
|X|=8,\qquad |\mathcal F|=18.
\]

This is a certificate-backed verification of the single finite parameter
pair. Together with the separate packages for smaller cardinalities, it
extends the verified order-eight range through 18 members. It does not address
\(m\geq19\), other ground-set orders, or prove the general clean-tight or
union-closed sets conjecture.

This statement is not subsumed by merely ruling out Frankl counterexamples at
this gate. Since \(m\) is even, a tight family may have elements of frequency
exactly \(m/2=9\) and therefore need not be a Frankl counterexample.

## Independent semantic audit

The definitions were checked against van der Hout and Roos,
*Some results and conjectures related to Frankl's union closed conjecture*,
[JANO 8 (2026), 11--18](https://doi.org/10.23952/jano.8.2026.1.02).
The paper uses the standing convention \(\varnothing\in\mathcal F\), defines
tightness by

\[
|\mathcal F_x|\leq |\mathcal F|/2\quad\text{for every }x\in X,
\]

and calls a family clean when it has no idle elements and all incidence
blocks are singletons. Equivalently, every two elements have different
incidence columns.

The implementation checks:

1. exactly 18 distinct selected subsets, including \(\varnothing\);
2. closure under pairwise union;
3. frequency at most 9 for every element;
4. no idle element and pairwise-distinct incidence columns.

A finite union-closed family with no idle element contains \(X\): iterating
unions over all members gives their union, which is \(X\). Thus the CNF unit
forcing \(X\in\mathcal F\) encodes cleanliness without adding a restriction.

Element labels do not matter. Relabeling them by nondecreasing frequency gives
a canonical representative, so
\(\operatorname{freq}(0)\leq\cdots\leq\operatorname{freq}(7)\) is a complete
symmetry break.

The direct predicate in `semantics.py` does not inspect the CNF. Differential
tests compare it with SAT under every complete family assignment on a
three-element ground set, for every cardinality 2 through 8. The order-four
power set is also checked independently at the \(m=16\) boundary.

## Deterministic CNF

For each subset \(A\subseteq X\), membership variable \(p_A\) says
\(A\in\mathcal F\). Auxiliary variables come only from deterministic
totalizer cardinality encodings.

| Condition | Clauses |
|---|---|
| standing convention and no-idle consequence | \(p_\varnothing\), \(p_X\) |
| union closure | \(\neg p_A\lor\neg p_B\lor p_{A\cup B}\) for incomparable \(A,B\) |
| family size | \(\sum_Ap_A=18\) |
| tightness | \(\sum_{A\ni x}p_A\leq9\) for every \(x\) |
| canonical labels | adjacent nondecreasing-frequency constraints |
| clean columns | one separating selected set for every element pair |

For adjacent elements \(x,y\), the canonical-label totalizer has 128 input
literals and right-hand side 64:

\[
\sum_{A:x\in A,y\notin A}p_A+
\sum_{A:y\in A,x\notin A}(1-p_A)\leq64.
\]

This simplifies exactly to
\(\operatorname{freq}(x)\leq\operatorname{freq}(y)\).

The target DIMACS is deterministic:

- variables: `17792`
- clauses: `231118`
- bytes: `4333092`
- SHA-256:
  `7663e2133354c68bfee72db4fc1841a1c5ea98060b739afd8bc68635ced6e05c`

The complete fingerprint is pinned by a regression test.

## Certificate chain

Kissat produced an UNSAT binary DRAT proof. `drat-trim` replayed the raw proof
while extracting its core, then replayed the trimmed proof. A separate
conversion produced LRAT, which `lrat-check` accepted. Finally, the public
verification command regenerated the CNF, checked compressed and uncompressed
hashes and sizes, and replayed both retained artifacts from a fresh work
directory.

| Stage | Wall time |
|---|---:|
| Kissat UNSAT search | 282.57 s |
| raw DRAT replay and trimming | 298.19 s |
| retained DRAT replay | 212.73 s |
| DRAT-to-LRAT conversion | 212.71 s |
| LRAT replay | 9.24 s |

Each external search/check stage had an 1800-second timeout.

The original raw DRAT proof had 339,743,715 bytes and SHA-256
`d1ab50e0e8f85c17ee7b5e8950cb1be0f4f42aff90dd5c00fbab2f2a456d6732`.
It was replayed successfully but is not retained.

Retained artifacts:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members18.drat.xz` | 31,833,804 | `c01a55a15384f2105bb29f77344031f0e3580cbf36e39da55ebd0466a1b17bfc` | 142,058,484 | `51227ae9ccf3772bd9c5b7ac8f37b4c3086097c922163b223c7cfa4c61a7c5c6` |
| `order8-members18.lrat.xz` | 181,097,764 | `f1de80784a16e93fdd843aa4069767b2aee7e52f68430bc4eea6ff4c9bc764c1` | 802,739,932 | `3d53da4411633722d6ff47f017ecdd471fbc64c1d037b95e3a55484ed007ddc1` |

`certificates/manifest.json` is the machine-readable source for these values.
The two earlier incomplete CaDiCaL attempts are documented in `artifacts/`;
neither partial trace is used or retained as a certificate.

## Novelty scope

The source paper reports computations only through seven ground elements.
This package is best described as a reproducible candidate new bounded
extension at order eight, not as a peer-reviewed priority claim.

## Tool identities

- Kissat 4.0.4, tag `rel-4.0.4`, commit
  `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, executable SHA-256
  `43be6166b83812b19e4c83cbbc1536f2772c90c722b24c0d6635707512b45c0e`
- `drat-trim`, commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, executable SHA-256
  `879d1e408ba3f59970781c69bb67b823ef5f539f672bbdd1934927ada377cfee`
- `lrat-check`, same source commit, executable SHA-256
  `9117804c5d07cb7a5e786ab5558e3485dca49762f5458a01ca715893da0d15be`
- Python 3.13.5 under `uv`; dependencies locked by `uv.lock`

## Reproduce

Run static, semantic, differential, and fingerprint checks:

```sh
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Regenerate and fingerprint the CNF:

```sh
uv run uctight-m18 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay the retained DRAT and LRAT proofs:

```sh
uv run uctight-m18 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

Rebuild both certificates from scratch using an unused work directory:

```sh
uv run uctight-m18 certify \
  --solver /tmp/arcadia-kissat404/build/kissat \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/rebuild \
  --timeout-seconds 1800
```

Verification expands about 0.95 GB of proof data under the selected work
directory. A successful command exits zero and prints
`order=8, m=18: retained DRAT+LRAT VERIFIED`.
