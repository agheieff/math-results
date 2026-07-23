# Proof report

## 1. Definitions and statement

All graphs below are finite, simple, and undirected. For a graph \(H\), let
\(\tau(H)\) be the maximum number of pairwise edge-disjoint spanning trees in
\(H\), and define

\[
\bar\tau(G)=\max\{\tau(H):H\subseteq G\}.
\]

Wang and Tian call \(G\) **\(\tau_k\)-maximal** when

\[
\bar\tau(G)\le k
\quad\text{and}\quad
\bar\tau(G+e)\ge k+1
\quad\text{for every }e\in E(G^c).
\]

We prove their Conjecture 1, the statement immediately preceding Theorem 3.8.

**Theorem.** Let \(k\ge1\) and \(n\ge2k+2\). Every \(\tau_k\)-maximal
\(n\)-vertex graph \(G\) has

\[
|E(G)|=(k+1)(n-1)-1.
\]

Set \(q=k+1\). Thus \(q\ge2\) and the order hypothesis is \(n\ge2q\).

## 2. The exact sparsity reformulation

For a nonempty edge set \(F\), write \(V(F)\) for its incident vertices.

**Lemma 1.** For every simple graph \(G\),

\[
\bar\tau(G)\le q-1
\quad\Longleftrightarrow\quad
|F|\le q|V(F)|-(q+1)
\quad\text{for every nonempty }F\subseteq E(G).
\tag{1}
\]

**Proof.** We first record the density implication

\[
\bar\tau(J)<q,\ |V(J)|=h\ge2
\quad\Longrightarrow\quad
|E(J)|<q(h-1).
\tag{2}
\]

This follows by induction on \(h\) from the Nash--Williams--Tutte theorem.
The case \(h=2\) is immediate because \(J\) is simple and \(q\ge2\). In the
inductive step, \(\tau(J)<q\), so there is a partition
\(\mathcal P=\{P_1,\ldots,P_t\}\), \(t\ge2\), with fewer than \(q(t-1)\)
crossing edges. Every non-singleton \(J[P_i]\) also has
\(\bar\tau(J[P_i])<q\), so induction gives fewer than
\(q(|P_i|-1)\) internal edges; a singleton contributes zero. Summing gives

\[
|E(J)|<q(t-1)+q\sum_i(|P_i|-1)=q(h-1).
\]

Now suppose \(\bar\tau(G)\le q-1\). For nonempty \(F\subseteq E(G)\), apply
(2) to \(J=(V(F),F)\). Integrality turns the strict inequality into

\[
|F|\le q(|V(F)|-1)-1=q|V(F)|-(q+1).
\]

Conversely, suppose (1) holds and some \(H\subseteq G\) contains \(q\)
edge-disjoint spanning trees. Necessarily \(h=|V(H)|\ge2\), since a
one-vertex graph has at most one distinct spanning tree and \(q\ge2\).
Their union has \(q(h-1)\) edges and has incident set \(V(H)\). This
contradicts (1). \(\square\)

There is no hidden isolated-vertex assumption. Equivalently, for every vertex
set \(X\subseteq V(G)\),

\[
i_G(X)\le \max\{0,q|X|-(q+1)\},
\tag{3}
\]

where \(i_G(X)=|E(G[X])|\). Empty and singleton sets have bound zero. For
\(|X|\ge2\), (3) follows from (1) by taking \(F=E(G[X])\), unless that set is
empty; the reverse direction follows by taking \(X=V(F)\). Thus (1) is exactly
the standard definition of a \((q,q+1)\)-sparse graph, including the
upper-range singleton convention.

## 3. The count-matroid input and simple restriction

We use the \((a,\ell)\)-sparsity matroid theorem of Lee and Streinu:
for \(0\le\ell<2a\), subject to their stated small-order conditions, sparse
edge sets form a matroid on the appropriate complete multigraph, and tight
graphs are its bases.

Apply it with

\[
a=q,\qquad \ell=q+1.
\]

The parameter condition holds because \(q\ge2\) gives
\(q+1<2q\). The order conditions also hold:

- if \(q=2\), then \(\ell=3=3q/2\), and their upper-range theorem requires
  \(n=2\) or \(n\ge \ell/(2q-\ell)=3\);
- if \(q\ge3\), then \(q<q+1<3q/2\), and their theorem requires \(n\ge2\).

Our hypothesis \(n\ge2q\) is stronger in both cases.

In this upper range the ambient graph is loopless and has
\(2q-\ell=q-1\) parallel copies of every pair. Choose one copy of every pair;
the chosen ground set is a simple \(K_n\). Restricting a matroid to a subset
of its ground set is again a matroid. Lee and Streinu also state this deletion
step explicitly: after deleting ground-set edges, bases are the maximal sparse
subgraphs of the remaining ground graph.

