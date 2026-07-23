# Exact \(n=22\) verification report

## Scope and gauge

Only \(C_{22}(1,2)\) is considered. It has \(22\) vertices and \(44\) edges.
Switching the path \(01,12,\ldots,20\,21\) positive leaves the Hamilton wrap
and all \(22\) step-2 edges, hence \(44-22+1=23\) free signs. The masks
\(0,\ldots,2^{23}-1\) therefore enumerate all switching classes exactly once.

## Exact target

Set

\[
\alpha=4\left(\cos^2(\pi/22)+\cos^2(\pi/11)\right).
\]

For \(u=2\cos(\pi/11)\),

\[
\alpha=u^2+u+2,\qquad
m(u)=u^5-u^4-4u^3+3u^2+3u-1=0.
\]

The identity \(S_{11}(u)+2=(u+2)m(u)^2\), where
\(S_k(z+z^{-1})=z^k+z^{-k}\), proves the latter relation. Eliminating \(u\)
gives

\[
p(\alpha)=0,\qquad
p(y)=y^5-20y^4+149y^3-519y^2+851y-529.
\]

Exact polynomial arithmetic verifies

\[
p(u^2+u+2)
=m(u)(u^5+6u^4+10u^3+u^2-6u-1).
\]

Since \(\pi/11<\pi/8\),

\[
u>\sqrt{2+\sqrt2}>\frac95,\qquad
\alpha=u^2+u+2>\frac{176}{25}>7.
\]

Here the middle inequality follows by squaring and using
\((31/25)^2<2\). Thus \(\alpha\) is the largest root of \(p\). Rational Sturm
arithmetic isolates all five roots in

\[
(9/5,19/10),\ (23/10,12/5),\ (31/10,16/5),\
(5,51/10),\ (38/5,3801/500).
\]

Thus \(\alpha<3801/500\).

## Exact exhaustion

For a mask \(m\), start \(s\), and \(k\ge0\), the checker uses the integer
vector \(x=A_m^{2k}e_s\). A class is strictly nonoptimal when

\[
500\lVert A_mx\rVert^2>3801\lVert x\rVert^2,
\]

because the Rayleigh principle gives
\(\rho(A_m)^2>3801/500>\alpha\).

The signed-64-bit pass with \(s=0\) certifies \(8{,}388{,}070\) masks and
leaves \(538\). Arbitrary-precision passes certify \(522\) more from \(s=0\)
and \(14\) from \(s=1\). The two remaining masks are

\[
3495253,\qquad 4893355.
\]

For the fast pass \(k\le13\). Since every row has absolute sum \(4\), tested
coordinates are bounded by \(4^{27}=2^{54}\), the final update by
\(4^{28}=2^{56}\), and both cross-multiplied dot products are below \(2^{123}\).
Thus signed 64-bit vectors and signed 128-bit comparisons cannot overflow.
The fallback uses `boost::multiprecision::cpp_int`.

## Extremizers

Both survivors have negative step-1 Hamilton holonomy and alternating triangle
flux. In the tree gauge, the negative wrap is fixed and
\(\sigma_{i,i+2}=\tau_i\sigma_{i,i+1}\sigma_{i+1,i+2}\), so the two choices
\(\tau_0=\pm1\) determine exactly two masks. Exact Newton identities applied
to their integer matrices give

\[
\det(xI-A)
=(x^2-4)
\left(x^{10}-20x^8+149x^6-519x^4+851x^2-529\right)^2.
\]

The degree-ten factor is \(p(x^2)\). The Sturm isolation shows that the largest
squared eigenvalue is \(\alpha\). Every other class has spectral radius
strictly above the separator, proving the frozen \(n=22\) statement.

No floating-point result is used by the certificate, and no claim is made for
any other \(n\).
