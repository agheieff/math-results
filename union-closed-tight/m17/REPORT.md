# Exact order-eight, \(m=17\) report

## Result

There is no clean tight union-closed family of exactly 17 distinct subsets of
an eight-element ground set:

\[
|X|=8,\qquad |\mathcal F|=17.
\]

This is a certificate-backed verification of the single finite parameter
pair. It extends the separate `union-closed-tight-m16/` computation by one
cardinality. It does not address \(m\geq18\), other ground-set orders, or prove
the general clean-tight or union-closed sets conjecture.

This finite case is also within previously published bounds for Frankl's
union-closed sets conjecture. The point of this package is the deterministic,
independently replayable certificate at the exact clean-tight gate.

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

1. exactly 17 distinct selected subsets, including \(\varnothing\);
2. closure under pairwise union;
3. frequency at most 8 for every element;
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
| family size | \(\sum_Ap_A=17\) |
| tightness | \(\sum_{A\ni x}p_A\leq8\) for every \(x\) |
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
  `9814d5a35f5c447bc0f1733d6ba1cdb651abb4e4206442fd0546c660440b4b52`

The complete fingerprint is pinned by a regression test.

## Certificate chain

CaDiCaL produced an UNSAT binary DRAT proof. `drat-trim` replayed the raw
proof while extracting its core, then replayed the trimmed proof. A separate
conversion produced LRAT, which `lrat-check` accepted. Finally, the public
verification command regenerated the CNF, checked compressed and
uncompressed hashes and sizes, and replayed both retained artifacts from a
fresh work directory.

| Stage | Wall time |
|---|---:|
| CaDiCaL UNSAT search | 432.14 s |
| raw DRAT replay and trimming | 261.91 s |
| retained DRAT replay | 162.77 s |
| DRAT-to-LRAT conversion | 293.44 s |
| LRAT replay | 19.50 s |

Each external search/check stage had an 1800-second timeout. The CaDiCaL
timing is the observed proof-file creation interval; checker timings came from
the replay commands.

The original raw DRAT proof had 608,844,315 bytes and SHA-256
`a3045d01483ec07fa798bc6e6426b3ac919d1a691e68bfaa82e3f436d8d440ea`.
It was replayed successfully but is not retained.

Retained artifacts:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members17.drat.xz` | 49,793,716 | `b465be8223defb6e38f3987d25e345137cea77fdde56b03e32aaeb81a55e2a58` | 233,787,105 | `eacf5878e482024d3e8788c002d3095a5cd9f22ae92454ecb93f90eef98e5af6` |
| `order8-members17.lrat.xz` | 302,065,536 | `29ee7749b501ca038309e59bdd8c7bc60cd4650282ac65ebaa1818dfc5071697` | 1,263,297,636 | `7898f8f4fcca88f7c3731652fb08392011583a3c6df591d6f7df5bafc8954165` |

`certificates/manifest.json` is the machine-readable source for these values.

## Tool identities

- CaDiCaL 2.2.1, executable SHA-256
  `d33c27ced2a9273e40e90d060626ca75544dd7debeda027fb93e62cc3d27d095`
- `drat-trim`, executable SHA-256
  `879d1e408ba3f59970781c69bb67b823ef5f539f672bbdd1934927ada377cfee`
- `lrat-check`, executable SHA-256
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
uv run uctight-m17 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay the retained DRAT and LRAT proofs:

```sh
uv run uctight-m17 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

Rebuild both certificates from scratch using an unused work directory:

```sh
uv run uctight-m17 certify \
  --solver /tmp/cadical.yg5jft/build/cadical \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/rebuild \
  --timeout-seconds 1800
```

Verification expands about 1.5 GiB of proof data under the selected work
directory. A successful command exits zero and prints
`order=8, m=17: retained DRAT+LRAT VERIFIED`.