Source caveat: Theorem 2's displayed ground-set phrase literally writes
`k-l` loop copies even in the upper range, where that number is negative.
Their Lemma 1(3), the theorem's construction, and the deletion paragraph make
the intended convention unambiguous: there are no loops when \(\ell>q\), and
there are \(2q-\ell\) parallel copies of each ordinary edge.

Let \(M_{q,n}\) denote this restriction to \(E(K_n)\). Its independent sets are
exactly the edge sets of simple \((q,q+1)\)-sparse graphs. By Lemma 1,

\[
E(G)\text{ is independent in }M_{q,n}
\quad\Longleftrightarrow\quad
\bar\tau(G)\le q-1.
\tag{4}
\]

The definition of \(\tau_k\)-maximality says precisely that \(E(G)\) is
independent but \(E(G)\cup\{e\}\) is dependent for every ground element
\(e\notin E(G)\). Therefore \(E(G)\) is an inclusion-maximal independent set,
hence a basis of \(M_{q,n}\).

## 4. Rank of the simple restriction

Every independent \(I\subseteq E(K_n)\) satisfies (3) with \(X=V(K_n)\), so

\[
|I|\le qn-(q+1).
\tag{5}
\]

It remains to show that equality is attainable using simple edges.

For \(n=2q\), take \(B_{2q}=K_{2q}-e\). It has

\[
\binom{2q}{2}-1=q(2q)-(q+1)
\]

edges. If \(2\le r\le2q-1\), then

\[
qr-(q+1)-\binom r2
=q-2+\frac{(r-2)(2q-1-r)}2\ge0.
\]

Thus every proper \(r\)-vertex set meets the sparsity bound. The full vertex
set meets it with equality because of the deleted edge, so \(B_{2q}\) is
\((q,q+1)\)-tight.

Given a tight graph \(B_m\) with \(m\ge2q\), add a new vertex \(v\) adjacent
to any \(q\) distinct old vertices. This adds \(q\) edges. To check sparsity,
consider a vertex set \(X\) containing \(v\), and put \(X'=X-\{v\}\).
If \(B_m[X']\) has an edge, then

\[
i_{B_{m+1}}(X)
\le q|X'|-(q+1)+q
=q|X|-(q+1).
\]

If \(B_m[X']\) has no edge, then all induced edges meet \(v\), so
\(i_{B_{m+1}}(X)\le |X|-1\). For \(|X|\ge2\),

\[
|X|-1\le q|X|-(q+1),
\]

and the singleton case has zero edges. Sets not containing \(v\) retain the
old bound. Hence the extension is sparse, and its edge count is again
\(q(m+1)-(q+1)\).

Induction constructs a simple tight graph for every \(n\ge2q\). Together with
(5), this proves

\[
\operatorname{rank}(M_{q,n})=qn-(q+1)=q(n-1)-1.
\tag{6}
\]

Every basis, in particular every \(\tau_k\)-maximal graph, has this many
edges. Substituting \(q=k+1\) proves the theorem. \(\square\)

## 5. Dependency and range audit

The proof imports exactly two standard results:

1. Nash--Williams--Tutte's partition characterization of edge-disjoint
   spanning-tree packings, used to prove (2).
2. Lee--Streinu's \((a,\ell)\)-sparsity matroid theorem, plus ordinary matroid
   restriction and the fact that maximal independent sets are bases.

The rank calculation and the required simple tight graph are proved here;
they are not inferred from the multigraph rank.

The hypotheses matter. The case \(k=0\) would give \(q=1,\ell=2=2q\), outside
the count-matroid range. For \(n\le2k+1\), Wang and Tian note that \(K_n\) is
already \(\tau_k\)-maximal, so their claimed formula is not the relevant one.

## 6. Independent finite checks

The bundled checker enumerates labeled simple graphs. Its direct predicate
examines every possible subgraph vertex set and every set partition, applying
Nash--Williams--Tutte without using Lemma 1. It separately evaluates all
\((q,q+1)\)-sparsity inequalities, asserts that the predicates agree, and then
tests maximality by every missing edge.

The default run gives:

| \(q\) | \(n\) | labeled graphs | maximal graphs | maximal edge sizes |
|---:|---:|---:|---:|---:|
| 2 | 4 | 64 | 6 | 5 |
| 2 | 5 | 1,024 | 100 | 7 |
| 2 | 6 | 32,768 | 3,355 | 9 |
| 3 | 6 | 32,768 | 15 | 14 |

These checks are regression evidence only; the proof is the matroid argument
above.
