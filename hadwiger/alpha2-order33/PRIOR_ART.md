# Prior-art boundary

This lane closes the next possible minimum-counterexample order after the
order-31 lane. The source audit was last updated on 2026-07-23.

- `../hadwiger-alpha2-order31/PROOF.md` proves the conjecture through
  order 32. The present lane is logically downstream of that result.

- M. D. Plummer, M. Stiebitz, and B. Toft, *On a special case of
  Hadwiger's conjecture*, Discussiones Mathematicae Graph Theory 23
  (2003), 333--363,
  [DOI 10.7151/dmgt.1206](https://doi.org/10.7151/dmgt.1206).
  This is the standard source for the exact odd order and connectivity of
  a minimum-order counterexample with independence two.

- M. Chudnovsky and P. Seymour, *Packing seagulls*, Combinatorica 32
  (2012), 251--282,
  [DOI 10.1007/s00493-012-2594-2](https://doi.org/10.1007/s00493-012-2594-2),
  [author PDF](https://web.math.princeton.edu/~mchudnov/seagulls.pdf).
  Theorem 1.6 is the exact seagull-packing criterion used here, and their
  clique threshold rules out a \(K_9\) in an order-33 counterexample.

- S. Brandt, G. Brinkmann, and T. Harmuth, *All Ramsey numbers
  \(r(K_3,G)\) for connected graphs of order 9*, Electronic Journal of
  Combinatorics 5 (1998), R7,
  [PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/EJC/Volume_5/PDF/v5i1r7.pdf).
  The exact value \(R(3,K_9-e)=31\) supplies the \(K_9-e\) core.

- D. Carter, *Hadwiger's Conjecture with Certain Forbidden Induced
  Subgraphs*, Experimental Mathematics (2024),
  [DOI 10.1080/10586458.2024.2428958](https://doi.org/10.1080/10586458.2024.2428958),
  [arXiv:2211.00259](https://arxiv.org/abs/2211.00259).
  Carter's contiguous general bound is order 30, with order 31 isolated
  as the first possible minimal-counterexample order.

- D. Costa, K. Luu, D. R. Wood, and S. M. Yip, *Verifying Hadwiger's
  Conjecture for Examples of Graphs with \(\alpha(G)=2\)* (2025),
  [arXiv:2512.17114](https://arxiv.org/abs/2512.17114).
  Theorem 2.28 still records the general boundary as order 30. The
  present proof does not use that preprint's Lemma 2.4.

- M. Scully and Z.-X. Song, *Dominating Hadwiger's Conjecture for graphs
  \(G\) with \(\alpha(G)=2\)* (2025),
  [arXiv:2510.12564](https://arxiv.org/abs/2510.12564).
  Their stronger dominating-minor theorem requires
  \(2\omega(G)\geq\lceil n/2\rceil+1\); at
  \(n=33,\omega=8\), its two sides are 16 and 18.

A targeted search found no source extending the contiguous general order
bound beyond 30. The order-31 and order-33 lanes together give the bound
through 34. That search is not a proof of novelty; both proofs should
receive independent expert review before any public novelty claim.
