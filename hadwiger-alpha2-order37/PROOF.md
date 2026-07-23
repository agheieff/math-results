# Hadwiger's conjecture through order 38

## 1. Reduction to the clique-nine case at order 37

We use four established inputs.

1. A minimum-order counterexample \(G\) to Hadwiger's conjecture among
   graphs with \(\alpha(G)\leq2\) has
   \[
   |V(G)|=2\chi(G)-1,\qquad \kappa(G)\geq\chi(G).
   \tag{1}
   \]
2. The sibling order-35 lane proves the conjecture in this class through
   order 36.
3. \(R(3,9)=36\).
4. Scully and Song prove Hadwiger's conjecture, in a stronger dominating
   form, for an \(n\)-vertex graph with \(\alpha(G)\leq2\) whenever
   \[
   2\omega(G)\geq\lceil n/2\rceil+1.
   \tag{2}
   \]

Suppose there is a counterexample on at most 38 vertices, and choose one
of minimum order. Inputs 1 and 2 give
\[
|V(G)|=37,\qquad \chi(G)=19,\qquad\kappa(G)\geq19.
\tag{3}
\]
Put \(F=\overline G\). It is triangle-free. Input 3 gives
\(\alpha(F)=\omega(G)\geq9\). If \(\omega(G)\geq10\), then (2) applies,
since
\[
2\omega(G)\geq20=\lceil37/2\rceil+1.
\]
Thus a counterexample would satisfy
\[
\omega(G)=\alpha(F)=9,\qquad\Delta(F)\leq9.
\tag{4}
\]

Fix a maximum stable set \(C\) of \(F\), put
\[
P=V(F)\setminus C,\qquad |P|=28,
\]
and define the support of \(v\in P\) by
\[
S_v=N_F(v)\cap C.
\tag{5}
\]

## 2. The empty-support case

Suppose first that \(S_x=\varnothing\) for some \(x\in P\). In \(G\),
the ten vertices \(C\cup\{x\}\) form a clique. Let
\[
H=G-(C\cup\{x\}).
\]
Then \(|V(H)|=27\), \(\alpha(H)\leq2\), \(\omega(H)\leq9\), and (3)
gives \(\kappa(H)\geq9\).

The vertices missed by a maximum matching in \(\overline H\) form a
clique in \(H\), of size at most nine. Hence
\[
27-2\nu(\overline H)\leq9,\qquad
\nu(\overline H)\geq9.
\tag{6}
\]
For every clique \(Q\) of \(H\), if \(D_Q\) is the set of vertices
outside \(Q\) mixed on \(Q\), then
\[
2\operatorname{cap}_H(Q)=27-|Q|+|D_Q|\geq18.
\tag{7}
\]
Chudnovsky and Seymour's seagull-packing theorem gives nine disjoint
seagulls in \(H\). They cover \(H\), pairwise touch, and touch the
ten-clique, yielding a \(K_{19}\) minor.

We may therefore assume from now on that
\[
S_v\neq\varnothing\qquad(v\in P).
\tag{8}
\]

## 3. Good pairs

Define a graph \(J\) on \(P\) by declaring \(uv\in E(J)\) exactly when
\[
uv\notin E(F),\qquad S_u\cap S_v=\varnothing.
\tag{9}
\]
Thus an edge of \(J\) is an edge branch in \(G\) that touches every
singleton of the nine-clique \(C\).

### The graph \(J\) is nonempty

Suppose \(J\) has no edges. If \(|S_v|=1\), at most nine vertices of
\(P\) have support meeting \(S_v\). At least \(28-9=19\) supports are
disjoint from \(S_v\), and all must be \(F\)-neighbours of \(v\), while
\(v\) has room for at most eight such neighbours outside \(C\).

If \(|S_v|=2\), the two relevant support classes have union of size at
most \(9+9-1=17\), so at least eleven supports are disjoint from
\(S_v\), while \(v\) has room for at most seven outside neighbours.
Together with (8), every support therefore has size at least three.
This gives
\[
84=28\cdot3
\leq\sum_{v\in P}|S_v|
=\sum_{c\in C}d_F(c)
\leq9\cdot9=81,
\]
a contradiction. Hence \(E(J)\neq\varnothing\).

### The graph \(J\) has a two-edge matching

Suppose instead that \(\nu(J)=1\), choose \(ab\in E(J)\), and put
\(R=P\setminus\{a,b\}\). The graph \(J[R]\) is empty.

The preceding small-support count on the 26 vertices of \(R\) gives 17
disjoint supports against an outside-neighbour budget of eight when a
support has size one, and nine against a budget of seven when it has
size two. Thus every support in \(R\) has size at least three, and
\[
|S_a|+|S_b|
\leq81-\sum_{v\in R}|S_v|
\leq81-26\cdot3=3.
\tag{10}
\]
The two supports are nonempty and disjoint, so their sizes are
\((1,1)\) or \((1,2)\), in some order.

