# Frozen bounded search

## Geometric construction

The exact \(H_3\) roots are converted to binary floating point only after their exact
certificate is complete. The search layer deduplicates points and recognizes zero sums at
tolerance \(10^{-7}\), then sends the resulting finite hypergraph to OR-Tools CP-SAT. CP-SAT
must report `OPTIMAL`; its independence number is exact conditional on the recovered
hypergraph.

For shared-\(x\)-axis rotations, a pair of unit points can occur in a zero-sum triple exactly
when its inner product is \(-1/2\). Its third point is then the unique completion
\(-x-y\). The critical-angle generator includes:

- moving-root/fixed-root coincidences;
- a moving root aligned with a completion of two fixed roots;
- a fixed root aligned with a rotated completion of two moving roots.

Angles producing the same rotated configuration are deduplicated. This yields 3 distinct
\(A_3/A_3\), 6 \(H_3/A_3\), and 6 \(H_3/H_3\) critical orientations.

## Enumerated families

| Family | Cases | Distinct outcomes | \(=2/3\) | Best \((n,e,\alpha;\alpha/n)\) |
|---|---:|---:|---:|---|
| \(A_3\) critical subsets | 7 | 4 | 6 | \((12,8,8;2/3)\) |
| fixed \(H_3\) plus \(A_3\) critical subsets | 64 | 17 | 9 | \((30,20,20;2/3)\) |
| \(H_3\) critical subsets | 63 | 25 | 13 | \((30,20,20;2/3)\) |
| fixed \(H_3\), mixed critical subsets | 2048 | 304 | 32 | \((30,20,20;2/3)\) |
| generic shared-axis pairs | 3 | 3 | 0 | \((58,40,40;20/29)\) |
| generic-offset \(A_3\) clusters | 7 | 4 | 0 | \((52,40,36;9/13)\) |
| generic-offset \(H_3\) clusters | 63 | 25 | 0 | \((130,96,88;44/65)\) |
| natural icosahedral orbits | 28 | 19 | 12 | \((60,40,40;2/3)\) |

The mixed family fixes one \(H_3\), then chooses an arbitrary subset of five nontrivial
critical \(H_3\) orientations and six critical \(A_3\) orientations, giving \(2^{11}=2048\)
cases.

The generic angle is \(\pi/\sqrt2\). The generic-offset families place all internally critical
orientations of one type at that common offset. These samples probe noncritical chambers; they
are not an exhaustive chamber decomposition.

The icosahedral family uses the computed 60-element rotational symmetry group and contains:

- the orbit of the standard \(A_3\) configuration, comprising five configurations;
- all 15 nonempty unions of the \(I_{12},D_{20},H_{30},A_{60}\) natural shells;
- six orbit unions from shared-axis \(A_3\) critical seeds;
- six orbit unions from shared-axis \(H_3\) critical seeds.

The \(H_{30}\cup A_{60}\) shell union is the 90-point decomposition described in
[REPORT.md](REPORT.md).

## Search boundary

No enumerated hypergraph has independence ratio below \(2/3\). This is not a proof that no such
finite configuration exists:

- only the listed gluing and orbit families were searched;
- generic chambers were sampled rather than exhaustively decomposed;
- point coincidences and zero sums in the search layer are recovered numerically;
- no interval or symbolic certification surrounds the floating critical angles.

Accordingly the broad search status is **inconclusive**. The exact \(H_3\) obstruction is
independent of these limitations.
