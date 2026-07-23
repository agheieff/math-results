# Proof through order 32

## 1. Trust base and minimum counterexample

We use the following established results.

1. Carter proved Hadwiger's conjecture for every graph with independence
   number at most two and at most 30 vertices, and proved that a minimal
   counterexample has either 31 vertices or at least 33 vertices.
2. A minimum-order counterexample \(G\) in the independence-two class is
   \(\chi(G)\)-critical and satisfies
   \[
   |V(G)|=2\chi(G)-1,
   \qquad
   \kappa(G)\geq\chi(G).
   \]
3. Chudnovsky and Seymour's clique threshold implies that an
   independence-two graph on 31 vertices containing \(K_9\) has a
   \(K_{16}\) minor.
4. Their seagull-packing theorem says that a graph \(H\) with
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
5. The exact Ramsey number \(R(3,K_9-e)\) is 31.

Suppose the frozen statement is false and choose a counterexample with the
fewest vertices. It has at most 32 vertices, while Carter's dichotomy
forces it to have 31 vertices. The minimum-counterexample properties give
\[
\chi(G)=16,\qquad \kappa(G)\geq16.
\tag{2}
\]

## 2. A \(K_9-e\) core and a prescribed seagull

Put \(F=\overline G\). It is triangle-free. Since
\(R(3,K_9-e)=31\), \(G\) contains a copy of \(K_9-e\). Write its vertices
as
\[
C\cup\{x,y\},
\]
where \(C\) is a seven-clique, \(x\) and \(y\) are complete to \(C\), and
the only possibly missing edge is \(xy\).

The \(K_9\) threshold and the assumption that \(G\) is a counterexample
force \(xy\notin E(G)\). Hence \(G\) contains a \(K_8\) but no \(K_9\), so
\[
\omega(G)=8,\qquad \alpha(F)=8.
\tag{3}
\]
Every neighbourhood in the triangle-free graph \(F\) is independent.
Thus
\[
d_F(v)\leq8
\tag{4}
\]
for every vertex \(v\).

Now \(xy\in E(F)\), and triangle-freeness makes
\(N_F(x)\setminus\{y\}\) and \(N_F(y)\setminus\{x\}\) disjoint. The number
of common neighbours of \(x,y\) in \(G\) is therefore
\[
29-(d_F(x)-1)-(d_F(y)-1)
=31-d_F(x)-d_F(y)
\geq15.
\tag{5}
\]
Seven of these vertices are in \(C\), so choose
\[
z\in V(G)\setminus(C\cup\{x,y\})
\]
adjacent to both \(x\) and \(y\). Define the 21-vertex remainder
\[
L=G-(C\cup\{x,y,z\}).
\tag{6}
\]

If \(L\) has seven disjoint seagulls, they cover \(V(L)\). Those seven
seagulls, the seven singleton vertices of \(C\), the connected branch set
\(\{x,z\}\), and the singleton \(\{y\}\) form a \(K_{16}\)-model:

- the first nine branch sets form a \(K_9\)-model;
- every outside vertex meets every seagull, since otherwise it and the two
  nonadjacent ends of that seagull would be an independent triple;
- the same observation makes any two seagulls touch.

It remains to verify the four seagull-packing conditions for \(L\) and
\(k=7\).

## 3. Antimatching

Let \(M\) be a maximum matching in \(\overline L\). The vertices not
covered by \(M\) form an independent set in \(\overline L\), since
otherwise \(M\) could be enlarged. By (3), every such independent set has
at most eight vertices. Therefore
\[
21-2|M|\leq8,
\]
and integrality gives
\[
\nu(\overline L)\geq7.
\tag{7}
\]

## 4. Capacity

Let \(Q\) be a clique of \(L\), and let \(D_Q\) be the vertices outside
\(Q\) mixed on it. By (3), \(|Q|\leq8\), and
\[
2\operatorname{cap}_L(Q)=21-|Q|+|D_Q|.
\tag{8}
\]
This is at least 14 unless \(|Q|=8\) and \(D_Q=\varnothing\).

In that exceptional numerical case, no outside vertex can be complete to
\(Q\), since \(\omega(G)=8\). Since no outside vertex is mixed on \(Q\)
either, all 13 outside vertices are anticomplete to \(Q\). They must form
a clique: two nonadjacent ones together with any vertex of \(Q\) would be
an independent triple. This contradicts \(\omega(G)=8\). Therefore
\[
\operatorname{cap}_L(Q)\geq7
\tag{9}
\]
for every clique \(Q\).

## 5. The apparent six-cut is impossible

Deleting ten vertices from the 16-connected graph \(G\) leaves a
6-connected graph, so
\[
\kappa(L)\geq6.
\tag{10}
\]
Suppose equality holds, and let \(S\) be a six-vertex cut in \(L\).
Because \(\alpha(L)\leq2\), the graph \(L-S\) has exactly two components
and both are cliques. Indeed, three components give an independent
triple, while two nonadjacent vertices in one component together with a
vertex of another do the same.

The two component sizes sum to 15 and are at most eight by (3), so they
are seven and eight. Call the components \(A\) and \(B\), with
\[
|A|=7,\qquad |B|=8.
\tag{11}
\]
They are anticomplete.

Lift the cut back to \(G\):
\[
T=S\cup C\cup\{x,y,z\}.
\]
Then \(|T|=16\) and \(G-T\) has components \(A,B\). For every \(t\in T\),
the graph \(G-(T\setminus\{t\})\) is connected by (2). Since \(A\) and
\(B\) are anticomplete, \(t\) must have a neighbour in each of \(A,B\).

No \(t\in T\) is complete to the eight-clique \(B\), by (3). Thus \(t\)
has a non-neighbour in \(B\). If it also had a non-neighbour in \(A\),
those two non-neighbours and \(t\) would form an independent triple.
Consequently every vertex of \(T\) is complete to the seven-clique \(A\).

Two adjacent vertices in \(T\), together with \(A\), would form a
nine-clique. Hence \(T\) is an independent set of size 16, contradicting
\(\alpha(G)\leq2\). This proves
\[
\kappa(L)\geq7.
\tag{12}
\]

## 6. Conclusion

The graph \(L\) has 21 vertices, is 7-connected by (12), satisfies every
clique-capacity inequality by (9), and has an antimatching of size seven
by (7). Chudnovsky--Seymour therefore gives seven disjoint seagulls in
\(L\). Section 2 turns them into a \(K_{16}\)-model in \(G\), contradicting
that \(G\) was a counterexample.

Therefore every graph with independence number at most two and at most
32 vertices satisfies Hadwiger's conjecture.
