# Bi-infinite strip theorem

## Convention

Only finite initial black sets are allowed. A vertex belongs to the finitary closure of \(S\)
when some finite legal forcing sequence from \(S\) colors it black. A finite set is zero
forcing when every vertex has such a finite derivation. The minimum size of such a set is
\(Z_{\mathrm{fin}}\).

This avoids any appeal to a completed transfinite process: every individual conclusion has a
finite certificate.

## Theorem

For the bi-infinite graph

\[
V=\{u_i,v_i:i\in\mathbb Z\},\qquad
E=\{u_i u_{i+1},u_i v_i,v_i v_{i+3}:i\in\mathbb Z\},
\]

one has

\[
Z_{\mathrm{fin}}(\mathcal P_3)=8.
\]

### Lower bound

Consider the adjacency equations

\[
x_{u_{i-1}}+x_{u_{i+1}}+x_{v_i}=0,\qquad
x_{u_i}+x_{v_{i-3}}+x_{v_{i+3}}=0.
\]

The first gives

\[
x_{v_i}=-x_{u_{i-1}}-x_{u_{i+1}}.
\]

Substitution into the second gives

\[
x_{u_{i+4}}
=x_{u_i}-x_{u_{i-4}}-x_{u_{i-2}}-x_{u_{i+2}}.
\]

Thus arbitrary values at

\[
u_{-4},u_{-3},\ldots,u_3
\]

extend uniquely in both directions to a solution, and every solution is obtained this way.
The solution space therefore has dimension eight.

Let \(S\) contain at most seven vertices. Evaluation on \(S\) is a linear map from this
eight-dimensional solution space to a space of dimension at most seven, so it has a nonzero
kernel vector \(x\). Hence \(x\) vanishes on \(S\).

If a black source has a unique white neighbor, all other terms in its adjacency equation are
already zero, so the remaining coordinate must also be zero. Induction along any finite
forcing derivation shows that \(x\) vanishes at every vertex in the finitary closure of \(S\).
Since \(x\ne0\), that closure is not the whole graph. Therefore
\(Z_{\mathrm{fin}}(\mathcal P_3)\ge8\).

### Upper bound

Start with \(u_0,\ldots,u_7\). First perform

\[
u_i\longrightarrow v_i\quad(1\le i\le6).
\]

Then the following forces are valid:

\[
v_3\longrightarrow v_0,\qquad
v_4\longrightarrow v_7,\qquad
u_0\longrightarrow u_{-1},\qquad
u_7\longrightarrow u_8.
\]

Consequently, whenever eight consecutive outer vertices are black, the outer vertex at each
end of the block belongs to their closure. Translation and monotonicity let this lemma be
iterated: every \(u_i\) has a finite derivation. Once \(u_{i-1},u_i,u_{i+1}\) are black,
\(u_i\) forces \(v_i\) if needed. Hence every \(v_i\) also has a finite derivation, proving
\(Z_{\mathrm{fin}}(\mathcal P_3)\le8\).

## Finite minor lemma

For \(n\ge10\), delete the spokes in three consecutive columns
\(n-3,n-2,n-1\). The exposed outer vertices form one degree-two path and the exposed inner
vertices form three degree-two paths. Suppressing those six vertices shortens the outer cycle
by three and each inner residue path by one, producing exactly \(P(n-3,3)\). Thus

\[
P(n-3,3)\preccurlyeq P(n,3).
\]

This is potentially useful with a minor-monotone lower-bound parameter, but ordinary zero
forcing itself cannot simply be transferred through this minor statement.
