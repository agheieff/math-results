# Prior-art and status audit

Search date: **2026-07-23**, Europe/Prague.

## Primary sources inspected

- Qinglin Wang and Yingzhi Tian,
  ["Extremal graphs with no subgraph admitting \(k+1\) edge-disjoint spanning
  trees"](https://arxiv.org/abs/2606.28198), arXiv:2606.28198v1, submitted
  2026-06-26. The abstract, HTML, and TeX source were inspected. Definitions
  are in the introduction, the density implication is Lemma 2.1, and the
  target statement is Conjecture 1 immediately before Theorem 3.8.
- Audrey Lee and Ileana Streinu,
  ["Pebble Game Algorithms and Sparse Graphs"](https://arxiv.org/abs/math/0702129),
  arXiv:math/0702129v1, submitted 2007-02-06. The TeX source was inspected.
  The relevant result is Theorem 2, "The \((k,\ell)\)-sparsity matroid," plus
  the paragraph immediately after its proof covering deletion of ambient
  ground-set edges.
- Wang--Tian state the Nash--Williams--Tutte partition theorem as their
  Theorem 1 and cite the original 1961 papers. The present report uses that
  theorem only through the short density induction reproduced in full.

Extracted TeX SHA-256 values used for this audit:

```text
e00bec51d2f351becbd9d4bff00c236c494ee8e465dca04749787de08a070fcf  manuscript.tex
fd9ba3fc58adc3ec4684f2f30748ef19c0c18abd318460649ea74cd99e47b403  pgsparse.tex
```

## Version and resolution search

The arXiv record displayed only v1 on the search date. These exact web queries
were run:

```text
"tau_k-maximal" conjecture Wang Tian 2026
"Extremal graphs with no subgraph admitting" conjecture proof
"every" "tau_k-maximal" graph "exactly"
site:arxiv.org/abs/2607 "tau_k" maximal spanning trees
```

The results found the original preprint and automated index/review mirrors,
but no later arXiv version, independent proof, or citing resolution. A direct
Semantic Scholar API request was also attempted and returned HTTP 429, so no
citation-count claim is made.

This is a timestamped, non-exhaustive search, not a novelty certification.

## Relationship to existing theory

The mathematical engine is classical: maximal independent sets of a matroid
are equicardinal. Lee--Streinu already establish that
\((q,q+1)\)-sparse edge sets form a count matroid in the required range and
explicitly permit restriction to a chosen ground graph.

The remaining observation is that Wang--Tian's own density lemma, applied to
every edge-supported subgraph, gives the exact equivalence

\[
\bar\tau(G)\le q-1
\quad\Longleftrightarrow\quad
G\text{ is }(q,q+1)\text{-sparse}.
\]

Accordingly, any external claim of a new resolution should receive an expert
bibliographic check before dissemination.
