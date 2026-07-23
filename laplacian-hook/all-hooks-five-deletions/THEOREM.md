# Corrected all-hook theorem

## Statement

Let \(\mathscr G_n\) be the simple graphs obtained from \(K_n\) by deleting
at most five edges. For every \(n>7\), \(1\le k\le n\), \(G\in\mathscr G_n\),
and simple graph \(H\),

\[
\Phi_{(k,1^{n-k})}(L(G),x)
=\Phi_{(k,1^{n-k})}(L(H),x)
\quad\Longrightarrow\quad G\cong H.
\]

## Correct hook characters

Put

\[
D=\binom{n-1}{k-1},\qquad
N=n-1,\qquad z=2k-n-1.
\]

The exterior-power identity

\[
\sum_{j=0}^{n-1}\chi^{(n-j,1^j)}(\pi)t^j
=\frac{\prod_{C\in\operatorname{cyc}(\pi)}
       (1-(-t)^{|C|})}{1+t}
\]

gives the normalized character values

\[
\rho_2=\frac{\chi(2,1^{n-2})}{D}=\frac zN,
\]

\[
\rho_3=\frac{\chi(3,1^{n-3})}{D}
=\frac{N(N-4)+3z^2}{4N(N-1)},
\]

\[
\rho_4=\frac{\chi(4,1^{n-4})}{D}
=\frac{z(N^2-6N+4+z^2)}{2N(N-1)(N-2)},
\]

\[
\rho_{22}=\frac{\chi(2,2,1^{n-4})}{D}
=\frac{z^2-N}{N(N-1)}.
\]

In particular, the three-cycle character is

\[
\binom{n-4}{k-4}+\binom{n-4}{k-1},
\]

not the binomial difference used in the source paper.

## Top coefficients

Normalize

\[
\Phi/D=x^n+q_1x^{n-1}+q_2x^{n-2}+q_3x^{n-3}
+q_4x^{n-4}+\cdots.
\]

For the degree multiset of \(G\), let \(e_j\) be its elementary symmetric
functions. Let \(E\) be the edge count, \(T\) the triangle count, \(C_4\)
the four-cycle count, and \(M_2\) the two-matching count. Define

\[
U=\sum_{uv\in E(G)}\sum_{w\notin\{u,v\}}d_w,\qquad
V=\sum_{uv\in E(G)}e_2(d_w:w\notin\{u,v\}),
\]

\[
S=\sum_{\triangle}\sum_{w\notin\triangle}d_w.
\]

The permutation types moving at most four vertices give

\[
q_1=-e_1,\qquad q_2=e_2+\rho_2E,
\]

\[
q_3=-e_3-\rho_2U+2\rho_3T,
\]

\[
q_4=e_4+\rho_2V-2\rho_3S+2\rho_4C_4+\rho_{22}M_2.
\]

These formulas are checked independently by direct immanant expansion.

## Reduction to 37 residual pairs

The polynomial degree and \(q_1\) recover the order and edge count, so any
polynomial mate of a target is also in \(\mathscr G_n\). Exact canonical
enumeration gives

\[
1,\ 1,\ 2,\ 5,\ 11,\ 26
\]

complement types with zero through five edges: 46 types and 1,035 pairs.

The first coefficient separates 644 pairs. At fixed deleted-edge count,
\(q_2\) separates exactly the 354 pairs with unequal
\(D_2=\sum_v d_{\overline G}(v)^2\). For each of the remaining 37 pairs,
put

\[
\Delta D_3
=\Delta\sum_vd_{\overline G}(v)^3,\qquad
\Delta t=\Delta|\mathscr C_3(\overline G)|.
\]

Then

\[
\Delta q_3=\frac{\Delta D_3}{3}-2\rho_3\Delta t.
\]

The exact \((\Delta D_3,\Delta t)\) table has twelve values:

\[
\begin{array}{c|rrrrrrrrrrrr}
(\Delta D_3,\Delta t)&(-12,1)&(-6,0)&(-6,1)&(0,-1)&(0,0)&(0,1)&
(6,-1)&(6,0)&(6,1)&(12,0)&(18,-1)&(18,0)\\
\hline
\text{count}&2&6&5&2&6&6&1&5&1&1&1&1.
\end{array}
\]

Writing \(a=k-1\), \(b=n-k\), so \(a+b=N\),

\[
2\rho_3=2-\frac{6ab}{N(N-1)}.
\]

It is positive and at most two. The table therefore shows that \(q_3\)
separates 30 pairs outright. The sole \((6,1)\) pair can collide only when
\(ab=0\), namely \(k=1\) or \(k=n\); its \(q_4\)-difference is \(-1\) at
both endpoints. Six pairs have \((\Delta D_3,\Delta t)=(0,0)\).

## Six final pairs

For five of the final pairs, the nonzero \(q_4\)-difference is a signed
scalar multiple of

\[
\frac{P(N,z)}{N(N-1)(N-2)},
\]

where

\[
P=N^3-6N^2+8N+z^3+(3N-6)z^2+(2N^2-9N+6)z.
\]

In terms of \(a,b\),

\[
P=7a(a-1)(a-2)+b(b-1)(b-2)+ab(b-a).
\]

If \(b\ge a\), every term is nonnegative and \(b\ge4\), so \(P>0\). If
\(a>b\), then \(a\ge4\) and

\[
b(a-b)\le a(a-1)<7(a-1)(a-2),
\]

so again \(P>0\).

The last pair is a signed multiple of

\[
\frac{Q(N,z)}{N(N-1)},\qquad
Q=N^2-4N+3z^2+(N-1)z.
\]

Equivalently,

\[
Q=5a^2-4ab-5a+3b^2-3b.
\]

As a quadratic in \(b\), its discriminant is
\(-44a^2+84a+9<0\) for \(a\ge3\), so \(Q>0\). For \(a=0,1,2\), respectively,

\[
Q=3b(b-1),\quad b(3b-7),\quad (3b-5)(b-2),
\]

which are positive because \(a+b=N\ge7\). Thus \(q_4\) separates the final
six pairs, proving the theorem.
