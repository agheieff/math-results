# Exact order-eight, \(m=16\) report

## Result

There is no clean tight union-closed family of exactly 16 distinct subsets of
an eight-element ground set. This is a finite, certificate-backed nonexistence
result for the single parameter pair

\[
|X|=8,\qquad |\mathcal F|=16.
\]

It extends the separate `union-closed-tight/` computation by one cardinality.
It does not address \(m\geq17\), other ground-set orders, or prove the general
clean-tight conjecture.

## Independent semantic audit

The definitions were checked against van der Hout and Roos,
*Some results and conjectures related to Frankl's union closed conjecture*,
[JANO 8 (2026), 11--18](https://doi.org/10.23952/jano.8.2026.1.02).
The paper uses the standing convention \(\varnothing\in\mathcal F\), defines
tightness by

\[
|\mathcal F_x|\leq |\mathcal F|/2\quad\text{for every }x\in X,
\]

and calls a family clean when it has no idle elements and all incidence blocks
are singletons. Equivalently, every two elements have different incidence
columns.

The implementation therefore checks:

1. exactly 16 distinct selected subsets, including \(\varnothing\);
2. closure under pairwise union;
3. frequency at most 8 for every element;
4. no idle element and pairwise-distinct incidence columns.

A finite union-closed family with no idle element contains \(X\): iterating
unions over all members gives their union, which is \(X\). Thus the CNF unit
forcing \(X\in\mathcal F\) is a consequence of cleanliness, not an extra
restriction.

Element labels do not matter. Relabeling them by nondecreasing frequency gives
a canonical representative, so the symmetry constraint
\(\operatorname{freq}(0)\leq\cdots\leq\operatorname{freq}(7)\) is complete.

The direct predicate in `semantics.py` does not inspect the CNF. Differential
tests compare it with SAT under every complete family assignment on a
three-element ground set, for every cardinality 2 through 8. The order-four
power set is also accepted at the \(m=16\) boundary.

## CNF

For each subset \(A\subseteq X\), membership variable \(p_A\) says
\(A\in\mathcal F\). Auxiliary variables come only from deterministic totalizer
cardinality encodings.

| Condition | Clauses |
|---|---|
| standing convention and no-idle consequence | \(p_\varnothing\), \(p_X\) |
| union closure | \(\neg p_A\lor\neg p_B\lor p_{A\cup B}\) for incomparable \(A,B\) |
| family size | \(\sum_A p_A=16\) |
| tightness | \(\sum_{A\ni x}p_A\leq8\) for each \(x\) |
| canonical labels | adjacent nondecreasing-frequency constraints |
| clean columns | one separating selected set for each element pair |

For adjacent elements \(x,y\), the canonical-label totalizer encodes

\[
\sum_{A:x\in A,y\notin A}p_A+
\sum_{A:y\in A,x\notin A}(1-p_A)\leq128,
\]

which simplifies exactly to
\(\operatorname{freq}(x)\leq\operatorname{freq}(y)\).

The fresh target DIMACS is deterministic:

- variables: `17792`
- clauses: `231118`
- bytes: `4333092`
- SHA-256:
  `9b1b28bf74ef19a77310e2c5dcdb1f98ba74e634e8ea33b5daea858e44645676`

The complete fingerprint is pinned by a test.

## Certificate chain

CaDiCaL produced an UNSAT binary DRAT proof. `drat-trim` first replayed the raw
proof while extracting its core, then replayed the trimmed proof. A separate
conversion produced LRAT, which `lrat-check` accepted. Finally, the public
verification command regenerated the CNF, checked compressed and uncompressed
hashes and sizes, and replayed both retained artifacts again.

| Stage | Wall time |
|---|---:|
| CaDiCaL UNSAT search | 254.767 s |
| raw DRAT replay and trimming | 252.271 s |
| retained DRAT replay during build | 189.645 s |
| DRAT-to-LRAT conversion | 198.205 s |
| LRAT replay during build | 11.269 s |

Every external search/check stage had an independent 1800-second timeout.
No stage approached the bound. Monitored peak resident memory was about
1.3 GiB during LRAT conversion. The largest working artifact was the
1,421,687,569-byte LRAT file; there was no runtime, memory, or storage blocker.

Retained artifacts:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members16.drat.xz` | 50,306,844 | `8e0a47aea5b230a83f8922c89877009f2053fad5f6ada3d495447c71198611ec` | 291,048,243 | `e3161b9e550b24821082806592078e7bcdcc942144ffed80c080ce0b524239ce` |
| `order8-members16.lrat.xz` | 264,889,336 | `d6d2417bed6980a9f92255c777fa4b15215969aa5c5bae328e4c691f2e80d5af` | 1,421,687,569 | `c31131d4341e90506c68e8e5a8dbe650061c00b0a05ea7335f0ed1fb58551158` |

`certificates/manifest.json` is the machine-readable source for these values.

## Tool identities

- CaDiCaL 2.2.1, commit
  `4198d817d0dcde5b1240eefbff70b555b7df2af9`, executable SHA-256
  `d33c27ced2a9273e40e90d060626ca75544dd7debeda027fb93e62cc3d27d095`
- `drat-trim`, commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, executable SHA-256
  `879d1e408ba3f59970781c69bb67b823ef5f539f672bbdd1934927ada377cfee`
- `lrat-check`, same source commit, executable SHA-256
  `9117804c5d07cb7a5e786ab5558e3485dca49762f5458a01ca715893da0d15be`
- Python 3.13.5 under `uv`; dependencies locked by `uv.lock`

The executable paths and hashes are also recorded in the manifest.

## Reproduce

Install and run all static and differential checks:

```sh
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Regenerate and fingerprint the CNF:

```sh
uv run uctight-m16 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay the retained DRAT and LRAT proofs:

```sh
uv run uctight-m16 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

Rebuild both certificates from scratch using an unused work directory:

```sh
uv run uctight-m16 certify \
  --solver /tmp/cadical.yg5jft/build/cadical \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/rebuild \
  --timeout-seconds 1800
```

Verification expands about 1.7 GiB of proof data under the selected work
directory. A successful command exits zero and prints
`order=8, m=16: retained DRAT+LRAT VERIFIED`.
