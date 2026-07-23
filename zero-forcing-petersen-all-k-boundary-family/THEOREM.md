# Exact half-boundary construction on \(P(km,k)\)

Let \(P(n,k)\) have vertices \(u_i,v_i\), with indices modulo \(n\), and edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+k}.
\]

## Theorem

For every pair of integers \(k,m\ge3\), the graph \(P(km,k)\) has an
\(km\)-vertex half-set \(X\) whose exact internal boundary has size \(2m\).

## Odd \(k\)

Write \(k=2r+1\). Repeat \(m\) times the \(k\)-column word

\[
BA\ (YY)^r\ BY\ (AA)^{r-1}.
\]

One block contains \(2r+1=k\) symbols \(Y\) and two symbols \(B\).

## Even \(k\)

Write \(k=2r\). Since \(k\ge3\), this case has \(r\ge2\). Repeat \(m\) times

\[
BA\ (YY)^r\ BA\ (AA)^{r-2}.
\]

Again, one block contains \(2r=k\) symbols \(Y\) and two symbols \(B\).

## Exact boundary

In either parity, let \(X\) be the vertices whose symbols are \(A\) or \(B\).
The repeated word has \(km=n\) symbols \(Y\) among the \(2n\) vertices, so \(|X|=n\).

On the outer cycle, the two \(B\)'s separate every \(A\)-run from every \(Y\)-run.
No spoke is colored \(A\)-\(Y\). Finally, adding \(k\) to a column index moves to the
same position in the next repeated block, so every inner edge has equal endpoint colors.
There is therefore no \(A\)-\(Y\) edge.

Every displayed \(B\) is an outer vertex adjacent to a \(Y\)-vertex. Every \(A\)-vertex
has only \(A\)- or \(B\)-neighbors. Hence the internal boundary of \(X\) is exactly the
two \(B\)'s per block:

\[
|\partial_X X|=2m.
\]

## Infinite square refutation

Take \(m=k\). Then \(P(k^2,k)\) has a half-set with exact boundary \(2k<2k+2\).
Moreover,

\[
k^2\ge6k-1
\]

for every \(k\ge6\). Thus the proposed statement that every half-set in every
\(P(n,k)\) with \(n\ge6k-1\) has boundary at least \(2k+2\) fails for infinitely many
values of \(k\).

This conclusion is limited to that separator statement. It makes no claim that
\(Z(P(k^2,k))\le2k\).
