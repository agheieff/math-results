# Exact order-eight, \(m=20\) report

## Result

There is no clean tight union-closed family of exactly 20 distinct subsets of
an eight-element ground set:

\[
|X|=8,\qquad |\mathcal F|=20.
\]

This is a certificate-backed verification of the single finite parameter
pair. Together with the separate packages for smaller cardinalities, it
extends the verified order-eight range through 20 members. It does not address
\(m\geq21\), other ground-set orders, or prove the general clean-tight or
union-closed sets conjecture.

This statement is not subsumed by merely ruling out Frankl counterexamples at
this gate. Since \(m\) is even, a tight family may have elements of frequency
exactly \(m/2=10\) and therefore need not be a Frankl counterexample.

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

1. exactly 20 distinct selected subsets, including \(\varnothing\);
2. closure under pairwise union;
3. frequency at most 10 for every element;
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
| family size | \(\sum_Ap_A=20\) |
| tightness | \(\sum_{A\ni x}p_A\leq10\) for every \(x\) |
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
  `bf3bf0267d86d737cb40b45ad6d0b5bb2bd68e3c18f3c1c46e3f451e9767c300`

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
| Kissat UNSAT search | 380.01 s |
| raw DRAT replay and trimming | 374.41 s |
| retained DRAT replay | 321.96 s |
| DRAT-to-LRAT conversion | 319.10 s |
| LRAT replay | 16.91 s |

Each external search/check stage had an 1800-second timeout.

The original raw DRAT proof had 506,322,966 bytes and SHA-256
`341a7e8436410f01a42a29c89b0542cf7e59e4452e60c95d4cbee1a59f0a39e0`.
It was replayed successfully but is not retained.

Retained artifacts:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members20.drat.xz` | 48,186,852 | `b29f17955747006525a71832d04cb4e27d0499599542dbc822d2d11b0a798218` | 212,008,096 | `a1546a25bec639eb3437e2052455bc743d79266f194a80a180a1511ad6dc412e` |
| `order8-members20.lrat.xz` | 290,768,940 | `e1a8fd5774a6e661b4a500048610bc9e3f02710edee50529088adf33b4a2526f` | 1,267,593,276 | `a2e15552736f0f387fe80c57e55da2ab0cb489033e359e1e0ea2b87ae7ff25ed` |

`certificates/manifest.json` is the machine-readable source for these values.

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
uv run uctight-m20 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay the retained DRAT and LRAT proofs:

```sh
uv run uctight-m20 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

Rebuild both certificates from scratch using an unused work directory:

```sh
uv run uctight-m20 certify \
  --solver /tmp/arcadia-kissat404/build/kissat \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/rebuild \
  --timeout-seconds 1800
```

Verification expands about 1.48 GB of proof data under the selected work
directory. A successful command exits zero and prints
`order=8, m=20: retained DRAT+LRAT VERIFIED`.
