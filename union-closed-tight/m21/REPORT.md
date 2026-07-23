# Exact order-eight, \(m=21\) report

## Result

There is no clean tight union-closed family \(\mathcal F\) of exactly 21
distinct subsets of an eight-element ground set:

\[
|X|=8,\qquad |\mathcal F|=21.
\]

This is a certificate-backed verification of one finite parameter pair.
Together with the separate packages at smaller cardinalities, it extends the
verified order-eight range through 21 members. It does not prove the general
union-closed sets conjecture or address other ground-set orders.

For odd \(m=21\), tightness means every element has frequency at most 10, so
this gate also excludes a clean Frankl counterexample at this parameter.

## Encoding and semantic audit

The package follows the standing convention
\(\varnothing\in\mathcal F\). It encodes:

1. exactly 21 selected subsets, including \(\varnothing\) and \(X\);
2. closure under pairwise union;
3. frequency at most 10 for each element;
4. no idle element and distinct element-incidence columns;
5. nondecreasing element frequencies as a complete relabeling symmetry break.

The unit \(X\in\mathcal F\) adds no restriction: a finite union-closed family
without idle elements contains the union of all its members, namely \(X\).
Distinct incidence columns are exactly the remaining cleanliness condition.

For adjacent columns \(x,y\), the symmetry constraint is

\[
\sum_{A:x\in A,y\notin A}p_A+
\sum_{A:y\in A,x\notin A}(1-p_A)\leq64,
\]

which simplifies to
\(\operatorname{freq}(x)\leq\operatorname{freq}(y)\).

The direct predicate in `semantics.py` is independent of the CNF. Differential
tests compare both descriptions under every complete family assignment on
three elements for every cardinality 2 through 8.

The deterministic DIMACS has:

- 17,792 variables;
- 231,118 clauses;
- 4,333,092 bytes;
- SHA-256
  `765187b5ee37e03b97af226faffda4ec8477770e3eb0523390806b2245270ca4`.

## Certificate chain

Kissat returned `s UNSATISFIABLE` and a binary DRAT proof. A separately built
`drat-trim` replayed the raw proof while extracting a core, then replayed that
retained DRAT. A second `drat-trim` pass converted it to LRAT, and the separate
`lrat-check` executable accepted the LRAT. Every checker stage emitted its
exact verification marker and exited zero.

| Stage | Wall time |
|---|---:|
| Kissat UNSAT search | 233.61 s |
| raw DRAT replay and trimming | 149.63 s |
| retained DRAT replay | 326.88 s |
| DRAT-to-LRAT conversion | 232.93 s |
| LRAT replay | 13.66 s |

Every external stage had a 1,800-second timeout.

The original raw DRAT has 356,224,569 bytes and SHA-256
`fd4b0f913570142412451d6c1c12eecf44d5273be88b7c8c022893d7aeab9301`.
Its preserved archive is `artifacts/order8-members21.raw.drat.xz`, with
137,261,356 bytes and SHA-256
`291902bfab57e048185191d6988dccd3e3e0541b5fb42a4ba67ab7b5137ba84c`.
The dated pause record beside it preserves the pre-replay checkpoint.

Retained public certificates:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members21.drat.xz` | 22,711,164 | `c88f8050e416026dce74e1fadcaec731cd469b033dc545c0afb293e2618cb133` | 92,467,983 | `b4292ce0626b846db077b046b26837a74429e1171d3a17aa071cfc8a28958cd6` |
| `order8-members21.lrat.xz` | 140,883,008 | `4878fc660a5eaa02c7271eba2c6e9aa625be3e8b194f121c78ef8f9e503886d2` | 588,716,289 | `820f7743acd4b534a9836809c19552b263f0e1f1d468be5142b05cbed9fb99c2` |

`certificates/manifest.json` is the machine-readable source for the retained
artifact dimensions, hashes, timings, and tool identities.

The packaged public verifier was then run from a fresh work directory. It
regenerated the CNF, validated every compressed and uncompressed size and
hash, replayed both retained proofs, and completed in 195.05 seconds with
`order=8, m=21: retained DRAT+LRAT VERIFIED`.

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
uv run uctight-m21 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay both retained proof formats from fresh decompression:

```sh
uv run uctight-m21 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

A successful public replay exits zero and prints
`order=8, m=21: retained DRAT+LRAT VERIFIED`.
