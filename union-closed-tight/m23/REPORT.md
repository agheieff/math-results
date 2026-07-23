# Exact order-eight, \(m=23\) report

## Result

There is no clean tight union-closed family \(\mathcal F\) of exactly 23
distinct subsets of an eight-element ground set:

\[
|X|=8,\qquad |\mathcal F|=23.
\]

This certificate-backed finite verification extends the separately packaged
order-eight range through 23 members. It does not prove the general
union-closed sets conjecture or address other ground-set orders.

For odd \(m=23\), tightness means every element has frequency at most 11, so
this gate also excludes a clean Frankl counterexample at this parameter.

## Encoding and semantic audit

The package uses one membership variable \(p_A\) for each \(A\subseteq X\)
and deterministic totalizer auxiliaries. It encodes:

1. exactly 23 selected subsets, including \(\varnothing\) and \(X\);
2. closure under pairwise union;
3. frequency at most 11 for each element;
4. no idle element and pairwise-distinct element-incidence columns;
5. nondecreasing element frequencies as a complete relabeling symmetry break.

The unit \(X\in\mathcal F\) adds no restriction: a finite union-closed family
without idle elements contains the union of all its members, namely \(X\).
For adjacent columns \(x,y\), the symmetry totalizer simplifies exactly to
\(\operatorname{freq}(x)\leq\operatorname{freq}(y)\).

The direct predicate in `semantics.py` is independent of the CNF.
Differential tests compare both descriptions under every complete family
assignment on three elements for every cardinality 2 through 8.

The deterministic DIMACS has:

- 17,792 variables;
- 231,118 clauses;
- 4,333,092 bytes;
- SHA-256
  `53339228c8bb4666bf973cb980dc15dffd2307180c5aeba5fe47a0d79a1659a1`.

## Certificate chain

Kissat returned exit 20 and exact output `s UNSATISFIABLE`, producing binary
DRAT. A separately built `drat-trim` replayed the raw proof while extracting
a core, replayed the retained DRAT, and converted it to LRAT. The separate
`lrat-check` executable accepted the LRAT. Every checker stage emitted its
exact verification marker and exited zero.

| Stage | Wall time |
|---|---:|
| Kissat UNSAT search | 153.81 s |
| raw DRAT replay and trimming | 129.54 s |
| retained DRAT replay | 94.39 s |
| DRAT-to-LRAT conversion | 95.16 s |
| LRAT replay | 5.03 s |

Every external stage had a 1,800-second timeout.

The original raw DRAT has 247,841,218 bytes and SHA-256
`23143a48de0eed3f22d381a16d33612d82f11aa53dd6924ae167077bc02e59c0`.
Its preserved archive is `artifacts/order8-members23.raw.drat.xz`, with
101,032,048 bytes and SHA-256
`30f13c6beb936a1d01b2040ff2e3b695c21897891beab8ece33a7592ba7c9188`.

Retained public certificates:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members23.drat.xz` | 21,909,716 | `d24ab770d751e0eb1d99f522a2ba6c437981fd3ec2c24618a03bd94170a479f2` | 79,375,809 | `8b0edb1c39937f272ab62cac1b8fce527836251ebac2af7fe8cb809a3fd867c7` |
| `order8-members23.lrat.xz` | 143,389,804 | `ee1435da0d6d2fb7dc6e49047ea1aba385ba26965237d46d6141932a29267945` | 593,172,286 | `6f1b45925aa3315a03aad771d32bb4d7ac69bd45ec8e700e80e38697e6b56e4c` |

`certificates/manifest.json` records all retained dimensions, hashes, timings,
and tool identities. The packaged public verifier regenerated the CNF,
validated every compressed and uncompressed size and hash, replayed both
proofs from fresh decompression, and completed in 162.59 seconds with
`order=8, m=23: retained DRAT+LRAT VERIFIED`.

## Tool identities

- Kissat 4.0.4, tag `rel-4.0.4`, commit
  `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, executable SHA-256
  `43be6166b83812b19e4c83cbbc1536f2772c90c722b24c0d6635707512b45c0e`;
- `drat-trim`, commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, executable SHA-256
  `879d1e408ba3f59970781c69bb67b823ef5f539f672bbdd1934927ada377cfee`;
- `lrat-check`, from the same source commit, executable SHA-256
  `9117804c5d07cb7a5e786ab5558e3485dca49762f5458a01ca715893da0d15be`;
- Python 3.13.5 under `uv`, with dependencies pinned by `uv.lock`.

## Reproduce

Run the code-level gates:

```sh
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Regenerate and fingerprint the CNF:

```sh
uv run uctight-m23 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay both retained proof formats from fresh decompression:

```sh
uv run uctight-m23 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

A successful public replay exits zero and prints
`order=8, m=23: retained DRAT+LRAT VERIFIED`.
