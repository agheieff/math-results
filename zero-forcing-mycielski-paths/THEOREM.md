# Exact zero forcing number

## Statement

Let \(P_n\) be the path on \(n\ge2\) vertices. Then

\[
\boxed{
Z(M(P_n))=
\begin{cases}
2,&n=2,\\
3,&n\ge3.
\end{cases}}
\]

Write the vertices of \(M(P_n)\) as

\[
v_0,\ldots,v_{n-1},\quad u_0,\ldots,u_{n-1},\quad w,
\]

where \(v_iv_{i+1}\) are the path edges, \(u_i\) is adjacent to every
neighbor of \(v_i\), and \(w\) is adjacent to every \(u_i\).

## Upper bound

For \(n\ge3\), color

\[
\{v_0,v_1,u_0\}
\]

black. The following chronological forces are valid:

\[
v_0\longrightarrow u_1,\qquad
u_0\longrightarrow w,\qquad
u_1\longrightarrow v_2,\qquad
v_1\longrightarrow u_2,
\]

followed, for \(2\le i\le n-2\), by

\[
u_i\longrightarrow v_{i+1},\qquad
v_i\longrightarrow u_{i+1}.
\]

Thus \(Z(M(P_n))\le3\). When \(n=2\), the Mycielskian is \(C_5\), whose
zero-forcing number is \(2\).

## Matrix lower-bound principle

For a graph \(G\), let \(\mathcal S(G)\) be the real symmetric matrices
whose nonzero off-diagonal entries occur exactly at the edges of \(G\).
The standard zero-forcing kernel argument gives

\[
\operatorname{null}(X)\le Z(G)\qquad(X\in\mathcal S(G)).
\]

## Generic lower bound

Assume \(n\ge4\) and \(n\ne5\). Let \(P\) be the adjacency matrix of
\(P_n\), whose simple eigenvalues are

\[
\lambda_k=2\cos\frac{k\pi}{n+1}\qquad(1\le k\le n).
\]

Put

\[
r=\lambda_2,\qquad s=\lambda_4,\qquad a=-rs,\qquad b=r+s.
\]

Here

\[
b=4\cos\frac{3\pi}{n+1}\cos\frac{\pi}{n+1}\ne0;
\]

among \(n\ge4\), the only vanishing case is \(n=5\). Define the symmetric
\(2n\)-by-\(2n\) matrix

\[
H=
\begin{pmatrix}
aI+bP&P\\
P&I
\end{pmatrix}.
\]

On the two copies of a \(\lambda\)-eigenspace of \(P\), it acts through

\[
B_\lambda=
\begin{pmatrix}
a+b\lambda&\lambda\\
\lambda&1
\end{pmatrix},
\qquad
\det B_\lambda
=-(\lambda-r)(\lambda-s).
\]

The path spectrum is simple, so \(\ker H\) has dimension exactly two,
one dimension from each of \(\lambda_2,\lambda_4\).

Let \(\boldsymbol1\in\mathbb R^n\) be the all-one vector and set
\(g=(0,\boldsymbol1)^{\mathsf T}\). An eigenvector for \(\lambda_k\) has
coordinates

\[
x^{(k)}_j=\sin\frac{k(j+1)\pi}{n+1}.
\]

For even \(k\), terms paired across the midpoint cancel, so
\(\boldsymbol1^{\mathsf T}x^{(k)}=0\). A kernel vector of \(H\) in this
mode is \((x^{(k)},-\lambda_kx^{(k)})\). Hence

\[
g\perp\ker H.
\]

Because \(H\) is symmetric, \(g\in\operatorname{im}H\). Choose \(z\) with
\(Hz=g\), put \(f=g^{\mathsf T}z\), and define

\[
X=
\begin{pmatrix}
H&g\\
g^{\mathsf T}&f
\end{pmatrix}.
\]

The condition \(b\ne0\) shows that \(X\in\mathcal S(M(P_n))\). The two
vectors \((k,0)\), for \(k\in\ker H\), remain in \(\ker X\), and

\[
\binom{z}{-1}\in\ker X.
\]

These give three independent kernel vectors. Therefore
\(Z(M(P_n))\ge3\).

## Exceptional lower bounds

A nonempty set \(F\) is a *fort* if every vertex outside \(F\) has either
zero or at least two neighbors in \(F\). Every zero forcing set intersects
every fort.

For \(n\in\{3,5\}\), the following three sets are pairwise disjoint forts:

\[
\{v_i:i\text{ even}\},\qquad
\{u_i:i\text{ even}\},\qquad
\{v_i,u_i:i\text{ odd}\}\cup\{w\}.
\]

Thus a zero forcing set has at least three vertices. Together with the
generic argument and the upper bound, this proves the formula.

## Coloring consequence

For \(n\ge2\), the path has chromatic number and clique number \(2\).
The Mycielski construction raises chromatic number by one and preserves
triangle-freeness, so

\[
\chi(M(P_n))=3,\qquad\omega(M(P_n))=2.
\]

For either possible value of \(Z\),

\[
3=
\left\lceil\frac{\omega(M(P_n))+Z(M(P_n))+1}{2}\right\rceil.
\]

Hence the Annor--Howerton conjectured bound is sharp on every path
Mycielskian \(M(P_n)\), \(n\ge2\).
