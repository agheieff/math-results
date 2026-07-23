# Proof report

## 1. Frozen definition

Let \(G\) be a finite abelian group, written additively, and let
\(g=(g_0,\ldots,g_{n-1})\in G^n\). Put

\[
t=\sum_{i=0}^{n-1}g_i.
\]

Following arXiv:2607.08366v2 and arXiv:2607.09949v2, say that \(g\) has
**unique multiset sums** when the only vector
\(k=(k_0,\ldots,k_{n-1})\in\mathbb Z_{\ge0}^n\) such that

\[
\sum_i k_i=n
\quad\text{and}\quad
\sum_i k_i g_i=t
\tag{1}
\]

is \(k=\mathbf 1=(1,\ldots,1)\).

For \(G=\mathbb Z_N\) and a set \(A=\{a_0,\ldots,a_{n-1}\}\), equality in
\(G\) is congruence modulo \(N\), and this is exactly the paper's definition
of \(A\) being valid mod \(N\). Repetitions among the \(g_i\) need not be
excluded separately: if \(g_i=g_j\) for \(i\ne j\), then
\(\mathbf1+e_i-e_j\) already violates (1).

## 2. Sharp group-order theorem

**Theorem.** If \(n\ge2\) and \(g_0,\ldots,g_{n-1}\in G\) have unique
multiset sums in a finite abelian group \(G\), then

\[
|G|\ge2^{n-1}.
\tag{2}
\]

More precisely, for every \(j\), the set of basepoint differences

\[
D_j=\{g_i-g_j:i\ne j\}
\]

is dissociated: all \(2^{n-1}\) of its subset sums are distinct.

**Proof.** Fix \(j\), and suppose two distinct subsets
\(U,V\subseteq [n]\setminus\{j\}\) have the same difference sum:

\[
\sum_{i\in U}(g_i-g_j)=\sum_{i\in V}(g_i-g_j).
\tag{3}
\]

Exchange \(U\) and \(V\), if necessary, so that \(|U|\le|V|\). Define an
integer vector \(c\) by

\[
c_i=\mathbf1_U(i)-\mathbf1_V(i)\quad(i\ne j),
\qquad
c_j=|V|-|U|.
\tag{4}
\]

This formula already handles overlap: indices in \(U\cap V\) receive
coefficient zero. Every coordinate of \(c\) is at least \(-1\), and

\[
\sum_i c_i=|U|-|V|+(|V|-|U|)=0.
\tag{5}
\]

Expanding (3) gives

\[
\sum_i c_i g_i
=
\sum_{i\in U}g_i-\sum_{i\in V}g_i+(|V|-|U|)g_j
=0.
\tag{6}
\]

Now set \(k=\mathbf1+c\). Equations (4) and (5) give \(k_i\ge0\) and
\(\sum_i k_i=n\); equation (6) gives

\[
\sum_i k_i g_i=\sum_i g_i=t.
\]

Because \(U\ne V\), their symmetric difference is nonempty, so some
coordinate outside \(j\) of \(c\) is \(1\) or \(-1\). Thus
\(k\ne\mathbf1\), contradicting unique multiset sums.

Therefore the subset-sum map

\[
\mathcal P([n]\setminus\{j\})\longrightarrow G,
\qquad
S\longmapsto\sum_{i\in S}(g_i-g_j)
\]

is injective. Its domain has \(2^{n-1}\) elements, proving (2). \(\square\)

The argument proves a necessary condition only. It uses the special balanced
relations whose non-basepoint coefficients lie in \(\{-1,0,1\}\); unique
multiset sums must also exclude balanced relations with larger positive
coefficients.

## 3. Equality and the all-groups optimum

**Proposition.** The bound (2) is attained for every \(n\ge2\).

**Proof.** Take

\[
G=(\mathbb Z_2)^{n-1},
\qquad
g=(0,e_1,\ldots,e_{n-1}),
\]

where the \(e_i\) are the standard basis vectors. If \(k\ge0\) satisfies
(1), comparison in coordinate \(i\ge1\) makes \(k_i\) odd. Hence
\(k_i\ge1\) for all \(i\ge1\). These coordinates already contribute at
least \(n-1\) to \(\sum_i k_i=n\). Increasing any of them to the next odd
value \(3\) would make the total at least \(n+1\), so every \(k_i=1\) for
\(i\ge1\), and then \(k_0=1\). Thus the family has unique multiset sums.
\(\square\)

Combining the theorem and proposition gives

\[
\min\{|G|:G\text{ finite abelian and admits a size-}n
\text{ unique-multiset-sum family}\}=2^{n-1}.
\tag{7}
\]

