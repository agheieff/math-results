# Eventual \(P(n,6)\) theorem

Let \(P(n,6)\) have vertices \(u_i,v_i\), with indices modulo \(n\), and edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+6}.
\]

## Theorem

For \(n=35\) and for every integer \(n\ge37\),

\[
Z(P(n,6))=14.
\]

## Six pathwidth bases

Fix \(n\in\{37,38,39,40,41,42\}\). For an \(n\)-vertex half-set
\(X\subseteq V(P(n,6))\), color \(X\setminus\partial_X X\) by \(A\), its internal
boundary by \(B\), and its complement by \(Y\). A boundary of size at most 13 gives

\[
|Y|=n,\qquad |B|\le13,
\]

with no \(A\)-\(Y\) edge. Conversely, any such coloring gives a half-set whose boundary
is contained in the \(B\)-vertices.

A spoke-compatible column \((u_i,v_i)\) is one of

\[
AA,\ AB,\ BA,\ BB,\ BY,\ YB,\ YY.
\]

The exact verifier enumerates open column words through length 42. Its state retains the
color of \(u_0\), the first six inner colors, the latest outer color, the latest six inner
colors, and the exact \(Y\)-count. For each such state it retains only the smallest
\(B\)-count. A smaller count dominates a larger one because every future constraint and
increment depends only on the retained colors.

Appending a column checks its spoke, preceding outer edge, and step-six inner edge.
At each order \(34,\ldots,42\), closure checks the outer wrap edge and six inner wrap
edges, then requires \(|Y|=n\).

It is complete to require column zero to contain \(B\). A balanced no-\(A\)-\(Y\) coloring
with \(B=0\) would disconnect the connected graph into nonempty \(A\) and \(Y\) sets.
Any nonempty \(B\) can be rotated into column zero.

The exact closure sets are empty at all six orders \(37,\ldots,42\). Thus every half-set
there has internal boundary at least 14. Every vertex ordering has an \(n\)-vertex prefix,
so its vertex separation is at least 14. Kinnersley's equality between vertex separation
and pathwidth gives

\[
\operatorname{pw}(P(n,6))\ge14
\quad(n=37,\ldots,42).
\]

The closure set is also empty at \(n=35\), so the same argument gives
\(\operatorname{pw}(P(35,6))\ge14\). Combined with the uniform upper schedule below, this
proves the isolated equality \(Z(P(35,6))=14\).

## Six-column transfer

For \(n\ge19\), delete the spokes in columns \(n-6,\ldots,n-1\). Suppress the six exposed
outer vertices and the six exposed inner vertices. The outer path becomes the wrap edge
of a cycle shorter by six. For \(0\le r<6\), the inner path

\[
v_{n-12+r},\ v_{n-6+r},\ v_r
\]

becomes the corresponding step-six edge. The resulting graph is exactly \(P(n-6,6)\);
therefore

\[
P(n-6,6)\preccurlyeq P(n,6).
\]

Every \(n\ge37\) reduces by multiples of six to the unique

\[
b=37+((n-37)\bmod6)\in\{37,\ldots,42\}.
\]

Pathwidth is minor-monotone, and a chronological zero-forcing order has vertex
separation at most its initial set size. Hence

\[
14\le\operatorname{pw}(P(b,6))
\le\operatorname{pw}(P(n,6))
\le Z(P(n,6)).
\]

## Uniform upper schedule

Start with

\[
\{v_0,u_0,u_1,\ldots,u_{11},v_{11}\}.
\]

First use \(u_i\to v_i\) for \(1\le i\le10\), making columns \(0,\ldots,11\) black.
Then, for \(j=n-1,n-2,\ldots,12\), use

\[
u_{j+1}\to u_j,\qquad v_{j+6}\to v_j,
\]

with source indices reduced modulo \(n\). At step \(j\), columns \(0,\ldots,11\) and
\(j+1,\ldots,n-1\) are black, so both forces are legal. This proves
\(Z(P(n,6))\le14\) and completes the theorem.

## Sharp positive control

At \(n=36\), the verifier finds a boundary-13 half-set. The independently replayed word is

```text
BA YY YY YY YB BA YB YY YY YY BA AA BA YY YY YY BA AA BA YY YY YY
BA AA BA YY YY YY BA AA AA BY YY BY AA AA
```

It has 36 \(Y\)'s, 13 \(B\)'s, no \(A\)-\(Y\) edge, and exact internal boundary 13.
Consequently the six consecutive pathwidth bases cannot start at 36. This does not
determine \(Z(P(36,6))\), and it does not affect the theorem: orders congruent to zero
modulo six stop at base 42 under the minor transfer.
