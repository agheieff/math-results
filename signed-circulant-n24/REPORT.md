# Exact \(n=24\) verification report

## Scope and gauge

Only \(C_{24}(1,2)\) is considered. It has \(24\) vertices and \(48\) edges.
Switching the path \(01,12,\ldots,22\,23\) positive leaves the Hamilton wrap
and all \(24\) step-2 edges, hence \(48-24+1=25\) free signs. The masks
\(0,\ldots,2^{25}-1\) therefore enumerate all switching classes exactly once.

## Exact target

Set

\[
\alpha=4\left(\cos^2(\pi/24)+\cos^2(\pi/12)\right)
=4+\sqrt3+\frac{\sqrt6+\sqrt2}{2}.
\]

Writing \(z=\alpha-4\), direct elimination gives

\[
z^2+1=\sqrt3(2z+1)
\]

and hence

\[
p(\alpha)=0,\qquad
p(y)=y^4-16y^3+86y^2-188y+142.
\]

The checker verifies the polynomial identity

\[
\bigl((y-4)^2+1\bigr)^2-3\bigl(2(y-4)+1\bigr)^2=p(y).
\]

The rational bounds

\[
\sqrt3>\frac53,\qquad \sqrt6>\frac{12}{5},\qquad
\sqrt2>\frac75
\]

give \(\alpha>227/30>7\), identifying it as the largest root of \(p\).
Exact Sturm arithmetic isolates all four roots in

\[
(17/10,9/5),\quad (27/10,14/5),\quad (19/5,39/10),\quad
(7663/1000,958/125).
\]

Thus \(\alpha<958/125\).

## Exact exhaustion

For a mask \(m\), start \(s\), and \(k\ge0\), the checker uses the integer
vector \(x=A_m^{2k}e_s\). A class is strictly nonoptimal when

\[
125\lVert A_mx\rVert^2>958\lVert x\rVert^2,
\]

because the Rayleigh principle gives
\(\rho(A_m)^2>958/125>\alpha\).

The signed-64-bit pass with \(s=0\) certifies \(33{,}551{,}968\) masks and
leaves \(2{,}464\). Arbitrary-precision passes certify \(2{,}412\) more from
\(s=0\) and \(50\) from \(s=1\). The two remaining masks are

\[
13981013,\qquad 19573419.
\]

For the fast pass \(k\le13\). Since every row has absolute sum \(4\), tested
coordinates are bounded by \(4^{27}=2^{54}\), the final update by
\(4^{28}=2^{56}\), and both cross-multiplied dot products are below \(2^{120}\).
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
=\left(x^4-8x^2+14\right)^2
\left(x^8-16x^6+86x^4-188x^2+142\right)^2.
\]

The degree-eight factor is \(p(x^2)\). The other squared-eigenvalue roots are
\(4\pm\sqrt2<6\), whereas \(\alpha>7\). Thus the Sturm isolation shows that
the spectral radius of both survivors is exactly \(\sqrt\alpha\). Every other
class lies strictly above the separator, proving the frozen \(n=24\) statement.

No floating-point result is used by the certificate, and no claim is made for
any other \(n\).
