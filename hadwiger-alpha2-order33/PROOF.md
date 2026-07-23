# Proof through order 34

## 1. Trust base and the order-33 frontier

We use four established inputs.

1. Every minimum-order counterexample \(G\) to Hadwiger's conjecture in
   the independence-two class satisfies
   \[
   |V(G)|=2\chi(G)-1,\qquad \kappa(G)\geq\chi(G).
   \]
2. Chudnovsky and Seymour's clique threshold implies that an
   independence-two graph on 33 vertices containing \(K_9\) has a
   \(K_{17}\) minor.
3. Their seagull-packing theorem says that a graph \(H\) with
   \(\alpha(H)\leq2\) has \(k\) disjoint induced three-vertex paths if and
   only if
   \[
   |V(H)|\geq3k,\quad
   \kappa(H)\geq k,\quad
   \operatorname{cap}_H(Q)\geq k
   \text{ for every clique }Q,\quad
   \nu(\overline H)\geq k,
   \]
   apart from an irrelevant exceptional five-wheel when \(k=2\). If
   \(D_Q\) is the set of vertices outside \(Q\) mixed on \(Q\), then
   \[
   2\operatorname{cap}_H(Q)
   =|V(H)|-|Q|+|D_Q|.
   \]
4. The exact Ramsey number \(R(3,K_9-e)\) is 31.

The preceding order-31 lane proves the conjecture through order 32.
Suppose there is a counterexample on at most 34 vertices and choose one
with minimum order. Input 1 makes its order odd, so it must have 33
vertices. Consequently
\[
\chi(G)=17,\qquad \kappa(G)\geq17.
\tag{1}
\]

Put \(F=\overline G\). It is triangle-free. Applying
\(R(3,K_9-e)=31\) to any 31 vertices gives a \(K_9-e\) in \(G\). Write its
vertices as
\[
C\cup\{x,y\},
\]
where \(C\) is a seven-clique, \(x,y\) are complete to \(C\), and the only
possibly missing edge is \(xy\).

The \(K_9\) threshold and the assumption that \(G\) is a counterexample
force \(xy\notin E(G)\). Thus
\[
\omega(G)=8,\qquad \alpha(F)=8.
\tag{2}
\]
Every neighbourhood in the triangle-free graph \(F\) is independent, so
\[
\Delta(F)\leq8.
\tag{3}
\]

## 2. A core-dominating edge

Let
\[
P=V(G)\setminus(C\cup\{x,y\}),
\qquad |P|=24,
\]
and, for each \(v\in P\), put
\[
S_v=N_F(v)\cap C.
\]
We claim that there are \(a,b\in P\) such that
\[
ab\in E(G)
\quad\text{and}\quad
S_a\cap S_b=\varnothing.
\tag{4}
\]
The second condition says exactly that the connected branch set
\(\{a,b\}\) touches every singleton vertex of \(C\).

Suppose (4) is false. Whenever \(S_u,S_v\) are disjoint, \(uv\) must then
be an edge of \(F\).

- If \(S_v=\varnothing\), then \(v\) has all other 23 vertices of \(P\)
  as \(F\)-neighbours, contradicting (3).
- If \(S_v=\{c\}\), at most eight vertices of \(P\) have \(c\) in their
  incidence set, since \(d_F(c)\leq8\). Thus at least \(24-8=16\)
  vertices have incidence sets disjoint from \(S_v\), again contradicting
  (3).
- If \(S_v=\{c,d\}\), the two classes of vertices whose incidence sets
  contain \(c\) or \(d\) each have size at most eight and intersect in
  \(v\). Their union therefore has size at most \(8+8-1=15\). At least
  \(24-15=9\) vertices have incidence sets disjoint from \(S_v\), once
  more contradicting (3).

Hence \(|S_v|\geq3\) for all 24 vertices \(v\in P\). This gives at least
\(24\cdot3=72\) incidences between \(P\) and \(C\), whereas (3) gives at
most \(7\cdot8=56\). The contradiction proves (4).

## 3. Attaching the edge to a ten-branch core

Since \(xy\notin E(G)\) and \(\alpha(G)\leq2\), every vertex outside
\(\{x,y\}\) is adjacent to \(x\) or \(y\). Thus the edge branch
\(\{a,b\}\) from (4) collectively touches at least one of \(x,y\).

The number of common \(G\)-neighbours of \(x,y\) is
\[
31-(d_F(x)-1)-(d_F(y)-1)
=33-d_F(x)-d_F(y)
\geq17.
\tag{5}
\]
Seven lie in \(C\), so the set
\[
W=(N_G(x)\cap N_G(y))\setminus C
\]
has at least ten vertices.

