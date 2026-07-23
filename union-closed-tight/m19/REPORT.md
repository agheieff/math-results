# Exact order-eight, \(m=19\) report

## Result

There is no clean tight union-closed family of exactly 19 distinct subsets of
an eight-element ground set:

\[
|X|=8,\qquad |\mathcal F|=19.
\]

This is a certificate-backed verification of the single finite parameter
pair. Together with the separate packages for smaller cardinalities, it
extends the verified order-eight range through 19 members. It does not address
\(m\geq20\), other ground-set orders, or prove the general clean-tight or
union-closed sets conjecture.

Because \(m\) is odd, tightness here means every element has frequency at most
9, whereas Frankl's conjecture would require some element to have frequency
at least 10. Thus a family excluded by this exact clean-tight gate would be a
Frankl counterexample, although the result does not cover non-clean families
at this ground-set order.

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

1. exactly 19 distinct selected subsets, including \(\varnothing\);
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
| family size | \(\sum_Ap_A=19\) |
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
  `65e77adfc1c4114a5e6f86f322b183dcc4301f0d85000f612f61695992314ec7`

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
| Kissat UNSAT search | 109.12 s |
| raw DRAT replay and trimming | 106.16 s |
| retained DRAT replay | 145.46 s |
| DRAT-to-LRAT conversion | 186.68 s |
| LRAT replay | 8.60 s |

Each external search/check stage had an 1800-second timeout.

The original raw DRAT proof had 294,319,256 bytes and SHA-256
`86bf0bbb021771f1a493476d27f35b8281b8ac8ce197684b7afba969e4ddc7e7`.
It was replayed successfully but is not retained.

Retained artifacts:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members19.drat.xz` | 24,630,836 | `63954940070c0783078882802d2216a83ecfba46c69062e7670f185b271aafd5` | 109,350,855 | `b06a9e9c1c5ccde534fd3d6ab627461e862f1f74b7d39d69a32e4bca4f89d325` |
| `order8-members19.lrat.xz` | 146,278,348 | `1c4970c6edef8a2eca01c3b02b0c9485e8b725347ecc6529729a24ee50874bb4` | 646,798,134 | `c8bb6b152eebcc6074a23b9358e9e39e2ac493ca2107c621a5b3ec2267104f23` |

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
uv run uctight-m19 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay the retained DRAT and LRAT proofs:

```sh
uv run uctight-m19 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

Rebuild both certificates from scratch using an unused work directory:

```sh
uv run uctight-m19 certify \
  --solver /tmp/arcadia-kissat404/build/kissat \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/rebuild \
  --timeout-seconds 1800
```

Verification expands about 0.76 GB of proof data under the selected work
directory. A successful command exits zero and prints
`order=8, m=19: retained DRAT+LRAT VERIFIED`.