If an endpoint has support size one, at least 18 vertices of \(R\) have
disjoint support and at most eight are its \(F\)-neighbours, giving at
least ten \(J\)-neighbours in \(R\). For support size two the analogous
numbers are ten, seven, and three. We can therefore choose distinct
\[
x\in N_J(a)\cap R,\qquad y\in N_J(b)\cap R.
\]
The edges \(ax,by\) form a two-edge matching in \(J\), a contradiction.
Moreover, their corresponding branches touch in \(G\) via the edge
\(ab\).

Consequently
\[
\nu(J)\geq2.
\tag{11}
\]

### Two disjoint good branches can be chosen to touch

Suppose, for a contradiction, that no two vertex-disjoint edges of
\(J\) give branch sets that touch in \(G\). A four-vertex path in \(J\)
would violate this: its first and last edges are disjoint and touch via
the middle edge. Thus \(J\) has no four-vertex path as a subgraph.

Every connected nontrivial component of such a graph has matching
number one. By (11), \(J\) has at least two nontrivial components. It
has at most two: choose an edge from each of three components. The
non-touching assumption forces every cross-pair of their endpoint sets
to be an \(F\)-edge, so one endpoint from each edge would form a
triangle in \(F\). Denote the two nontrivial components by \(U,W\).

Every \(u\in U\) and \(w\in W\) lies on an edge of its component.
The two edges are disjoint, so the non-touching assumption forces
\[
uw\in E(F).
\tag{12}
\]
Triangle-freeness and (12) make both \(U\) and \(W\) stable in \(F\).
Set
\[
A=\bigcup_{u\in U}S_u,\qquad B=\bigcup_{w\in W}S_w.
\]
Equation (12) gives \(A\cap B=\varnothing\). Moreover,
\(U\cup(C\setminus A)\) is stable in \(F\), and so is
\(W\cup(C\setminus B)\). Since \(\alpha(F)=9\),
\[
|U|\leq|A|,\qquad |W|\leq|B|,\qquad |U|+|W|\leq9.
\tag{13}
\]

The total support incidence is at most 81, so among 28 nonempty
supports some support has size at most two. A size-one support has at
least
\[
(28-9)-8=11
\tag{14}
\]
neighbours in \(J\), which would make its component have at least 12
vertices, contrary to (13). Hence some size-two support exists. It has
at least
\[
(28-17)-7=4
\tag{15}
\]
neighbours in \(J\). Relabel so that it lies in \(U\); then
\(|U|\geq5\), and (13) gives \(|W|\leq4\).

No vertex of \(W\) has support size one, by (14), or size two, since
(15) would force \(|W|\geq5\). Every support in \(W\) has size at least
three. The component \(W\) contains an edge of \(J\), whose two supports
are disjoint, and hence \(|B|\geq6\). But (13) also gives
\(|A|\geq|U|\geq5\), contradicting the fact that the disjoint sets
\(A,B\) lie in the nine-set \(C\).

We have proved that there are vertex-disjoint edges \(ab,xy\in E(J)\)
whose two edge branches touch in \(G\).

## 4. Eight seagulls in the 24-vertex remainder

The nine singleton branches from \(C\), together with
\(\{a,b\}\) and \(\{x,y\}\), form an eleven-branch complete-minor core
on 13 vertices. Let \(H\) be the graph left after deleting those
vertices. Then
\[
|V(H)|=24,\qquad \alpha(H)\leq2,\qquad\omega(H)\leq9,
\qquad\kappa(H)\geq6.
\tag{16}
\]

We claim that \(\kappa(H)\geq8\). As usual, a cut leaves exactly two
components, both cliques. A six-cut would leave two nine-cliques.
Every cut vertex has a nonneighbour in each, since it cannot complete
either to a ten-clique; this gives a stable triple. A seven-cut leaves
cliques of sizes eight and nine. Every cut vertex misses a vertex of
the nine-clique and is therefore complete to the eight-clique. An edge
in the cut would complete that eight-clique to a ten-clique, so the cut
is stable, again impossible. This proves
\[
\kappa(H)\geq8.
\tag{17}
\]

Exactly as in the order-35 lane, the unmatched vertices of a maximum
matching in \(\overline H\) form a clique of \(H\), giving
\[
\nu(\overline H)\geq8.
\tag{18}
\]
For every clique \(Q\) of \(H\),
\[
2\operatorname{cap}_H(Q)=24-|Q|+|D_Q|\geq16,
\tag{19}
\]
apart from the numerical case \(|Q|=9,D_Q=\varnothing\). In that case
all 15 outside vertices are anticomplete to \(Q\) and hence form a
clique, contradicting \(\omega(G)=9\). Thus (19) holds in every case.

The seagull-packing theorem now supplies eight disjoint seagulls in
\(H\). They cover \(H\), pairwise touch, and touch every core branch.
Together with the eleven core branches they give a \(K_{19}\) minor,
contrary to (3).

There is no minimum counterexample of order at most 38. Therefore every
graph with independence number at most two and at most 38 vertices
satisfies Hadwiger's conjecture.
