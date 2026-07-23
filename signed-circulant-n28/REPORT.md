# Exact \(n=28\) verification report

## Scope and gauge

Only \(C_{28}(1,2)\) is considered. It has \(28\) vertices and \(56\) edges.
Switching the path \(01,12,\ldots,26\,27\) positive leaves the Hamilton wrap
and all \(28\) step-2 edges, hence \(56-28+1=29\) free signs. The masks
\(0,\ldots,2^{29}-1\) therefore enumerate all switching classes exactly once.

## Exact target

Set

\[
\alpha=4\left(\cos^2(\pi/28)+\cos^2(\pi/14)\right).
\]

For \(u=2\cos(\pi/14)\),

\[
\alpha=u^2+u+2,\qquad
m(u)=u^6-7u^4+14u^2-7=0.
\]

The identity \(S_{14}(u)+2=u^2m(u)^2\), where
\(S_k(z+z^{-1})=z^k+z^{-k}\), proves the latter relation. The polynomial
\(m\) is irreducible by Eisenstein at \(7\). Eliminating \(u\) gives

\[
p(\alpha)=0,
\]

\[
p(y)=y^6-26y^5+270y^4-1434y^3+4111y^2-6030y+3529.
\]

Exact polynomial arithmetic verifies

\[
p(u^2+u+2)
=m(u)(u^6+6u^5+8u^4-8u^3-13u^2+6u+1).
\]

Also,

\[
p(y+2)=y^6-14y^5+70y^4-154y^3+147y^2-42y-7,
\]

so \(p\) is irreducible by Eisenstein at \(7\). Since \(\pi/14<\pi/8\),

\[
u>\sqrt{2+\sqrt2}>\frac95,\qquad
\alpha>\frac{176}{25}>7.
\]

Exact Sturm arithmetic isolates all six roots of \(p\) in

\[
(9/5,19/10),\ (14/5,29/10),\ (18/5,37/10),\
(19/5,39/10),\ (6,61/10),\ (7,969/125).
\]

Therefore \(\alpha\) is the largest root and \(\alpha<969/125\).

## Exact exhaustion

For a mask \(m\), start \(s\), and \(k\ge0\), the checker uses the integer
vector \(x=A_m^{2k}e_s\). A class is strictly nonoptimal when

\[
125\lVert A_mx\rVert^2>969\lVert x\rVert^2,
\]

because the Rayleigh principle gives
\(\rho(A_m)^2>969/125>\alpha\).

The signed-64-bit pass with \(s=0\) certifies \(536{,}828{,}396\) masks and
leaves \(42{,}516\). The arbitrary-precision pass from \(s=0\) certifies
\(42{,}364\) more and leaves \(152\). A second arbitrary-precision pass from
\(s=1\) certifies \(150\), leaving exactly

\[
223696213,\qquad 313174699.
\]

For the fast pass \(k\le13\). Every row has absolute sum \(4\), so tested
vector coordinates are bounded by \(4^{26}=2^{52}\), tested image coordinates
by \(4^{27}=2^{54}\), and the final update by \(4^{28}=2^{56}\). Moreover,

\[
125\cdot28\cdot2^{108}<2^{120},\qquad
969\cdot28\cdot2^{104}<2^{119}.
\]

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
=(x^2-2)^2
\left(x^{12}-26x^{10}+270x^8-1434x^6+
4111x^4-6030x^2+3529\right)^2.
\]

The degree-12 factor is \(p(x^2)\). Its largest squared root is \(\alpha>7\),
whereas the remaining factor has squared root \(2\). Every other class lies
strictly above the separator, proving the frozen \(n=28\) statement.

No floating-point result is used by the certificate, and no claim is made for
any other \(n\).
