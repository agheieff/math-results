# Prior-art audit

Audit date: 2026-07-23.

## Direct source

Dickson Y. B. Annor and Ben Howerton,
[*Induced Subgraph Bounds on the Zero Forcing Number and a
\((\chi,\omega,Z)\)-Conjecture*](https://arxiv.org/abs/2607.20137v1),
arXiv:2607.20137v1, submitted 2026-07-22, propose

\[
\chi(G)\le
\left\lceil\frac{\omega(G)+Z(G)+1}{2}\right\rceil.
\]

They also formulate Condition \((R)\). Their Section 5 reports exact
finite verification of that condition for the Mycielskians
\(M(C_5),\ldots,M(C_{13})\), among other graphs. The paper does not state or
prove an all-\(q\) formula for \(Z(M(C_q))\). The theorem in this lane also
includes \(M(C_4)\), below their reported Mycielskian range.

## Matrix method

The inequality

\[
\operatorname{null}(A)\le Z(G)\qquad(A\in\mathcal S(G))
\]

comes from the AIM Minimum Rank--Special Graphs Work Group,
[*Zero forcing sets and the minimum rank of
graphs*](https://doi.org/10.1016/j.laa.2007.10.009),
Linear Algebra and its Applications 428 (2008), 1628--1648. The lower
certificate in this lane is an application of that established method.

## Search scope

Web, arXiv, and exact-phrase searches were run for combinations of
“zero forcing”, “zero forcing number”, “Mycielski”, “Mycielskian”, “minimum
rank”, and “maximum nullity”. They found work on other Mycielskian graph
parameters and general zero-forcing theory, but no earlier exact formula for
\(Z(M(C_q))\) over all cycles.

This is a limited current-source audit, not a guarantee of
literature-wide novelty. Accordingly, [THEOREM.md](THEOREM.md) states the
resolved result without a novelty claim.
