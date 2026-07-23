# Eventual \(P(n,5)\) theorem

Let \(P(n,5)\) have vertices \(u_i,v_i\), with indices modulo \(n\), and edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+5}.
\]

## Theorem

For every integer \(n\ge29\),

\[
Z(P(n,5))=12.
\]

## Five pathwidth bases

For a 29-, 30-, 31-, 32-, or 33-vertex half-set \(X\subseteq V(P(n,5))\), color
\(X\setminus\partial_X X\) by \(A\), its internal boundary by \(B\), and its complement by
\(Y\). A boundary of size at most 11 would give

\[
|Y|=n,\qquad |B|\le11,
\]

with no \(A\)-\(Y\) edge. Conversely, any coloring with those properties gives a half-set
whose boundary is contained in the \(B\)-vertices.

A spoke-compatible column \((u_i,v_i)\) is one of

\[
AA,\ AB,\ BA,\ BB,\ BY,\ YB,\ YY.
\]

The exact verifier scans the cyclic column word. Its state retains:

- the color of \(u_0\) and the colors of \(v_0,\ldots,v_4\), for wrap closure;
- the latest outer color and the latest five inner colors;
- the accumulated \(B\)- and \(Y\)-counts.

When a column is appended, the verifier checks its spoke, the preceding outer edge, and the
step-five inner edge to the oldest retained inner color. In the final five columns it also
checks the five wrap-around inner edges, and in the final column it checks
\(u_{n-1}u_0\).

It is complete to require column zero to contain \(B\). Indeed, \(B=0\) is impossible:
\(P(n,5)\) is connected, while a balanced coloring has both \(A\) and \(Y\), and no edge may
join them. Any nonempty \(B\) can be rotated to column zero.

The finite state sets are empty after the final column for all five orders
\(29,\ldots,33\). Hence every half-set has internal boundary at least 12. Every vertex
ordering has such a half-set as its \(n\)-vertex prefix, so vertex separation, and therefore
pathwidth, is at least 12 at those five orders.

## Five-column transfer

For \(n\ge16\), delete the spokes in columns \(n-5,\ldots,n-1\). Suppress the five exposed
outer vertices and the five exposed inner vertices. This replaces the outer path by the
wrap edge of the shorter outer cycle and, for \(0\le r<5\), suppresses

\[
v_{n-10+r},v_{n-5+r},v_r.
\]

The resulting graph is exactly \(P(n-5,5)\). Thus

\[
P(n-5,5)\preccurlyeq P(n,5).
\]

Every \(n\ge29\) reduces to a unique \(b\in\{29,30,31,32,33\}\). Pathwidth is
minor-monotone, and a chronological zero-forcing order has vertex separation at most its
initial set size. Therefore

\[
12\le\operatorname{pw}(P(b,5))
\le\operatorname{pw}(P(n,5))
\le Z(P(n,5)).
\]

## Uniform upper schedule

Start with

\[
\{v_0,u_0,u_1,\ldots,u_9,v_9\}.
\]

First use \(u_i\to v_i\) for \(1\le i\le8\), making columns \(0,\ldots,9\) black.
Then, for \(j=n-1,n-2,\ldots,10\), use

\[
u_{j+1}\to u_j,\qquad v_{j+5}\to v_j
\]

with source indices reduced modulo \(n\). At step \(j\), columns \(0,\ldots,9\) and
\(j+1,\ldots,n-1\) are black. The other neighbor of each displayed source is in that black
set, so both forces are legal and column \(j\) becomes black. This proves
\(Z(P(n,5))\le12\), completing the theorem.

## Sharp half-boundary threshold

At \(n=28\), the verifier separately checks the cyclic column word

```text
YB YB YY YY YY YY YY YY YY YY YY YB YB YB YB BY AA AA AA AA AB AA
AA AA AA BY YB YB
```

It has 28 \(Y\)'s and 11 \(B\)'s, has no \(A\)-\(Y\) edge, and its corresponding half-set
has exact internal boundary 11. Thus 29 is the exact threshold for this half-boundary
argument. This witness does not determine \(Z(P(28,5))\).
