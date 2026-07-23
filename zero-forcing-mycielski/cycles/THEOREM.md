# Exact zero forcing number

## 1. Statement and notation

Let \(q\ge4\). Write the vertices of the Mycielskian \(M(C_q)\) as

\[
v_0,\ldots,v_{q-1},\quad u_0,\ldots,u_{q-1},\quad w,
\]

with indices modulo \(q\). Its edges are

\[
v_iv_{i+1},\qquad u_iv_{i-1},\qquad u_iv_{i+1},\qquad wu_i.
\]

Then

\[
\boxed{Z(M(C_q))=5.}
\]

## 2. Uniform upper bound

Initially color

\[
S=\{v_0,v_1,v_2,u_0,u_1\}
\]

black. The following is a chronological list of valid forces:

\[
\begin{aligned}
v_1&\longrightarrow u_2,&
u_1&\longrightarrow w,&
u_0&\longrightarrow v_{q-1},&
v_0&\longrightarrow u_{q-1},\\
u_i&\longrightarrow v_{i+1},&
v_i&\longrightarrow u_{i+1}
&& (2\le i\le q-3).
\end{aligned}
\]

For \(q=4\), the final range is empty; for \(q=5\), it contains only
\(i=2\). The list colors every vertex, so \(Z(M(C_q))\le5\).

## 3. The matrix lower-bound principle

For a graph \(G\), let \(\mathcal S(G)\) be the real symmetric matrices whose
off-diagonal entry \(A_{xy}\) is nonzero exactly when \(xy\in E(G)\).
The standard zero-forcing kernel argument gives

\[
\operatorname{null}(A)\le Z(G)\qquad(A\in\mathcal S(G)).
\]

Indeed, if a kernel vector vanishes on a zero forcing set, the row belonging
to a forcing vertex has only one possibly nonzero summand left, and its
nonzero edge coefficient makes the forced coordinate vanish. Induction
along the forcing sequence makes the whole vector zero. Restriction to the
forcing-set coordinates is therefore injective on the kernel.

## 4. Spectral certificate for \(q\ge5,\ q\ne6\)

Let \(C\) be the adjacency matrix of \(C_q\), and put

\[
r=2\cos\frac{2\pi}{q},\qquad
s=2\cos\frac{4\pi}{q},\qquad
a=-rs,\qquad b=r+s,
\]

\[
A_0=a+2b,\qquad f=\frac{qA_0}{A_0-4}.
\]

The identities

\[
b=4\cos\frac{3\pi}{q}\cos\frac{\pi}{q}\ne0
\]

and

\[
A_0-4=-(2-r)(2-s)\ne0
\]

hold in this range. The first identity fails only at \(q=6\) among integers
\(q\ge5\). In the vertex order
\((v_0,\ldots,v_{q-1},u_0,\ldots,u_{q-1},w)\), consider

\[
X=
\begin{pmatrix}
aI+bC&C&0\\
C&I&\mathbf 1\\
0&\mathbf 1^{\mathsf T}&f
\end{pmatrix}.
\]

Because \(b\ne0\), the off-diagonal support of \(X\) is exactly the edge set
displayed in Section 1. Thus \(X\in\mathcal S(M(C_q))\).

The eigenvalues of \(C\) are

\[
\lambda_j=2\cos\frac{2\pi j}{q}\qquad(0\le j<q).
\]

The constant eigenspace has \(\lambda_0=2\). Every other real eigenspace is
orthogonal to \(\mathbf1\). On the two copies of a nonconstant
\(\lambda\)-eigenspace, \(X\) acts through

\[
B_\lambda=
\begin{pmatrix}
a+b\lambda&\lambda\\
\lambda&1
\end{pmatrix},
\qquad
\det B_\lambda
=a+b\lambda-\lambda^2
=-(\lambda-r)(\lambda-s).
\]

For \(q\ge5\), the \(r=\lambda_1=\lambda_{q-1}\) and
\(s=\lambda_2=\lambda_{q-2}\) eigenspaces are distinct and each has real
dimension two. Each contributes two kernel dimensions. No other
nonconstant eigenspace contributes.

Using normalized constant vectors in the two \(q\)-blocks, together with
the apex coordinate, gives the symmetric block

\[
K=
\begin{pmatrix}
A_0&2&0\\
2&1&\sqrt q\\
0&\sqrt q&f
\end{pmatrix}.
\]

Here

\[
\det K=f(A_0-4)-qA_0=0,
\]

while the leading \(2\times2\) minor is \(A_0-4\ne0\). Hence \(K\) has
nullity one. Altogether,

\[
\operatorname{null}(X)=2+2+1=5,
\]

and the matrix principle gives \(Z(M(C_q))\ge5\).

## 5. Integral matrix certificate for \(q=4\)

Here \(C=C_4\) has eigenvalues \(2,0,0,-2\). The integral matrix

\[
Y=
\begin{pmatrix}
C&C&0\\
C&0&\mathbf1\\
0&\mathbf1^{\mathsf T}&-2
\end{pmatrix}
\]

belongs to \(\mathcal S(M(C_4))\). On the two copies of a
\(\lambda\)-eigenspace orthogonal to \(\mathbf1\), its block is

