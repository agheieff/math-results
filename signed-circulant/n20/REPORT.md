# Exact verification report

## 1. Source statement and scope

Suvagiya defines \(C_n(1,2)\) on \(\mathbb Z/n\mathbb Z\), with step-1 and
step-2 edges, and defines

\[
\rho_-(n)=2\sqrt{\cos^2(\pi/n)+\cos^2(2\pi/n)}.
\]

Conjecture 3 of arXiv:2607.18334v1 says that
\(\min_\sigma\rho(A_\sigma)=\rho_-(n)\) for every even \(n\ge8\). The paper
reports exhaustive floating-point checks through \(n=18\). This report freezes
only \(n=20\).

## 2. Complete switching gauge

Switching by \(\varepsilon:V\to\{-1,1\}\) replaces an edge sign by
\(\sigma'(uv)=\varepsilon(u)\sigma(uv)\varepsilon(v)\). If
\(D=\operatorname{diag}(\varepsilon)\), then

\[
A_{\sigma'}=D A_\sigma D,
\]

so switching preserves the spectrum.

Take the spanning path

\[
T=\{01,12,\ldots,18\,19\}.
\]

Fix \(\varepsilon(0)=1\) and recursively put
\(\varepsilon(i+1)=\varepsilon(i)\sigma(i,i+1)\). This makes every edge of
\(T\) positive. The gauge is unique: a switching preserving all tree signs is
constant on the connected tree, and its two constant choices induce the same
edge signing.

The graph has \(20\) vertices and \(40\) edges. Its cotree consists of the
step-1 edge \(19\,0\) and all \(20\) step-2 edges. Thus the \(21\) cotree
signs enumerate all \(2^{40-20+1}=2^{21}\) switching classes exactly once.
Masks run deterministically from \(0\) through \(2^{21}-1\); bit zero is the
edge \(19\,0\), and bit \(i+1\) is the edge \(\{i,i+2\}\).

## 3. Exact target and separator

Write

\[
\alpha=\rho_-(20)^2
=\frac{9+\sqrt5+\sqrt{10+2\sqrt5}}2.
\]

Eliminating the radicals gives

\[
p(\alpha)=0,\qquad
p(y)=y^4-18y^3+114y^2-302y+281.
\]

Indeed,

\[
\bigl((2y-9)^2-5\bigr)^2-5(4y-16)^2=16p(y).
\]

The exact Sturm sequence used by the checker isolates one root of \(p\) in
each of \((2,3),(3,4),(4,5),(7,8)\), with none in \((5,7)\). The displayed
radical is the root in \((7,8)\). The rational estimates

\[
2<\sqrt5<\frac94,\qquad
3<\sqrt{10+2\sqrt5}<\frac{77}{20}
\]

give

\[
7<\alpha<\frac{151}{20}<\frac{38}{5}.
\]

## 4. Exhaustive lower certificates

For a mask \(m\), a start vertex \(s\), and \(k\ge0\), the enumerator takes

\[
x=A_m^{2k}e_s.
\]

All coordinates are integers. It accepts the class as strictly nonoptimal when

\[
5\lVert A_mx\rVert^2>38\lVert x\rVert^2.
\]

The Rayleigh principle then gives

\[
\rho(A_m)^2
=\lambda_{\max}(A_m^2)
\ge\frac{x^\mathsf{T}A_m^2x}{x^\mathsf{T}x}
>\frac{38}{5}>\alpha.
\]

The complete run certifies \(2{,}096{,}980\) masks using signed 64-bit vectors
and 128-bit dot products with \(s=0\), leaving \(172\). Arbitrary-precision
integer vectors with \(s=0\) certify another \(162\), and \(s=1\) certifies
eight more. No floating-point operation occurs in this enumeration.

There is no overflow in the fast pass. Since the graph is \(4\)-regular,
\(\lVert A^j e_s\rVert_1\le4^j\). At its largest exponent \(j=29\), every
coordinate is therefore at most \(4^{29}=2^{58}<2^{63}\). Moreover,
\(\lVert A^{29}e_s\rVert_2^2\le2^{116}\), so multiplying either squared norm
by \(5\) or \(38\) remains below the signed 128-bit limit.

The two remaining masks are

\[
873813,\qquad 1223339.
\]

Both have negative step-1 Hamilton holonomy and alternating triangle fluxes;
they are exactly the two twisted classes \((\tau_0,\alpha_{\rm hol})=(\pm1,-1)\)
from the source paper.

## 5. Independent extremal check

A separate pure-Python routine builds each remaining integer matrix and
computes its characteristic polynomial from the exact traces
\(\operatorname{tr}(A^j)\) using Newton identities. Both give

\[
\det(xI-A)
=(x^2-2)^2
\left(x^8-18x^6+114x^4-302x^2+281\right)^2.
\]

The degree-eight factor is \(p(x^2)\). The Sturm isolation above shows that
its largest squared root is exactly \(\alpha\); the other factor has squared
root \(2\). Hence both remaining classes have spectral radius
\(\sqrt\alpha=\rho_-(20)\).

Combining this with the exhaustive strict lower certificates proves the frozen
\(n=20\) statement. It supplies no induction or claim for any other \(n\).

## 6. Trust boundary

Floating-point eigensolvers were used only to choose a convenient rational
separator and witness-depth cutoff. Neither their values nor their ordering is
used by the final checker. The final result depends on:

- the short gauge proof above;
- integer sparse matrix-vector multiplication in `cpp/enumerate.cpp`;
- exact integer and rational arithmetic in `signed_circulant/exact.py`; and
- the system C++ compiler and Boost.Multiprecision implementation.
