# Exact \(H_3\) obstruction

## Problem

Let \(m_3\) be the supremum of the normalized surface measure of measurable
zero-sum-free subsets of \(S^2\). For a finite \(F\subset S^2\), let \(H(F)\) be the
3-uniform hypergraph whose edges are the unordered triples summing to zero. Rotation averaging
gives

\[
  m_3\leq \frac{\alpha(H(F))}{|F|}.
\]

Thus an improvement on \(m_3\leq 2/3\) requires a finite configuration with independence ratio
strictly below \(2/3\).

## Exact \(H_3\) configuration

Write \(\phi=(1+\sqrt5)/2\). The program enumerates the 30 normalized roots

\[
\{\pm e_1,\pm e_2,\pm e_3\}
\;\cup\;
\left\{
\tfrac12(\pm1,\pm\phi,\pm\phi^{-1})
\text{ under cyclic coordinate permutations}
\right\}.
\]

All arithmetic in this part is in
\(\mathbb Q(\phi)=\{a+b\phi:a,b\in\mathbb Q\}\), reduced using
\(\phi^2=\phi+1\). Exhaustive exact enumeration verifies:

- the 30 roots are distinct, unit, and antipodally closed;
- exactly 20 unordered triples sum to zero;
- every root lies in exactly two such triples.

With the enumeration order in `roots.py`, the following ten zero-sum triples form a perfect
matching:

```text
(0,10,13) (1,7,8)   (2,16,21) (3,15,18) (4,23,29)
(5,24,26) (6,17,28) (9,14,27) (11,20,25) (12,19,22)
```

Every independent set omits at least one vertex from each matching edge, so its size is at most
20. The following 20 vertices contain no zero-sum triple:

```text
2 3 4 5 6 7 8 9 10 11 12 13 18 19 20 21 26 27 28 29
```

Consequently

\[
  \alpha(H(H_3))=20,\qquad
  \frac{\alpha(H(H_3))}{|H_3|}=\frac{20}{30}=\frac23.
\]

This is an exact obstruction: \(H_3\) certifies the existing \(2/3\) upper bound but cannot
improve it.

## A natural 90-point gluing

The rotational icosahedral orbit of the standard \(A_3\) configuration consists of five
12-point configurations with a 60-point union \(A_{60}\). For \(H_3\cup A_{60}\), the recovered
zero-sum hypergraph has no cross-component edges and decomposes as

\[
  H(H_3)\;\sqcup\;5H(A_3).
\]

Its component profiles are \((30,20)\) and five copies of \((12,8)\), where each pair records
(vertices, edges). Hence it has 90 vertices, 60 edges, and independence number
\(20+5\cdot8=60\), again giving \(2/3\). This decomposition is part of the floating geometric
search, not the exact \(\mathbb Q(\phi)\) certificate.

## Result

**Verified:** the normalized \(H_3\) root system has independence ratio exactly \(2/3\).

**Inconclusive:** the bounded gluing search found no ratio below \(2/3\), but it neither
exhausts all finite configurations on \(S^2\) nor supplies a global lower bound for their
independence ratios.
