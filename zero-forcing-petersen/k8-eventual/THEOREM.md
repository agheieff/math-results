# Eventual \(P(n,8)\) theorem

Let \(P(n,8)\) have vertices \(u_i,v_i\), with indices modulo \(n\), and edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+8}.
\]

## Theorem

For every integer \(n\ge65\),

\[
Z(P(n,8))=18.
\]

No claim is made for \(n=64\).

## Exact pathwidth bases

For an \(n\)-vertex half-set \(X\subseteq V(P(n,8))\), color
\(X\setminus\partial_X X\) by \(A\), its internal boundary by \(B\), and its complement by
\(Y\). A boundary of size at most 17 gives

\[
|Y|=n,\qquad |B|\le17,
\]

with no \(A\)-\(Y\) edge. Conversely, any such coloring gives a half-set whose boundary
is contained in the \(B\)-vertices.

The exact verifier fixes \(u_0=B\). This loses no coloring. If there were no outer \(B\),
the no-\(A\)-\(Y\) outer cycle would be all \(A\) or all \(Y\). The former forbids every
inner \(Y\). In the latter case the outer layer already contains all \(n\) required
\(Y\)'s, so every inner vertex is \(B\), contradicting \(|B|\le17<n\).

The verifier partitions by the \(3^8=6561\) possible colors of
\(v_0,\ldots,v_7\). Inside one partition, a state retains the latest outer color, the
latest eight inner colors, and the exact \(Y\)-count. For each key it retains only the
smallest \(B\)-count. This is exact dominance because every future constraint and cost
increment depends only on the retained data.

Appending a column checks its spoke, preceding outer edge, and step-eight inner edge.
Closure checks the outer wrap edge and eight inner wrap edges, then requires \(|Y|=n\).
The exact reduced closure counts at orders \(64,\ldots,72\) are

\[
(97,0,0,0,0,0,0,0,0).
\]

Every half-set at orders \(65,\ldots,72\) therefore has internal boundary at least 18.
Every vertex ordering has an \(n\)-vertex prefix, so its vertex separation is at least
18. Kinnersley's equality between vertex separation and pathwidth gives

\[
\operatorname{pw}(P(n,8))\ge18\qquad(65\le n\le72).
\]

## Eight-column transfer

For \(n\ge25\), delete the spokes in columns \(n-8,\ldots,n-1\). Suppress the eight
exposed outer vertices and eight exposed inner vertices. The outer path becomes the wrap
edge of a cycle shorter by eight. For \(0\le r<8\), the inner path

\[
v_{n-16+r},\ v_{n-8+r},\ v_r
\]

becomes the corresponding step-eight edge. The result is exactly \(P(n-8,8)\), so

\[
P(n-8,8)\preccurlyeq P(n,8).
\]

Every \(n\ge65\) reduces by multiples of eight to

\[
b=65+((n-65)\bmod8)\in\{65,\ldots,72\}.
\]

Pathwidth is minor-monotone, and a chronological zero-forcing order has vertex
separation at most its initial set size. Hence

\[
18\le\operatorname{pw}(P(b,8))
\le\operatorname{pw}(P(n,8))
\le Z(P(n,8)).
\]

## Uniform upper schedule

Start with

\[
\{v_0,u_0,u_1,\ldots,u_{15},v_{15}\}.
\]

First use \(u_i\to v_i\) for \(1\le i\le14\), making columns \(0,\ldots,15\) black.
Then, for \(j=n-1,n-2,\ldots,16\), use

\[
u_{j+1}\to u_j,\qquad v_{j+8}\to v_j,
\]

with source indices reduced modulo \(n\). Both forces are legal at each step. This proves
\(Z(P(n,8))\le18\).

## The \(n=64\) separator control

Repeat eight times

```text
BA YY YY YY YY BA AA AA
```

on \(P(64,8)\). The word has 64 \(Y\)'s, 16 \(B\)'s, no \(A\)-\(Y\) edge, and exact
internal boundary 16. It explains the positive exact closure at 64 and prevents this
separator proof from starting there. It does not imply a 17-vertex zero forcing set.
