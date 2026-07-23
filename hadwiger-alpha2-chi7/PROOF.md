# Frozen reduction and proof

## 1. Complement translation

Let \(F=\overline G\).

- \(\alpha(G)\leq2\) if and only if \(F\) is triangle-free.
- A colour class of \(G\) has size at most two. Its two-vertex colour classes
  are edges of \(F\), so
  \[
  \chi(G)=|V(G)|-\nu(F).
  \]
- Hence, on 13 vertices, \(\chi(G)=7\) if and only if \(\nu(F)=6\).

## 2. Exact seagull/matching criterion

A *seagull* is an induced \(P_3\). Fix a clique \(Z\) of four vertices in
\(G\), equivalently an independent four-set in \(F\), and put
\(W=V(G)\setminus Z\).

There is a \(K_7\)-model whose branch sets are the four singleton vertices of
\(Z\) and three seagulls partitioning \(W\) if and only if there are:

1. a three-edge matching
   \(M=\{x_iy_i:1\leq i\leq3\}\) in \(F[W]\), and
2. a bijection from the three vertices of \(W\setminus V(M)\) to \(M\)

such that the vertex assigned to \(x_iy_i\) is adjacent in \(F\) to neither
\(x_i\) nor \(y_i\).

Indeed, \(\{x_i,z_i,y_i\}\) then induces the path
\(x_i-z_i-y_i\) in \(G\), and the converse reads the unique nonedge between
the endpoints of each induced path.

Every seagull in a graph with independence number at most two is dominating:
an outside vertex nonadjacent to all three path vertices would form an
independent triple with the two path endpoints. Consequently the three
seagulls are pairwise adjacent and adjacent to all four singleton branch
sets. The criterion therefore certifies a \(K_7\)-minor.

## 3. The 13-vertex theorem

Assume for contradiction that the frozen statement is false. Then
Hadwiger's conjecture with \(\alpha\leq2\) has a counterexample on at most
13 vertices; choose one, \(G\), with the fewest vertices. The standard
minimal-counterexample results of Plummer--Stiebitz--Toft say that \(G\) is
vertex-critical, is 7-connected, and satisfies
\[
|V(G)|=2\chi(G)-1.
\]
Hadwiger's conjecture through chromatic number six gives \(\chi(G)\geq7\).
Because \(|V(G)|\leq13\), the displayed equality forces
\[
|V(G)|=13,\qquad \chi(G)=7.
\]
Their Theorem 3.3(b) also forces \(\omega(G)\leq\chi(G)-3=4\): a clique of
size at least \(\chi(G)-2\) would already yield a \(K_{\chi(G)}\)-minor.

Since \(F\) is triangle-free and \(R(3,4)=9\), it has an independent set of
four vertices. Thus \(\omega(G)=4\). Choose a four-clique \(Z\), put
\(W=V(G)\setminus Z\), and let \(H=G[W]\). In particular,
\(\alpha(H)\leq2\). We verify the four hypotheses of the
Chudnovsky--Seymour seagull-packing theorem for \(H\) and \(k=3\).

1. \(|V(H)|=9=3k\), and \(H\) is not the five-wheel.
2. Deleting \(Z\) lowers connectivity by at most four, so
   \(\kappa(H)\geq3\).
3. Because \(G\) is vertex-critical, \(\chi(H)\leq6\). The complement
   matching formula gives
   \[
   9-\nu(\overline H)=\chi(H)\leq6,
   \]
   hence \(\nu(\overline H)\geq3\).
4. Let \(C\) be a clique of \(H\), and let \(D\) be the vertices outside
   \(C\) having both a neighbour and a non-neighbour in \(C\). Since
   \[
   2\operatorname{cap}_H(C)=|D|+|V(H)\setminus C|,
   \]
   the required capacity condition is the following inequality. Since
   \(|C|\leq4\), we have \(|V(H)\setminus C|\geq5\). Only equality needs
   attention. If \(|C|=4\) and \(D=\varnothing\), no outside vertex is
   complete to \(C\), since that would create a five-clique. Every outside
   vertex is therefore anticomplete to \(C\). Then \(H\) is disconnected and
   \(Z\) is a vertex cut of \(G\) of size four, contradicting the
   7-connectivity of \(G\). Thus
   \[
   |D|+|V(H)\setminus C|\geq6=2k.
   \]

The seagull-packing theorem now gives three vertex-disjoint seagulls in
\(H\). They cover its nine vertices. Together with the four singleton
vertices of \(Z\), they form the \(K_7\)-model from Section 2, a
contradiction.

## 4. Why the six-pair reduction is false

A stronger-looking reduction asks for a partition of all 13 vertices into
one singleton and six two-vertex branch sets. Equivalently, it asks for a
perfect matching of \(G-v\) whose six edges are pairwise adjacent and each
adjacent to \(v\).

Take \(F=K_{6,7}\). It is triangle-free and \(\nu(F)=6\), so
\[
G=\overline F=K_6\mathbin{\dot\cup}K_7,\qquad \chi(G)=7.
\]
The \(K_7\) component is already the required minor. But no six-edge
connected matching can cover both components of \(G\), so the proposed
six-pair criterion fails. It is sufficient, not necessary.
