# Eleven-deletion exceptional-line theorem

## Theorem

Let \(n=2r+1\ge9\) and \(\lambda=(r+1,1^r)\). If \(H\) is an \(n\)-vertex
graph with at most eleven edges, then \(K_n-H\) is determined among all
simple graphs by

\[
\Phi_\lambda(G,x)=\operatorname{Imm}_\lambda(xI-L(G)).
\]

The first eight normalized coefficients suffice uniformly, and eight is
minimal.

## Exact complement censuses

Nauty component canonical labels and an independent Burnside average agree
on the stable counts

\[
(1,1,2,5,11,26,68,177,497,1476,4613,15216).
\]

Thus there are 22,093 stable types. Eleven edges have at most 22 active
vertices, so the first stable odd order is 23. The boundary counts are

\[
\begin{array}{c|r|r}
n&\text{exactly 11 deletions}&\text{at most 11 deletions}\\ \hline
9&3252&6261\\
11&10250&15971\\
13&14140&20803\\
15&15036&21877\\
17&15186&22057\\
19&15211&22087\\
21&15215&22092\\
23&15216&22093.
\end{array}
\]

Burnside averages the edge-orbit generating functions over every vertex
cycle type. It shares no canonical-label code with the augmentation census.

## Coefficients through \(q_8\)

Let \(D=\binom{n-1}{r}\) and write

\[
\Phi_\lambda/D=x^n+q_1x^{n-1}+\cdots+q_8x^{n-8}+\cdots.
\]

The formulas through \(q_7\) use elementary degree statistics, triangles,
matchings, and cycle covers of moved support at most seven. For \(q_8\), let
\(\mu\) range over partitions of \(s\le8\) with every part at least two.
Let \(W_{\mu,t}\) be the sum of \(e_t\) on the vertices outside every
oriented permutation cover of cycle type \(\mu\). Then

\[
q_8=e_8+\sum_{\mu}(-1)^{8-s}
 \frac{\chi^{(r+1,1^r)}(\mu,1^{n-s})}{D}W_{\mu,8-s}.
\]

Here \(s\) is the moved support. The implementation computes \(W_{\mu,t}\)
by missing-edge inclusion-exclusion. If \(P_\mu\) is the
disjoint-cycle pattern, \(F\subseteq E(H)\), \(k=|V(F)|\), and
\(a_\mu=\prod_i(2\text{ if }\mu_i=2\text{ else }\mu_i)
\prod_jm_j!\), its exact summand is

\[
\frac{(-1)^{|F|}\operatorname{emb}(F,P_\mu)
(s-k)!\binom{n-k-t}{s-k}
e_t(d_{\overline{V(F)}})}{a_\mu}.
\]

The exterior-power hook generator checks the character ratios directly.
For the new moved-support-eight types, the nonzero ratios are

\[
\begin{aligned}
\chi(6,2)/D&=-\frac{3(n-9)(n-11)}
 {16(n-6)(n-4)(n-2)},\\
\chi(5,3)/D&=\frac{(n-9)(n^2-16n+135)}
 {64(n-6)(n-4)(n-2)},\\
\chi(4,4)/D&=-\frac{n^2-16n+75}
 {4(n-6)(n-4)(n-2)},\\
\chi(2,2,2,2)/D&=\frac3{(n-4)(n-2)}.
\end{aligned}
\]

The ratios for \((8),(4,2,2),(3,3,2)\) vanish.

## Stable symbolic separation

After denominator clearing, the degree bounds for \(q_1,\ldots,q_8\) are

\[
(2,4,7,9,12,14,17,19).
\]

Indeed, for fixed \(H\), every degree of \(K_n-H\) is affine in \(n\), and
choosing vertices among the growing isolate set of \(H\) shows that \(e_t\)
has degree at most \(2t\). In a moved-support-\(s\) inclusion-exclusion term,
if the required missing edges use \(k\) vertices, the binomial factor has
degree \(s-k\) and the outside \(e_{i-s}\) has degree at most \(2(i-s)\).
Thus that term has degree at most \(2i-s-k\le2i-2\). The common character
denominators through \(q_8\) have degrees \(0,0,1,1,2,2,3,3\); after
clearing them, the diagonal \(e_i\) term gives exactly the displayed bounds.

Exact interpolation and integer-root checks give the first-difference
histogram across all \(\binom{22093}{2}=244039278\) pairs:

\[
(116415929,119623258,7417312,530662,50841,1251,23,2).
\]

There are 854 top-five identity groups. The residual pairs are separated
as follows: 1,251 by \(q_6\), 23 by \(q_7\), and two by \(q_8\). With
\(m=(n-23)/2\), the two cleared \(q_8\) differences in certificate
orientation are

\[
\begin{aligned}
-96m^3-2432m^2-21216m-63040,\\
-72m^3-1936m^2-17400m-52016.
\end{aligned}
\]

Both are strictly negative for \(m\ge0\). Their common denominator is
\(32(n-6)(n-4)(n-2)\).

There are 311 admissible odd specializations of symbolic \(q_4\)
differences, at orders in \(\{23,29,41,77\}\). Every one is separated by
\(q_5\). The JSON stores every pair, polynomial, order, edge set, and exact
separating difference.

## Boundary orders

The complete \(q_1,\ldots,q_8\) first-difference histograms are

\[
\begin{aligned}
n=9 &: (12602366,6322656,603367,62421,5417,672,31,0),\\
n=11&: (67314715,55443564,4370566,364290,34511,773,15,1),\\
n=13&: (105393288,103410165,7002602,515355,49344,1218,27,4),\\
n=15&: (114535653,116779545,7393430,529942,50781,1250,23,2),\\
n=17&: (116101787,119143380,7416320,530942,50890,1220,55,2),\\
n=19&: (116364069,119542586,7417308,530661,50642,1450,23,2),\\
n=21&: (116409052,119608043,7417312,530662,50841,1251,23,2).
\end{aligned}
\]

At \(n=9\), the full subset cycle-cover immanant recurrence independently
reproduces all eight normalized coefficients for every deepest pair.

## Determination among all graphs

The polynomial degree recovers the order. Its first normalized coefficient
is \(-2|E(G)|\), so it recovers the size. Any graph sharing the polynomial
of \(K_n-H\) has a complement with the same at-most-eleven edge count and
is one of the certified types. Pairwise separation proves the theorem.

No floating-point or randomized step is used.