This answers the all-finite-abelian-groups question in Open Problem 4 of
arXiv:2607.08366v2 and Remark 1 of arXiv:2607.09949v2.

## 4. Cyclic corollary and remaining gap

If \(A\subseteq\mathbb Z_N\) is valid mod \(N\), the theorem gives

\[
N\ge2^{n-1}.
\tag{8}
\]

Fonollosa's cyclic conjecture asks for the stronger lower bound

\[
N\ge2^n-2^{\lfloor\log_2 n\rfloor}.
\tag{9}
\]

For every \(n\ge3\), the right side of (9) is strictly larger than
\(2^{n-1}\). Thus (8) is a general set-free exponential bound, but it does
not settle the cyclic conjecture.

The later companion paper arXiv:2607.09949v2 already proves

\[
|G|\ge\frac{\binom{2n}{n}}{2^n}
\sim\frac{2^n}{\sqrt{\pi n}}
\tag{10}
\]

by the partial-derivative method for permanent formulas. Relative to the
displayed real-valued right side in (10), bound (2) improves it by the exact
factor

\[
\frac{2^{n-1}}{\binom{2n}{n}/2^n}
=\frac{2^{2n-1}}{\binom{2n}{n}}
\sim\frac{\sqrt{\pi n}}2,
\]

and meets the companion paper's upper construction.

There is also a classical algebraic route that makes the same sharp bound
implicit. An order-\(n\) evaluation scheme in the companion paper has the form

\[
\operatorname{per} B
=c\sum_{r\in R}w_r\prod_{i=0}^{n-1}L_r(B_{i,*}).
\]

Set every row of \(B\) equal to \(x=(x_0,\ldots,x_{n-1})\). The identity
becomes

\[
n!x_0\cdots x_{n-1}
=c\sum_{r\in R}w_rL_r(x)^n.
\]

Thus \(|R|\) is at least the complex Waring rank of the squarefree monomial.
The monomial-rank formula of Carlini--Catalisano--Geramita
(arXiv:1110.0745) gives

\[
\operatorname{rk}_{\mathbb C}(x_0\cdots x_{n-1})=2^{n-1}.
\]

Their theorem is over an algebraically closed field of characteristic zero,
so it applies over \(\mathbb C\). Here \(n!\ne0\); after division by \(n!\),
each nonzero scalar \(cw_r/n!\) has an \(n\)-th root and can be absorbed into
\(L_r\). Zero-weight terms are discarded. Hence the resulting Waring
decomposition has at most \(|R|\) nonzero summands.

Consequently their classical theorem independently sharpens the companion
paper's lower bound for every evaluation scheme of its stated form, not only
for character schemes. The direct dissociation proof above avoids complex
algebra and applies entirely inside the finite group.

## 5. Computation

The bundled code is regression evidence, not part of the proof. Finite
abelian groups are represented as products of cyclic prime-power groups.
For every small group type and every normalized \(n\)-element set, it:

- enumerates all nonnegative multiplicity vectors summing to \(n\);
- computes every basepoint-difference subset sum;
- turns a repeated subset sum into the vector \(k\) in (4); and
- checks directly that this \(k\) is a forbidden multiset.

Normalization loses nothing: translation preserves (1), and every set can
be translated so that one selected element is zero. Families with repeated
elements are excluded from the set enumeration because their two-coordinate
collision is immediate.

The default command exhausts all finite abelian group isomorphism types of
orders below \(2^{n-1}\) for \(2\le n\le5\), then directly checks the equality
construction in \((\mathbb Z_2)^{n-1}\).

| \(n\) | lower bound | group types below | normalized sets | valid below | equality |
|---:|---:|---:|---:|---:|:---|
| 2 | 2 | 1 | 0 | 0 | valid |
| 3 | 4 | 3 | 1 | 0 | valid |
| 4 | 8 | 8 | 36 | 0 | valid |
| 5 | 16 | 20 | 3,473 | 0 | valid |

## 6. Lean verification

`lean/UniqueMultisetSum.lean` formalizes the full lower-bound implication for
an arbitrary finite additive commutative group. Its indexing uses a family of
size `n + 1`, so `group_card_lower_bound` concludes `2 ^ n ≤ |G|`.

The formal proof constructs the forbidden natural-valued multiplicity vector,
checks its total and weighted sum, proves injectivity of the basepoint
subset-sum map, and obtains the cardinal bound. It contains no `sorry`.
`CheckAxioms.lean` reports only `propext`, `Classical.choice`, and `Quot.sound`.

The elementary equality construction remains proved conventionally in
Section 3 and checked exhaustively by the independent implementations.
