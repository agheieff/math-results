# Exact order-eight, \(m=22\) report

## Result

There is no clean tight union-closed family \(\mathcal F\) of exactly 22
distinct subsets of an eight-element ground set:

\[
|X|=8,\qquad |\mathcal F|=22.
\]

This certificate-backed finite verification extends the separately packaged
order-eight range through 22 members. It does not prove the general
union-closed sets conjecture or address other ground-set orders.

Since \(m=22\) is even, tightness permits frequency exactly \(m/2=11\).
Therefore this result is stronger at this parameter than merely ruling out
Frankl counterexamples.

## Encoding and semantic audit

The package uses one membership variable \(p_A\) for each \(A\subseteq X\)
and deterministic totalizer auxiliaries. It encodes:

1. exactly 22 selected subsets, including \(\varnothing\) and \(X\);
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
  `572ef916a42a0da50c00aa8711462052b3eb77fe9f9b91e30a54082cff1b1c5f`.

## Certificate chain

Kissat returned exit 20 and exact output `s UNSATISFIABLE`, producing binary
DRAT. A separately built `drat-trim` replayed the raw proof while extracting
a core, replayed the retained DRAT, and converted it to LRAT. The separate
`lrat-check` executable accepted the LRAT. Every checker stage emitted its
exact verification marker and exited zero.

| Stage | Wall time |
|---|---:|
| Kissat proof-trace lifetime | approximately 996.042 s |
| raw DRAT replay and trimming | 381.04 s |
| retained DRAT replay | 301.72 s |
| DRAT-to-LRAT conversion | 294.42 s |
| LRAT replay | 17.70 s |

The solver was not run under a timing wrapper. Its value above is explicitly
a filesystem proxy: raw-proof birth at `20:46:26.266320073` and final
modification at `21:03:02.308052518`. Every external stage had a
1,800-second timeout.

The original raw DRAT has 514,740,496 bytes and SHA-256
`a25a13c9df1975ce2f2a00b00668f276b5cecf03e9a2994d57932d712828049e`.
Its preserved archive is `artifacts/order8-members22.raw.drat.xz`, with
210,837,764 bytes and SHA-256
`fe60b662bfb8093ec2c9f1fcaab6020935a0dbb24a9017c04384fb04f4ab38e1`.

Retained public certificates:

| Artifact | Compressed bytes | Compressed SHA-256 | Raw bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `order8-members22.drat.xz` | 41,117,580 | `b654d6bc1c48cfefb6f39a81f595a2f0a92b9701d211d7468aa728b80f5ddd9c` | 160,708,761 | `d78381faa9383c1e0d3dc01d92a09592c6d1a5e85ef4c868c3330a33a26f6ff3` |
| `order8-members22.lrat.xz` | 264,645,984 | `6b01be9c79ca2546b197c676d9fde441bd0ef0757badb03d33535c2c1b9cc8da` | 1,090,820,122 | `cee6908090281307e9a640b684b5b3a596c12957384387d25f70128d3618a86a` |

`certificates/manifest.json` records all retained dimensions, hashes, timings,
and tool identities. The packaged public verifier regenerated the CNF,
validated every compressed and uncompressed size and hash, replayed both
proofs from fresh decompression, and completed in 291.51 seconds with
`order=8, m=22: retained DRAT+LRAT VERIFIED`.

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
uv run uctight-m22 generate --output .work/target.cnf
sha256sum .work/target.cnf
```

Replay both retained proof formats from fresh decompression:

```sh
uv run uctight-m22 verify \
  --drat-checker /tmp/arcadia-math-drat-trim/drat-trim \
  --lrat-checker /tmp/arcadia-math-drat-trim/lrat-check \
  --manifest certificates/manifest.json \
  --work-directory .work/verify \
  --timeout-seconds 1800
```

A successful public replay exits zero and prints
`order=8, m=22: retained DRAT+LRAT VERIFIED`.
