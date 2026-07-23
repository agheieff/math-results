# Frozen bounded assertion

Let \(\mathcal S=(S_1,\ldots,S_{28})\) be a multiset of nonempty subsets of
a ten-set \(C\). Construct \(F\) on
\[
\{v\}\mathbin{\dot\cup}C\mathbin{\dot\cup}X,\qquad |X|=28,
\]
by joining \(v\) to \(C\), joining \(x_i\) to \(S_i\), and joining
\(x_i,x_j\) exactly when \(S_i\cap S_j=\varnothing\). Put
\(G=\overline F\).

Assume:

1. every support has size at least three, total incidence is at most 90,
   and every coordinate occurs at most nine times;
2. the exact outside-degree, diameter-two coverage, disjoint-triple, and
   pairwise-intersecting Hall inequalities from the sibling support lane
   all hold;
3. \(F\) is factor-critical;
4. \(\kappa(G)\geq20\);
5. every edge of \(G\) is non-dominating; and
6. \(\chi(G/e)=19\) for every edge \(e\in E(G)\).

These assumptions imply
\[
\alpha(G)=2,\qquad \omega(G)=10,\qquad \chi(G)=20.
\]

The assertion under investigation is:

> \(G\) has a spanning \(K_{20}\)-model consisting of one singleton branch
> and nineteen two-vertex branches.

Equivalently, for some singleton \(s\), \(G-s\) has a perfect matching
\(M\) such that every edge of \(M\) touches \(s\) and every two edges of
\(M\) touch one another.

This assertion does not assume that \(G\) is \(K_{20}\)-minor-free. A
counterexample would refute only this stronger local-structure route, not
Hadwiger's conjecture.
