# Search boundary

## Exhaustive layer

For \(n=6\), there are 20 possible triples. The enumerator scans all \(2^{20}\) bit masks and
marks each full orbit under all 720 vertex permutations. Because masks are visited in
increasing order, the retained mask is the minimum representative of its orbit. The resulting
2,136 classes agree with the independent Burnside count.

Every retained family is decided exactly at \(r=3,4\). Numerical diagonalization is run only
to count screening candidates and identify the closest-looking strict cases. The exact layer
always recomputes:

- the signed integer boundary Gram matrix;
- its integer characteristic polynomial;
- its irreducible rational factors;
- disjoint rational isolating intervals for every eigenvalue;
- an upper, lower, or exact factor-trace certificate for the Ky Fan sum.

The frozen run used interval denominator \(10^5\) throughout. No numerical candidate survived,
and the exact layer found no violation.

## Exact counts

| Ground set | Possible triples | Labeled families | Isomorphism classes |
|---:|---:|---:|---:|
| 3 | 1 | 2 | 2 |
| 4 | 4 | 16 | 5 |
| 5 | 10 | 1,024 | 34 |
| 6 | 20 | 1,048,576 | 2,136 |
| 7 | 35 | 34,359,738,368 | 7,013,320 |

The seven-vertex isomorphism count is computed exactly by Burnside's lemma:

\[
\frac1{7!}\sum_{\pi\in S_7}2^{c_3(\pi)}=7{,}013{,}320,
\]

where \(c_3(\pi)\) is the number of cycles induced by \(\pi\) on the 35 triples.

## Why the exhaustive boundary is six vertices

The implemented orbit marker allocates one bit of state per labeled family and scans the
entire mask interval. This is modest at \(2^{20}\) and infeasible at \(2^{35}\). An orderly
unlabeled hypergraph generator could avoid that scan, but enumerating and exactly certifying
7,013,320 classes would still be a materially different computation. No such backend is
included, so the exact gate stops at six vertices.

## Relation to Huang's search

Huang states that the two seven-vertex seeds were “identified through an exhaustive computer
search on seven vertices.” The paper uses that statement to motivate its \(r\ge5\)
counterexample seeds. It does not state a no-counterexample result at \(r=3,4\), give counts
for those indices, or publish a universal seven-vertex certificate. Therefore that sentence
cannot be treated as an existing \(r=3,4\) finite gate, and this package makes no claim about
what unpublished screening may have covered.

## Status

The exact search establishes a six-vertex theorem only. Extension to seven vertices and the
universal \(r=3,4\) questions remain **inconclusive**.
