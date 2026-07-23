# General transfer theorem

Let \(k\ge1\) and \(n\ge2k+1\). The generalized Petersen graph \(P(n,k)\) has vertices
\(u_i,v_i\), with indices modulo \(n\), and edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+k}.
\]

## Uniform upper bound

For every \(n\ge2k+1\),

\[
Z(P(n,k))\le2k+2.
\]

Start with

\[
S=\{v_0,u_0,u_1,\ldots,u_{2k-1},v_{2k-1}\}.
\]

First use \(u_i\to v_i\) for \(1\le i\le2k-2\). Thus every vertex in columns
\(0,\ldots,2k-1\) is black.

Now let \(j\) descend from \(n-1\) to \(2k\). At the start of step \(j\), every column in

\[
[0,2k-1]\cup[j+1,n-1]
\]

is black. Perform

\[
u_{j+1}\to u_j,\qquad v_{j+k}\to v_j,
\]

with source indices reduced modulo \(n\).

For the outer force, the source column is already black, its spoke neighbor is black, and
its other outer neighbor is in the displayed black set. For the inner force, both
\((j+k)\bmod n\) and \((j+2k)\bmod n\) lie in that black set: without wrap they exceed \(j\),
and after wrap they lie in \([0,2k-1]\). The displayed target is therefore the unique white
neighbor in each case. Step \(j\) makes column \(j\) black and preserves the induction.
After the final step every vertex is black. Since \(|S|=2k+2\), the bound follows.

## The \(k\)-column minor

For every \(n\ge3k+1\),

\[
P(n-k,k)\preccurlyeq P(n,k).
\]

Put \(m=n-k\). Delete the \(k\) spokes \(u_i v_i\) for \(m\le i<n\). The exposed outer
vertices form the degree-two path

\[
u_{m-1},u_m,\ldots,u_{n-1},u_0.
\]

Suppressing its \(k\) internal vertices replaces it by \(u_{m-1}u_0\). For each
\(0\le r<k\), the exposed inner vertex \(v_{m+r}\) lies on the degree-two path

\[
v_{m-k+r},v_{m+r},v_r.
\]

Suppress these \(k\) inner vertices as well. The remaining vertices are
\(u_0,\ldots,u_{m-1},v_0,\ldots,v_{m-1}\); their edges are exactly those of \(P(m,k)\).
The condition \(n\ge3k+1\) ensures \(m\ge2k+1\), so the target is again a simple cubic
generalized Petersen graph in the stated parameter range.

## Finite-basis corollary

Fix \(k\ge1\) and \(B\ge2k+1\). Suppose

\[
\operatorname{pw}(P(B+r,k))\ge2k+2\qquad(0\le r<k).
\]

For each \(n\ge B\), repeatedly subtract \(k\) until reaching the unique
\(b\in[B,B+k-1]\) congruent to \(n\) modulo \(k\). Every applied minor step has source order
at least \(B+k\ge3k+1\). Pathwidth is minor-monotone and
\(\operatorname{pw}(G)\le Z(G)\), hence

\[
2k+2\le\operatorname{pw}(P(b,k))
\le\operatorname{pw}(P(n,k))
\le Z(P(n,k))
\le2k+2.
\]

Thus \(Z(P(n,k))=2k+2\) for every \(n\ge B\).
