# Refutation of the order-39 local support implication

## Proposed local implication

The attempted order-39 route sought to derive a core-dominating edge from the
following local structural consequences, without using
\(K_{20}\)-minor-freeness itself. Let \(G\) have 39 vertices and satisfy

\[
\alpha(G)=2,\quad \omega(G)=10,\quad \chi(G)=20,\quad\kappa(G)\geq20,
\]

let every edge contraction have chromatic number 19, let no edge of \(G\) be
dominating, and let \(F=\overline G\) be factor-critical and have diameter
two. Fix a degree-ten vertex \(v\) of \(F\), set
\[
C=N_F(v),\qquad X=V(F)\setminus(C\cup\{v\}),
\]
and for \(x\in X\) write \(S_x=N_F(x)\cap C\).

The proposed local implication was:

> Some \(a,b\in X\) satisfy \(ab\notin E(F)\) and
> \(S_a\cap S_b=\varnothing\).

Then \(ab\in E(G)\), and the branch \(\{a,b\}\) touches all ten singleton
branches in \(C\). The certificate below satisfies every listed hypothesis
but has no such pair, so this implication is false.

This says nothing about a stronger statement whose hypothesis still includes
that \(G\) has no \(K_{20}\) minor. The certificate has a \(K_{20}\) minor.

The order-39 clique-ten branch is motivated in part by Scully and Song's
recent dominating-Hadwiger threshold
([arXiv:2510.12564](https://arxiv.org/abs/2510.12564)); see
[PRIOR_ART.md](PRIOR_ART.md)). The countercertificate and its verification do
not depend on that theorem.

## Countercertificate

Index the coordinates of \(C\) by \(0,\ldots,9\). The 28 supports are:

```text
015 015 023 036 038 049 04a 052 064 0a8 0b0 0d0 10e 121
141 160 186 18a 18c 203 209 218 224 244 281 2c0 310 382
```

Here a hexadecimal mask records a subset of the ten coordinates. Construct
\(F\) on
\[
\{v\}\mathbin{\dot\cup}C\mathbin{\dot\cup}X
\]
by joining \(v\) to all of \(C\), joining \(x\in X\) to its support
\(S_x\), and joining two vertices of \(X\) exactly when their supports are
disjoint. Its graph6 encoding is:

```text
fsaCCA?_C?I_T?W_Eo?[?QOGhE@I??e??IeA@gB?JA?FA?BOc@aOSKK?Yo?@`_o?IL_O?WpA?B?ObpIOPEp_KH@BoCaBaQ?aQ`cOGDEwc??Z{@_?@ERW??CFrG???
```

## Why the support model is exact

This is not merely a list of necessary numerical conditions. Under the
contrary assumption to the proposed conclusion, adjacency inside \(X\) is
forced:

- intersecting supports cannot be adjacent in \(F\), since a shared point of
  \(C\) would complete a triangle;
- disjoint supports must be adjacent in \(F\), since otherwise their edge in
  \(G\) would dominate \(C\).

Thus \(F[X]\) is exactly the disjointness graph of the supports.

For a pairwise-intersecting support submultifamily \(\mathcal Q\), let
\(U=\bigcup\mathcal Q\). Stable sets of \(F\) have precisely two forms:

- with \(v\), at most \(1+|\mathcal Q|\) vertices, requiring
  \(|\mathcal Q|\leq9\);
- without \(v\), the vertices of \(\mathcal Q\) together with
  \(C\setminus U\), requiring \(|\mathcal Q|\leq|U|\).

Consequently
\[
|\mathcal Q|\leq\min(|U|,9)
\tag{1}
\]
for every pairwise-intersecting \(\mathcal Q\) is equivalent to
\(\alpha(F)\leq10\), not just necessary for it. The exact separator checks
all 1,023 nonempty \(U\subseteq C\) and computes a maximum-weight clique in
the intersection graph of the active support types contained in \(U\).

The remaining encoded conditions are likewise sufficient:

- no three support types are pairwise disjoint exactly prevents triangles
  inside \(X\);
- \(|S|+\#\{T:S\cap T=\varnothing\}\leq10\) is the degree bound at the
  corresponding outside vertex;
- coordinate multiplicity at most nine is the degree bound at \(C\);
- disjoint supports covering \(C\setminus S\) gives all missing
  length-two paths from an outside vertex to \(C\).

The other nonadjacent pairs already have a common neighbour by construction,
so these coverage checks are equivalent to \(\operatorname{diam}(F)\leq2\).

## Exact audit

The exact checker verifies:

- 22 supports have size three, six have size four, and total incidence is 90;
- every coordinate occurs exactly nine times;
- all degree, coverage, disjoint-triple, and inequalities (1) pass;
- \(F\) has 39 vertices, 183 edges, degree multiset
  \(7^1,8^3,9^{15},10^{20}\), diameter two, and no triangle;
- \(\alpha(F)=10\) by both the support separator and an independent exact
  maximum-stable-set search;
- \(F\) is factor-critical;
- \(G=\overline F\) has
  \[
  \alpha(G)=2,\quad\omega(G)=10,\quad\chi(G)=20,\quad\kappa(G)=28;
  \]
- all 558 edges of \(G\) are non-dominating and contract to a graph of
  chromatic number 19; and
- no edge of \(G[X]\) dominates the fixed clique \(C\).

For contraction-criticality, each \(uv\in E(G)\) is certified by a common
\(F\)-neighbour \(x\) and a perfect matching of
\(F-\{u,v,x\}\). This produces a 19-colouring after contracting \(uv\).

## The graph satisfies Hadwiger's conjecture

The countercertificate is not a Hadwiger counterexample. With
\(\{0\}=\{v\}\), the following is a spanning \(K_{20}\)-model:

```text
{0}
{1,22} {2,29} {3,18} {4,35} {5,26} {6,17} {7,21}
{8,15} {9,13} {10,24} {11,30} {12,23} {14,34} {16,32}
{19,25} {20,33} {27,37} {28,38} {31,36}
```

Every two-vertex branch is an edge of \(G\), and the verifier checks that all
20 branches are disjoint, connected, and pairwise touching.

## Search boundary

The decisive search started from a locally valid system having exactly one
remaining Hall defect, a pairwise-intersecting family of weight ten and bound
nine on the full coordinate set. Two systems were adjacent when one
coordinate was exchanged between each of two support occurrences; only
systems passing every non-Hall support check were retained.

Breadth-first search exhausted all 2,973 systems at switch radius at most six
without finding a Hall-feasible system. At radius seven it found the
certificate after 8,070 total systems had been seen. The seven switches and
frontier counts are recorded in `artifacts/radius-seven-path.txt`.

This radius statement concerns only that precisely defined switch graph. It
is not an exhaustive enumeration of all support multisets. The certificate
itself does not depend on the search history.

## Status

**REFUTED:** the explicitly listed local structural consequences do not imply
an outside edge dominating the fixed ten-clique. Thus the support-only route
fails. A stronger implication using \(K_{20}\)-minor-freeness, and Hadwiger's
conjecture at this frontier, remain open.
