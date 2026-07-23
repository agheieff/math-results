# Exact \(n=26\) verification report

## Scope and gauge

Only \(C_{26}(1,2)\) is considered. It has \(26\) vertices and \(52\) edges.
Switching the path \(01,12,\ldots,24\,25\) positive leaves the Hamilton wrap
and all \(26\) step-2 edges, hence \(52-26+1=27\) free signs. The masks
\(0,\ldots,2^{27}-1\) therefore enumerate all switching classes exactly once.

## Exact target

Set

\[
\alpha=4\left(\cos^2(\pi/26)+\cos^2(\pi/13)\right).
\]

For \(u=2\cos(\pi/13)\),

\[
\alpha=u^2+u+2,\qquad
m(u)=u^6-u^5-5u^4+4u^3+6u^2-3u-1=0.
\]

The identity \(S_{13}(u)+2=(u+2)m(u)^2\), where
\(S_k(z+z^{-1})=z^k+z^{-k}\), proves the latter relation. Eliminating \(u\)
gives

\[
p(\alpha)=0,
\]

\[
p(y)=y^6-24y^5+227y^4-1085y^3+2774y^2-3609y+1873.
\]

Exact polynomial arithmetic verifies

\[
p(u^2+u+2)
=m(u)(u^6+7u^5+15u^4+6u^3-11u^2-6u+1).
\]

Since \(\pi/13<\pi/8\),

\[
u>\sqrt{2+\sqrt2}>\frac95,\qquad
\alpha>\frac{176}{25}>7.
\]

Thus \(\alpha\) is the largest root of \(p\). Exact Sturm arithmetic isolates
all six roots in

\[
(9/5,19/10),\ (21/10,11/5),\ (16/5,33/10),\
(33/10,17/5),\ (57/10,29/5),\ (77/10,779/101).
\]

Therefore \(\alpha<779/101\).

## Exact exhaustion

For a mask \(m\), start \(s\), and \(k\ge0\), the checker uses the integer
vector \(x=A_m^{2k}e_s\). A class is strictly nonoptimal when

\[
101\lVert A_mx\rVert^2>779\lVert x\rVert^2,
\]

because the Rayleigh principle gives
\(\rho(A_m)^2>779/101>\alpha\).

The signed-64-bit pass with \(s=0\) certifies \(134{,}207{,}272\) masks and
leaves \(10{,}456\). Arbitrary-precision passes certify \(10{,}404\) more from
\(s=0\) and \(50\) from \(s=1\). The two remaining masks are

\[
55924053,\qquad 78293675.
\]

For the fast pass \(k\le13\). Since every row has absolute sum \(4\), tested
coordinates are bounded by \(4^{27}=2^{54}\), the final update by
\(4^{28}=2^{56}\), and both cross-multiplied dot products are below \(2^{120}\).
Thus signed 64-bit vectors and signed 128-bit comparisons cannot overflow.
The depth-\(40\) fallback uses `boost::multiprecision::cpp_int`.

## Extremizers

Both survivors have negative step-1 Hamilton holonomy and alternating triangle
flux. In the tree gauge, the negative wrap is fixed and
\(\sigma_{i,i+2}=\tau_i\sigma_{i,i+1}\sigma_{i+1,i+2}\), so the two choices
\(\tau_0=\pm1\) determine exactly two masks. Exact Newton identities applied
to their integer matrices give

\[
\det(xI-A)
=(x^2-4)
\left(x^{12}-24x^{10}+227x^8-1085x^6+2774x^4-3609x^2+1873\right)^2.
\]

The degree-12 factor is \(p(x^2)\). Its largest squared root is \(\alpha>7\),
whereas the remaining factor has squared root \(4\). Every other class lies
strictly above the separator, proving the frozen \(n=26\) statement.

No floating-point result is used by the certificate, and no claim is made for
any other \(n\).
