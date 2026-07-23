# Eventual \(P(n,7)\) theorem

Let \(P(n,7)\) have vertices \(u_i,v_i\), with indices modulo \(n\), and edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+7}.
\]

## Theorem

For \(45\le n\le48\) and for every integer \(n\ge50\),

\[
Z(P(n,7))=16.
\]

No claim is made for \(n=49\).

## Exact pathwidth bases

For an \(n\)-vertex half-set \(X\subseteq V(P(n,7))\), color
\(X\setminus\partial_X X\) by \(A\), its internal boundary by \(B\), and its complement by
\(Y\). A boundary of size at most 15 gives

\[
|Y|=n,\qquad |B|\le15,
\]

with no \(A\)-\(Y\) edge. Conversely, any such coloring gives a half-set whose boundary
is contained in the \(B\)-vertices.

A spoke-compatible column \((u_i,v_i)\) is one of

\[
AA,\ AB,\ BA,\ BB,\ BY,\ YB,\ YY.
\]

The exact verifier enumerates open column words through length 56. Its state retains the
color of \(u_0\), the first seven inner colors, the latest outer color, the latest seven
inner colors, and the exact \(Y\)-count. For each key it retains only the smallest
\(B\)-count; a smaller count dominates because every future constraint and increment
depends only on the retained data.

The verifier fixes \(u_0=B\). To see completeness, suppose there were no outer \(B\).
The no-\(A\)-\(Y\) outer cycle would be all \(A\) or all \(Y\). The former forbids every
inner \(Y\). In the latter case the outer layer already contains all \(n\) required
\(Y\)'s, so every inner vertex is \(B\), contradicting \(|B|\le15<n\). Thus an outer
\(B\) exists and can be rotated to \(u_0\).

Appending a column checks its spoke, preceding outer edge, and step-seven inner edge.
At each order \(44,\ldots,56\), closure checks the outer wrap edge and seven inner wrap
edges, then requires \(|Y|=n\).

The closure sets are empty at the isolated orders \(45,\ldots,48\) and at all seven
orders \(50,\ldots,56\). Every half-set there therefore has internal boundary at least
16. Every vertex ordering has an \(n\)-vertex prefix, so its vertex separation is at
least 16. Kinnersley's equality between vertex separation and pathwidth gives

\[
\operatorname{pw}(P(n,7))\ge16
\quad(45\le n\le48\ \text{or}\ 50\le n\le56).
\]

## Seven-column transfer

For \(n\ge22\), delete the spokes in columns \(n-7,\ldots,n-1\). Suppress the seven
exposed outer vertices and seven exposed inner vertices. The outer path becomes the wrap
edge of a cycle shorter by seven. For \(0\le r<7\), the inner path

\[
v_{n-14+r},\ v_{n-7+r},\ v_r
\]

becomes the corresponding step-seven edge. The resulting graph is exactly \(P(n-7,7)\);
therefore

\[
P(n-7,7)\preccurlyeq P(n,7).
\]

Every \(n\ge50\) reduces by multiples of seven to the unique

\[
b=50+((n-50)\bmod7)\in\{50,\ldots,56\}.
\]

Pathwidth is minor-monotone, and a chronological zero-forcing order has vertex
separation at most its initial set size. Hence

\[
16\le\operatorname{pw}(P(b,7))
\le\operatorname{pw}(P(n,7))
\le Z(P(n,7)).
\]

## Uniform upper schedule

Start with

\[
\{v_0,u_0,u_1,\ldots,u_{13},v_{13}\}.
\]

First use \(u_i\to v_i\) for \(1\le i\le12\), making columns \(0,\ldots,13\) black.
Then, for \(j=n-1,n-2,\ldots,14\), use

\[
u_{j+1}\to u_j,\qquad v_{j+7}\to v_j,
\]

with source indices reduced modulo \(n\). At step \(j\), columns \(0,\ldots,13\) and
\(j+1,\ldots,n-1\) are black, so both forces are legal. This proves
\(Z(P(n,7))\le16\) and completes every claimed equality.

## The \(n=49\) positive control

For \(n=49\), repeat the seven-column block

```text
BA YY YY YY BY AA AA
```

seven times. The word has 49 \(Y\)'s, 14 \(B\)'s, no \(A\)-\(Y\) edge, and exact
internal boundary 14. This prevents the separator proof from including 49, but does not
give a 15-vertex zero forcing set or otherwise determine \(Z(P(49,7))\).
