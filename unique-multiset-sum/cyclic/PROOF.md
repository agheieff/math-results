# Proof

## Frozen definition

Let \(n\ge2\), and let \(g_0,\ldots,g_{n-1}\in\mathbb Z_N\). The family has
**unique multiset sums** if the only \(k\in\mathbb Z_{\ge0}^n\) satisfying

\[
\sum_i k_i=n,\qquad
\sum_i k_i g_i=\sum_i g_i
\tag{1}
\]

is \(k=\mathbf1\). Translation preserves (1), so fix \(g_0=0\) and put
\(d_i=g_i-g_0\) for \(1\le i<n\).

## Lemma 1: subset-sum injection

All subset sums of \(d_1,\ldots,d_{n-1}\) are distinct. Indeed, a collision
between subsets \(U,V\), oriented so that \(|U|\le|V|\), gives the balanced
relation

\[
c_i=\mathbf1_U(i)-\mathbf1_V(i),\qquad
c_0=|V|-|U|.
\]

Every \(c_i\ge-1\), \(\sum_i c_i=0\), and \(\sum_i c_i g_i=0\). Thus
\(k=\mathbf1+c\) contradicts (1). Consequently the subset-sum image
\(I\subseteq\mathbb Z_N\) has exactly \(2^{n-1}\) elements.

## Lemma 2: doubled differences are holes

For each \(i>0\),

\[
2d_i\ne0\quad\Longrightarrow\quad 2d_i\notin I.
\tag{2}
\]

Suppose instead that \(2d_i=\sum_{j\in S}d_j\). Nonzero \(2d_i\) forces
\(S\ne\varnothing\). Define

\[
c_j=2\mathbf1_{\{i\}}(j)-\mathbf1_S(j)\quad(j>0),
\qquad
c_0=|S|-2.
\]

Then every coordinate is at least \(-1\), because \(S\ne\varnothing\);
\(\sum_jc_j=0\); and the displayed subset-sum identity gives
\(\sum_jc_jg_j=0\). Moreover \(c_i\in\{1,2\}\), so
\(\mathbf1+c\ne\mathbf1\). This again contradicts (1), proving (2).

## The cyclic bound

Write \(m=n-1\). The \(d_i\) are \(m\) distinct nonzero residues.

Suppose first that \(N\) is even, and write \(h=N/2\). A collision
\(2a=2b\) between distinct \(a,b\in\{d_1,\ldots,d_m\}\) is equivalent to
\(a=b+h\). There is at most one such collision pair. Indeed, two pairs
\(a=b+h\) and \(c=d+h\) are disjoint because doubling has fibers of size
two, but then

\[
a+d=b+c,
\]

contradicting subset-sum injectivity. Moreover, a collision pair cannot
coexist with \(h\) among the \(d_i\), since \(a=b+h\) would make the
singleton subset \(\{a\}\) and the two-element subset \(\{b,h\}\) have the
same sum. Thus either one difference doubles to zero or one pair collides
under doubling, but not both. It follows that there are at least \(m-1\)
distinct nonzero doubles.

Lemma 2 puts all these values outside \(I\), so

\[
N-2^m\ge m-1.
\tag{3}
\]

Both \(N\) and \(2^m\) are even, hence their difference is even. Rounding
(3) to the next even integer gives

\[
N-2^m\ge2\left\lceil\frac{m-1}{2}\right\rceil
=2\left\lfloor\frac m2\right\rfloor.
\]

If \(N\) is odd, doubling is injective and no \(d_i\) doubles to zero, so
Lemma 2 gives the stronger \(N-2^m\ge m\). Both parity cases therefore imply

\[
\boxed{N\ge
2^{n-1}+2\left\lfloor\frac{n-1}{2}\right\rfloor}.
\]

## Equality rigidity for arbitrary finite abelian groups

The same hole lemma gives a structural equality statement. If a finite
abelian group \(G\) of order \(2^{n-1}\) admits such a family, the injective
subset-sum map is bijective and has no holes. Lemma 2 therefore forces every
basepoint difference to have order two. Since their subset sums cover \(G\),
every element of \(G\) has order at most two. Thus

\[
G\cong(\mathbb Z_2)^{n-1},
\]

and the differences form an \(\mathbb F_2\)-basis.
