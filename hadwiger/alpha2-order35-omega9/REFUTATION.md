# Refutation of the proposed clique-nine edge lemma

## The proposed lemma

At the order-35 frontier, let \(G\) have independence number two and let
\(C\) be a nine-clique. Put \(F=\overline G\), \(P=V(G)\setminus C\),
and
\[
S_v=N_F(v)\cap C\qquad(v\in P).
\]
A tempting strengthening of the order-33 incidence argument was:

> There are \(a,b\in P\) such that \(ab\in E(G)\) and
> \(S_a\cap S_b=\varnothing\).

Such an edge would dominate \(C\), produce a ten-branch core on eleven
vertices, and leave exactly 24 vertices for eight seagulls. The
statement is false, even after imposing all presently used local
properties of a hypothetical minimum counterexample.

## Countercertificate

Let \(C=\{0,\ldots,8\}\), and give the vertices \(9,\ldots,34\) the
following supports, in order:

```text
027 014 278 357 158 156 0367 068 0345 1268 025 157 178
245 134 458 368 347 013 038 248 467 127 046 256 236
```

Define \(F\) by making \(C\) independent, joining \(v\in P\) to the
points in \(S_v\), and joining two vertices of \(P\) exactly when their
supports are disjoint. Its graph6 encoding is

```text
b??????gUOCLDQPKGqceA_ga[CBDCLG?@D?GOW@PW?ojA`GBKC?Cm?YBGLWE_G?ScGGI?gao_OUAA?rA?WEQIF?o@Ha?DM@cQ@c??
```

Exact verification gives:

- \(F\) is triangle-free, has 150 edges, and has independence number
  nine;
- its degree multiset is \(7^2,8^{11},9^{22}\);
- \(F\) is factor-critical;
- \(G=\overline F\) has
  \(\alpha(G)=2\), \(\omega(G)=9\), \(\chi(G)=18\), and
  \(\kappa(G)=25\);
- every edge contraction of \(G\) has chromatic number 17;
- every edge of \(G\) is non-dominating; and
- no edge in \(G[P]\) dominates \(C\).

For the contraction claim, the verifier checks for every
\(uv\in E(G)\) that some common \(F\)-neighbour \(x\) leaves a perfect
matching in \(F-\{u,v,x\}\). Factor-criticality similarly certifies
vertex-criticality.

Thus the countercertificate survives the degree, Hall, connectivity,
vertex-criticality, contraction-criticality, and non-dominating-edge
conditions available from the minimum-counterexample setup.

## The graph is not a Hadwiger counterexample

The failed lemma was only a proposed proof device. The graph itself has
the following spanning \(K_{18}\)-model:

```text
{0}
{1,22} {2,23} {3,29} {4,27} {5,26} {6,10} {7,14} {8,33}
{9,31} {11,15} {12,25} {13,17} {16,30} {18,21} {19,20}
{24,32} {28,34}
```

Every two-vertex branch is an edge of \(G\), and all 18 branch sets
pairwise touch. An independently found second model is

```text
{32}
{0,2} {1,16} {3,19} {4,34} {5,7} {6,27} {8,33} {9,18}
{10,28} {11,29} {12,24} {13,14} {15,31} {17,25} {20,26}
{21,23} {22,30}
```

For two \(G\)-edge branches of size two, failure to touch is exactly the
selection of both diagonals of an induced four-cycle in \(F\). The two
models therefore suggest a replacement order-35 argument: seek a
near-perfect matching in \(G\) which contains neither both diagonals of
an \(F\)-induced four-cycle nor an edge wholly inside the
\(F\)-neighbourhood of its unmatched vertex.

The order-35 clique-nine case remains unresolved in general.
