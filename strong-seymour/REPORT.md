# Strong Seymour tournaments: exact first-open-order result

## Result

Every tournament on at most 13 vertices has a strong Seymour vertex.

Bai, Li, and Park prove that every oriented graph of minimum outdegree at most 5 has a
strong Seymour vertex. This settles tournaments through order 12. Order 13 is the first case
not covered by that theorem. An exact Hall-witness CNF for an order-13 counterexample is
UNSAT, with a checked DRAT certificate; see `proof/encoding.md` and
`proof/verification.md`.

This is a computer-assisted extension by one order, not a proof of the full tournament
conjecture. I found no indexed follow-up or counterexample in searches on 23 July 2026 for
the exact phrases “strong Seymour vertex”, “every tournament has a strong Seymour vertex”,
and the paper identifier. Given how new the preprint is, that search is weak evidence and no
claim of priority or novelty is made.

## Formalization decision

A Lean formalization would require importing or rebuilding a proof-producing SAT stack. The finite
result is instead double-checked by a written Hall reduction, deterministic CNF regeneration, and an
independently replayed DRAT refutation. This follows the fallback allowed by `PLAN.md`; the result is
not described as Lean-formalized.

## Sources

- [Bai--Li--Park, *Towards a strengthening of the second neighborhood conjecture*](https://arxiv.org/abs/2607.18047), submitted 20 July 2026.
- [DRAT-trim format and checker](https://github.com/marijnheule/drat-trim).
- [CaDiCaL 2.0 proof-format description](https://doi.org/10.1007/978-3-031-65627-9_7).

## Independent checks

The model verifier does not use SAT witness variables. It recomputes first and second
out-neighbourhoods, then exhaustively tries every feasible injection from the first to the
second. Its matching routine is cross-checked against a separate augmenting-path algorithm
on all 512 labelled `3 x 3` bipartite graphs.

No order-13 model exists, so there is no counterexample JSON to validate. The same verifier
is ready for later satisfiable orders.