\[
\begin{pmatrix}\lambda&\lambda\\ \lambda&0\end{pmatrix}.
\]

This is the zero matrix for the two-dimensional \(0\)-eigenspace, producing
four kernel dimensions, and it is nonsingular for \(\lambda=-2\). On the
two normalized constant vectors and the apex, the block is

\[
\begin{pmatrix}
2&2&0\\
2&0&2\\
0&2&-2
\end{pmatrix}.
\]

Its determinant is zero and its leading \(2\times2\) minor is \(-4\), so it
contributes one more kernel dimension. Thus
\(\operatorname{null}(Y)=5\), proving the lower bound at \(q=4\).

## 6. Fort certificate for \(q=6\)

A nonempty set \(F\) is a *fort* if every vertex outside \(F\) has either
zero or at least two neighbors in \(F\). Every zero forcing set meets every
fort: otherwise, immediately before the first force into \(F\), its forcing
vertex would have exactly one neighbor in \(F\). It suffices to exclude
four-vertex zero forcing sets, since every superset of a zero forcing set is
again zero forcing.

All indices below are modulo six. Start with the four pairwise disjoint
forts

\[
\{v_0,v_2,v_4\},\quad \{v_1,v_3,v_5\},\quad
\{u_0,u_2,u_4\},\quad \{u_1,u_3,u_5\}.
\]

A four-vertex zero forcing set would therefore contain exactly one vertex
from each fort and would exclude \(w\), leaving \(3^4=81\) candidates.
Consider twelve more forts:

\[
A_i=\{v_i,v_{i+3},u_i,u_{i+3},w\}\qquad(0\le i<3),
\]

\[
B_i=\{v_{i-1},v_i,v_{i+1},u_{i+3},w\}\qquad(0\le i<6),
\]

\[
D_i=\{w\}\cup\{v_j:j\not\equiv i\pmod3\}\qquad(0\le i<3).
\]

A direct count from the edge list gives the following possible values for
\(\lvert N(x)\cap F\rvert\) as \(x\) ranges outside a listed set \(F\):

| family of \(F\) | possible values |
| --- | --- |
| four parity forts | \(0,2,3\) |
| \(A_i\) | \(2\) |
| \(B_i\) | \(0,2,3\) |
| \(D_i\) | \(2,3\) |

In particular, every listed set is a fort. The exact \(3^4\) intersection
table for the \(A_i\) and \(B_i\) leaves only the six cyclic candidates

\[
T_i=\{v_i,v_{i+3},u_{i+1},u_{i+2}\}\qquad(0\le i<6).
\]

But \(T_i\cap D_{i\bmod3}=\varnothing\), so none meets every listed fort.
Thus no four-vertex zero forcing set exists. The 81-entry table and every
fort check are independently replayed by `q6_fort_certificate` in
`src/zero_forcing_mycielski/forts.py`.

Sections 2 and 4--6 prove \(Z(M(C_q))=5\) for every \(q\ge4\).

## 7. Coloring consequences

The Mycielski construction raises chromatic number by one and preserves
triangle-freeness. For completeness, a coloring of the base graph extends
by giving every shadow its original's color and giving the apex one new
color. Conversely, from a coloring of the Mycielskian, replace every
original having the apex's color by its shadow's color; this gives a proper
coloring of the base graph without the apex's color.

Therefore

\[
(\chi(M(C_q)),\omega(M(C_q)),Z(M(C_q)))=
\begin{cases}
(4,2,5),&q\text{ odd},\\
(3,2,5),&q\text{ even}.
\end{cases}
\]

For odd \(q\),

\[
\chi(M(C_q))
=4
=\left\lceil\frac{2+5+1}{2}\right\rceil,
\]

so the Annor--Howerton conjecture is attained with equality. Let
\(I=\{u_0,\ldots,u_{q-1}\}\). This set is independent and

\[
M(C_q)-I=C_q\sqcup K_1.
\]

For odd \(q\),

\[
\chi(M(C_q)-I)=3,\qquad
\omega(M(C_q)-I)=2,\qquad
Z(M(C_q)-I)=Z(C_q)+Z(K_1)=2+1=3.
\]

Here zero forcing is additive over components, two adjacent vertices force
a cycle in both directions, and a single cycle vertex cannot make the first
force. Hence \(Z(C_q)=2\), while \(Z(K_1)=1\).

Thus removal of \(I\) lowers \(\chi\) by one, lowers \(Z\) by two, and does
not lower \(\omega\). It witnesses Condition \((R)\):

\[
Z(M(C_q))-Z(M(C_q)-I)
=2
=2-\bigl(\omega(M(C_q))-\omega(M(C_q)-I)\bigr).
\]

For even \(q\), the conjectured right side is \(4\) while \(\chi=3\), so the
conjecture also holds, but not with equality. Condition \((R)\) is not
applicable because \(\chi=\omega+1\), outside its stated
\(\chi\ge\omega+2\) regime.

## 8. Scope

The theorem concerns one application of the Mycielski construction to
cycles. It makes no claim about arbitrary Mycielskians or iterated
Mycielskians. The literature audit is recorded in
[PRIOR_ART.md](PRIOR_ART.md); no claim of novelty is made.
