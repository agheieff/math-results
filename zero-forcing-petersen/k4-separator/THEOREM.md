# Half-set boundary theorem for \(P(n,4)\)

Write

\[
P(n,4)=\bigl(\{u_i,v_i:i\in\mathbb Z/n\mathbb Z\},
\{u_iu_{i+1},u_iv_i,v_iv_{i+4}\}\bigr).
\]

For \(X\subseteq V(P(n,4))\), let

\[
\partial_X X=\{x\in X:N(x)\not\subseteq X\}.
\]

Then

\[
|X|=n,\quad n\ge23\quad\Longrightarrow\quad|\partial_X X|\ge10.
\]

## Separator coloring

If a counterexample has \(B=\partial_X X\), color \(X\setminus B\) by \(A\), \(B\) by \(B\),
and the complement by \(Y\). No edge joins \(A\) to \(Y\), and

\[
|B|=b\le9,\qquad |A|=n-b,\qquad |Y|=n.
\]

Conversely, any coloring with these cardinalities and no \(A\)-\(Y\) edge gives a half-set
whose boundary is contained in its \(B\)-vertices. A spoke-compatible column is one of

\[
AA,\ AB,\ BA,\ BB,\ BY,\ YB,\ YY.
\]

A state records four consecutive columns. There are 1,481 states and 7,383 valid transitions.
Closed walks of length \(n\), weighted by the number of \(B\)'s and by
\(\#Y-1\) in each appended column, encode exactly the balanced cyclic colorings. The exact
transfer recurrence excludes \(b\le9\) for every \(23\le n\le162\).

## Reduction above 162

Call a column dirty if it contains \(B\), and let \(d\) be the number of dirty columns. Then
\(1\le d\le9\); every clean column is \(AA\) or \(YY\), and consecutive clean columns have
the same color. Thus the clean columns of either color occupy at most \(d\) runs.

Let \(r_A,r_Y\) count clean \(AA,YY\) columns, and let \(a_D,y_D\) count \(A,Y\) vertices in
dirty columns. Since \(a_D,y_D\le d\le9\),

\[
r_A=\frac{n-b-a_D}{2}\ge\frac{n-18}{2},\qquad
r_Y=\frac{n-y_D}{2}\ge\frac{n-9}{2}.
\]

For \(n\ge163\), both colors therefore have a clean run of length at least nine. Delete the
central column of such a run. The new outer edge has equal-colored endpoints. The only new
step-four inner edges join

\[
(i-4,i+1),\ (i-3,i+2),\ (i-2,i+3),\ (i-1,i+4),
\]

all within the same nine-column run, so no \(A\)-\(Y\) edge is created. Deleting one \(AA\)
column and one \(YY\) column preserves \(b\) and changes

\[
(|A|,|B|,|Y|)=(n-b,b,n)
\quad\text{to}\quad
(n-2-b,b,n-2).
\]

Repeated deletion reaches order 161 or 162, contradicting the finite exclusion.

## Sharpness and consequences

At \(n=22\), the cyclic column word

\[
(YB)^3\,(YY)^7\,(YB)^3\,BY\,(AA)^3\,AB\,(AA)^3\,BY
\]

is balanced, has no \(A\)-\(Y\) edge, and contains nine \(B\)'s. Hence 23 is the exact
eventual threshold.

Every vertex order has an \(n\)-vertex prefix, so the theorem gives
\(\operatorname{pw}(P(n,4))\ge10\). A chronological zero-forcing order has vertex separation
at most the initial set size, hence

\[
Z(P(n,4))\ge10\qquad(n\ge23).
\]

The separate exact cyclic-orbit census in
[`../zero-forcing-petersen-k4`](../zero-forcing-petersen-k4/REPORT.md) proves
\(Z(P(n,4))=10\) for \(18\le n\le22\) and supplies a ten-vertex forcing set for every
\(n\ge9\). Combining the two certificates yields

\[
\boxed{Z(P(n,4))=10\quad\text{for every }n\ge18.}
\]
