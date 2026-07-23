# Rung-4 reconnaissance: K7-minor-free graphs

**Audit date:** 2026-07-23  
**Parent target status:** open in the audited primary sources  
**Lane result:** inconclusive for the parent target; one local lemma refuted exactly

## Scope freeze

All graphs are finite and simple. A \(K_t\) minor consists of \(t\) nonempty, pairwise disjoint,
connected branch sets with an edge between every pair.

The frozen rung-4 target is

\[
  \forall G,\qquad K_7\not\preccurlyeq G\ \Longrightarrow\ \chi(G)\le 7.
\]

Its exact negation is a finite simple graph \(G\) with no \(K_7\) minor and
\(\chi(G)\ge 8\). A positive result requires a conventional audited proof (and independent
specialist review under the repository protocol); a negative result requires raw graph data plus
independent checks of both chromatic number and minor exclusion.

The allowed imported results here are Mader's \(K_7\)-minor extremal bound, standard facts about
minor-minimal counterexamples, the Rolek--Song generalized Kempe-chain lemma, the 2023
Rolek--Song--Thomas (RST) theorem quoted below, and the 2025 Norin--Totschnig theorem excluding
\(K_7^\vee\).

This target is weaker than the still-open \(t=7\) case of Hadwiger's conjecture, which asks for
6-colourability. Settling a bounded order, checking a neighborhood graph, or refuting an auxiliary
lemma would not settle either statement.

## Authoritative frontier

RST prove that if \(G\) is 8-contraction-critical and has no \(K_7\) minor, then:

1. \(8\le\delta(G)\le9\);
2. with \(n_i=|\{v:d(v)=i\}|\), \(n_8\le1\) and
   \(n_9\ge30-2n_8\ge28\);
3. for each degree-9 vertex \(v\), either \(G[N[v]]\) contains \(K_5\), or
   \(\alpha(G[N(v)])=3\) and \(1\le\delta(G[N(v)])\le4\).

Their abstract explicitly says that 7-colourability remains open. Norin--Totschnig subsequently
proved that excluding \(K_7^\vee\), obtained from \(K_7\) by deleting two edges with a common end,
forces 6-colourability. This is a stricter graph class, not the frozen target. The current-source
audit in `PRIOR_ART.md` found no primary source closing the universal target; its best published
colouring bound remains 8 colours.

## Minimal-counterexample dependency graph

Assume the frozen target is false and take a counterexample minimal under the proper-minor order.

```text
proper-minor minimality
  -> every proper minor is 7-colourable
  -> deleting a vertex and restoring it gives chi(G) <= 8
  -> chi(G) = 8
  -> G is 8-contraction-critical
  -> Norin--Totschnig: G contains a K7^vee minor
  -> apply RST
       -> delta(G) is 8 or 9
       -> n8 <= 1
       -> at least 28 degree-9 vertices
       -> every degree-9 neighborhood has one of two exact local forms
```

Mader's bound \(e(G)\le5|G|-15\) gives the useful bookkeeping inequality

\[
  \sum_{v\in V(G)}(10-d(v))\ge30,
\]

or, more sharply,

\[
  2n_8+n_9\ge30+\sum_{d\ge11}(d-10)n_d.
\]

Thus eliminating every degree-9 vertex would contradict RST/Mader immediately; even
\(n_9\le27\) would suffice. Neither conclusion is established here.

## First frozen new structural lemma

For the hard RST alternative with no \(K_5\) in \(G[N[v]]\), set \(H=G[N(v)]\). Then \(H\) has
nine vertices, is \(K_4\)-free, has \(\alpha(H)=3\) and \(1\le\delta(H)\le4\), and has no
\(K_6\) minor (otherwise the universal vertex \(v\) supplies a \(K_7\) minor).

The first local bridge was frozen before testing:

> **Matching-completion lemma.** Every 9-vertex, \(K_4\)-free, \(K_6\)-minor-free graph \(H\)
> with \(\alpha(H)=3\) and \(1\le\delta(H)\le4\) has an independent triple
> \(S\) and a matching \(M\) of missing edges in \(H-S\) such that \(H+M\) has a
> \(K_6\) minor.

For \(k=8\), \(d(v)=9=k+1\), and \(|S|=3\), the Rolek--Song lemma realizes every such matching
(\(|M|\le3\)) by pairwise vertex-disjoint paths whose interiors lie outside \(N[v]\). Contracting
those paths would realize \(H+M\) as a minor, and a \(K_6\) minor there together with \(v\) would
give a \(K_7\) minor. Therefore the lemma would eliminate only the \(K_4\)-free degree-9 branch.
It would not address degree-9 neighborhoods containing \(K_4\), eliminate all degree-9 vertices,
or prove the parent target by itself.

## Exact local refutation

The lemma is false. Let

\[
  R=L(K_{3,3}),
\]

the \(3\times3\) rook graph: cells are adjacent exactly when they share a row or column. The raw
18-edge object is in `src/hadwiger_k7/obstruction.py`. Its canonical JSON SHA-256 is
`18c6d8aae8f72705038b0ebd16e17e0ae423c9eda2e66e475c5c8c5e7ed469bd`. Direct checks give:

- \(|V(R)|=9\), every degree is 4, \(\omega(R)=3\), and \(\alpha(R)=3\);
- \(R\) has no \(K_6\) minor;
- \(R\) has exactly six independent triples;
- for every one of those triples \(S\), all 32 matchings of missing edges in \(R-S\) were
  enumerated, including the empty matching;
- none of the 192 graphs \(R+M\) has a \(K_6\) minor.

Two separately written exact minor checkers agree. One enumerates selected vertex sets and their
canonical six-block partitions. The other independently enumerates connected vertex masks and
searches for six disjoint pairwise-touching masks. Both allow unused vertices, and both are tested
on positive and negative controls.

This object need not occur as a neighborhood in an 8-contraction-critical graph. It refutes only
the frozen local lemma and is not progress on the full Hadwiger problem.

## Reproduction and next boundary

```sh
uv sync --dev
uv run hadwiger-k7-check
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
```

On the audit host (Arch Linux, CPython 3.13.5), the standalone exact verifier used 7.315 seconds
wall time, 7.287 seconds user CPU, and 0.006 seconds system CPU. Package versions are pinned by
`uv.lock`.

The next structural step must use constraints absent from an arbitrary local graph—the forced
\(K_7^\vee\) minor, ambient 7-connectivity, interactions among many degree-9 vertices, or the more
general star-shaped Rolek--Song linkages. Pure matching completion of one neighborhood is
insufficient.
