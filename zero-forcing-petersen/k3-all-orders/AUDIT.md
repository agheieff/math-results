# Certificate audit

## Reachable-prefix recurrence

A state is only a vertex subset. Layer \(j\) contains exactly those \(j\)-sets that can occur
as the first \(j\) vertices of an ordering whose every prefix has internal boundary at most
seven. Layers through size seven contain every subset. Size eight is enumerated directly;
later layers are obtained by adding one vertex to a preceding reachable state and checking
the boundary. Therefore an empty layer is a lower certificate, not a failed heuristic search.

The boundary bitset formula is tested against the adjacency-list definition on exhaustive
small subsets. Target runs use no automorphism reduction.

## Off-by-one convention

Vertex separation is the maximum boundary size and equals pathwidth, where pathwidth is
maximum bag size minus one. Thus excluding separation at most seven proves pathwidth at least
eight.

## Transfer

The verifier compares the complete simple edge set after the six contractions with the edge
set of \(P(n-3,3)\). The proof uses minor monotonicity in the direction
\(\operatorname{pw}(P(n-3,3))\le\operatorname{pw}(P(n,3))\).

## Scope

The theorem is finite and applies exactly to every integer \(n\ge13\). The bi-infinite strip
result is not used. The symbolic upper-bound proof is accompanied by direct replays, but the
finite replay range is only a regression test, not the reason the upper bound holds for all
orders.
