# Exact six-vertex gate

## Definitions

Let \(F\subseteq\binom V3\). For \(i<j<k\), orient its simplicial boundary by

\[
\partial[ijk]=[jk]-[ik]+[ij].
\]

Let \(B_F\) be the integer boundary matrix with facets as columns and ridges as rows, and let
\(M_F=B_F^{\mathsf T}B_F\). The positive eigenvalues of \(M_F\) are those of the simplicial
up-Laplacian \(B_FB_F^{\mathsf T}\). Arrange them decreasingly, pad with zeros, and define

\[
s_r(F)=\sum_{i=1}^r\lambda_i(M_F),\qquad
D_r(F)=\sum_{v\in V}\min\{d_F(v),r\}.
\]

The question is whether \(s_r(F)\leq D_r(F)\).

## Exhaustive result

The full \(S_6\)-action on the 20 possible triples partitions the \(2^{20}\) labeled families
into 2,136 orbits. The program visits one representative of every orbit. Relabeling changes
the oriented boundary matrix only by signed permutation matrices, so it preserves the
spectrum and degree multiset.

Exact certification gives:

\[
\begin{array}{c|rrr}
r& s_r=D_r&s_r<D_r&s_r>D_r\\ \hline
3&510&1626&0\\
4&315&1821&0
\end{array}
\]

Families on fewer than six vertices are included by adjoining isolated vertices, which
changes neither side. Therefore both inequalities hold for every 3-uniform family on at most
six vertices.

## Exact spectral certificate

For every orbit representative, the program:

1. constructs \(M_F\) over \(\mathbb Z\);
2. computes \(\det(xI-M_F)\) exactly and factors it over \(\mathbb Q\);
3. isolates every real root in a rational interval;
4. orders the intervals and bounds the sum of the largest \(r\) roots.

For a strict case, the rational upper endpoints sum to strictly less than \(D_r(F)\). For an
equality case, the selected roots contain the same number of multiplicity layers from every
root of each selected irreducible factor. Vieta's formula then evaluates their sum exactly.
No floating-point result determines a certificate status.

The numerically closest strict cases illustrate the margin.

### \(r=3\)

The representative mask 3359 has eight facets and \(D_3=16\). Its characteristic polynomial
is

\[
x(x-6)(x^3-9x^2+23x-16)(x^3-9x^2+23x-14).
\]

Exact rational isolation gives

\[
s_3(F)<\frac{1783801}{111657}
=16-\frac{2711}{111657}<16.
\]

### \(r=4\)

The representative mask 3551 has ten facets and \(D_4=22\). Its characteristic polynomial is

\[
x(x-1)^2(x-6)^2
\bigl(x^5-16x^4+95x^3-254x^2+289x-96\bigr).
\]

Exact rational isolation gives

\[
s_4(F)<\frac{2191997}{99674}
=22-\frac{831}{99674}<22.
\]

## Huang seed audit

The two seven-vertex seeds in arXiv:2607.20051v1 were also checked with the same exact engine:

| Seed | \(r=3\) | \(r=4\) | Published violating indices |
|---|---|---|---|
| \(\mathcal F_{16}\) | equality | strict | \(r=5\), verified |
| \(\mathcal F_{15}\) | strict | strict | \(r=8,9\), verified |

Thus the published seeds do not already refute \(r=3\) or \(r=4\).

## Status

**Verified:** both inequalities hold for all 3-uniform families on at most six vertices.

**Inconclusive:** neither inequality is resolved on seven vertices or in general.
