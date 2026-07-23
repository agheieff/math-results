# Prior-art boundary

This lane combines established ingredients at the first order left open
by Carter. The source audit was last updated on 2026-07-23.

- D. Carter, *Hadwiger's Conjecture with Certain Forbidden Induced
  Subgraphs*, Experimental Mathematics (2024),
  [DOI 10.1080/10586458.2024.2428958](https://doi.org/10.1080/10586458.2024.2428958),
  [arXiv:2211.00259](https://arxiv.org/abs/2211.00259).
  Theorem 3 proves that \(K_8\) is unavoidable in a counterexample with
  independence two. Corollary 1 states that a minimal counterexample has
  31 vertices or at least 33. Thus order 32 is not a minimal-counterexample
  order, while the published contiguous all-graphs boundary is 30.

- M. Chudnovsky and P. Seymour, *Packing seagulls*, Combinatorica 32
  (2012), 251--282,
  [DOI 10.1007/s00493-012-2594-2](https://doi.org/10.1007/s00493-012-2594-2),
  [author PDF](https://web.math.princeton.edu/~mchudnov/seagulls.pdf).
  Theorem 1.6 is the exact four-condition seagull-packing criterion used
  here; Theorems 1.3--1.5 give the clique threshold that rules out a
  \(K_9\) in a 31-vertex counterexample.

- M. D. Plummer, M. Stiebitz, and B. Toft, *On a special case of
  Hadwiger's conjecture*, Discussiones Mathematicae Graph Theory 23
  (2003), 333--363,
  [DOI 10.7151/dmgt.1206](https://doi.org/10.7151/dmgt.1206).
  This is the standard source for the criticality, exact-order, and
  connectivity properties of a minimum-order counterexample with
  independence two.

- S. Brandt, G. Brinkmann, and T. Harmuth, *All Ramsey numbers
  \(r(K_3,G)\) for connected graphs of order 9*, Electronic Journal of
  Combinatorics 5 (1998), R7,
  [PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/EJC/Volume_5/PDF/v5i1r7.pdf).
  The paper records \(R(3,K_9-e)=31\), the exact input producing the
  \(K_9-e\) core.

- D. Costa, K. Luu, D. R. Wood, and S. M. Yip, *Verifying Hadwiger's
  Conjecture for Examples of Graphs with \(\alpha(G)=2\)* (2025),
  [arXiv:2512.17114](https://arxiv.org/abs/2512.17114).
  Theorem 2.8 surveys counterexample properties, and Theorem 2.28 still
  states the Carter boundary as order 30. The present proof takes its
  needed minimum-counterexample properties from Plummer--Stiebitz--Toft.
  The current arXiv version's Lemma 2.4, asserting that deleting two
  nonadjacent vertices from every \((2k-1)\)-vertex \(k\)-critical
  independence-two graph leaves a \((k-1)\)-critical graph, is not used:
  as written it fails for \(C_5\), where deleting a nonadjacent pair leaves
  \(K_2\mathbin{\dot\cup}K_1\). The antimatching step here instead uses the
  elementary unmatched-vertices bound in Section 3 of `PROOF.md`.

- M. Scully and Z.-X. Song, *Dominating Hadwiger's Conjecture for graphs
  \(G\) with \(\alpha(G)=2\)* (2025),
  [arXiv:2510.12564](https://arxiv.org/abs/2510.12564).
  Their stronger dominating-minor theorem applies when
  \(2\omega(G)\geq\lceil n/2\rceil+1\). At the unresolved parameters
  \(n=31,\omega=8\), it misses by exactly one.

A targeted search found no source extending the contiguous general order
bound beyond 30. Closing the possible order-31 minimal counterexample,
together with Carter's exclusion of minimal order 32, gives the bound
through 32. The search is not a proof of novelty; the proof should receive
independent expert review before any public novelty claim.