There are three cases.

1. If \(\{a,b\}\) touches both \(x\) and \(y\), choose
   \(z\in W\setminus\{a,b\}\). Use the core branch sets
   \[
   \{\{c\}:c\in C\},\quad \{x,z\},\quad\{y\},\quad\{a,b\}.
   \]
2. If \(\{a,b\}\) touches \(x\) but not \(y\), neither endpoint lies in
   \(W\). Since \(|W|\geq10>d_F(a)\), choose \(z\in W\) adjacent to \(a\)
   in \(G\). Use
   \[
   \{\{c\}:c\in C\},\quad \{x\},\quad\{y,z\},\quad\{a,b\}.
   \]
3. If \(\{a,b\}\) touches \(y\) but not \(x\), use the symmetric
   construction.

The edge cannot miss both \(x\) and \(y\), since either endpoint would
then form an independent triple with \(x,y\). In each case the ten
displayed branch sets are pairwise disjoint, connected, and pairwise
touching: \(C\) is a clique, \(x,y\) are complete to \(C\), (4) makes
\(\{a,b\}\) touch \(C\), \(z\) is adjacent to both \(x,y\), and the
case-specific choice supplies the remaining contacts with \(\{a,b\}\).
They use the 12 vertices
\[
U=C\cup\{x,y,z,a,b\}.
\tag{6}
\]

## 4. Seven seagulls in the remainder

Let
\[
H=G-U.
\]
Then \(|V(H)|=21\), \(\alpha(H)\leq2\), and \(\omega(H)\leq8\).

### Connectivity

Deleting the 12 vertices of \(U\) from the 17-connected graph \(G\)
leaves a 5-connected graph, so \(\kappa(H)\geq5\). Suppose
\(\kappa(H)<7\), and let \(S\) be a cut of size five or six.

The graph \(H-S\) has exactly two components and both are cliques:
three components give an independent triple, while two nonadjacent
vertices in one component together with a vertex of another do the same.

If \(|S|=5\), the two component sizes sum to 16 and are at most eight, so
both are eight. Any \(s\in S\) must have a non-neighbour in each
eight-clique, since being complete to either would create a \(K_9\).
Those two non-neighbours and \(s\) form an independent triple, a
contradiction.

If \(|S|=6\), the component sizes are seven and eight; call the components
\(A,B\), respectively. Every \(s\in S\) has a non-neighbour in \(B\), so
\(\alpha(G)\leq2\) forces \(s\) to be complete to \(A\). Any edge inside
\(S\), together with the seven-clique \(A\), would create a \(K_9\).
Thus \(S\) is an independent six-set, another contradiction. Therefore
\[
\kappa(H)\geq7.
\tag{7}
\]

### Antimatching

Let \(M\) be a maximum matching in \(\overline H\). Its unmatched
vertices form an independent set in \(\overline H\), and hence a clique
of \(H\), so there are at most eight of them. Therefore
\[
21-2|M|\leq8,
\qquad
\nu(\overline H)\geq7.
\tag{8}
\]

### Capacity

Let \(Q\) be a clique of \(H\), and let \(D_Q\) be the vertices outside
\(Q\) mixed on it. Since \(|Q|\leq8\),
\[
2\operatorname{cap}_H(Q)=21-|Q|+|D_Q|\geq14
\]
unless \(|Q|=8\) and \(D_Q=\varnothing\). In that exceptional numerical
case, no outside vertex is complete to \(Q\), since \(\omega(G)=8\), so
all 13 outside vertices are anticomplete to \(Q\). They form a clique by
\(\alpha(G)\leq2\), contradicting \(\omega(G)=8\). Hence
\[
\operatorname{cap}_H(Q)\geq7
\tag{9}
\]
for every clique \(Q\).

Chudnovsky--Seymour now gives seven disjoint seagulls in \(H\), covering
all 21 vertices.

## 5. Conclusion

Every seagull in an independence-two graph touches every outside vertex:
otherwise that vertex and the two nonadjacent ends of the seagull form an
independent triple. Thus the seven seagulls are pairwise touching and
touch all ten core branch sets from Section 3. Together they form a
\(K_{17}\)-model in \(G\), a contradiction.

There is no minimum counterexample of order 33. Since minimum
counterexamples have odd order and the preceding lane handles all orders
through 32, every independence-two graph on at most 34 vertices satisfies
Hadwiger's conjecture.
