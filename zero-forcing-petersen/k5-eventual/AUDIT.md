# Certificate audit

## Exact DP semantics

The native verifier uses sets of packed integer states; it performs no numerical
optimization, heuristic pruning, or automorphism quotient beyond fixing a dirty column by
rotation. Histories are merged only after all edges incident to forgotten vertices have
been checked.

The packed fields are disjoint: two outer colors, two five-trit inner words, the separator
count, and the \(Y\)-count. Every transition checks all newly completed graph constraints.
Cardinality pruning uses only the maximum two future \(Y\)'s per unprocessed column.

The frozen transcript includes every layer size plus two order-independent 64-bit
fingerprints of every state set. A displayed \(n=28\) coloring is a positive control.

## Off-by-one convention

Internal boundary at least 12 for every \(n\)-vertex half-set makes every layout's
\(n\)-vertex prefix have boundary at least 12. Vertex separation equals pathwidth with
width equal to maximum bag size minus one.

## Transfer direction

The verifier compares the complete contracted edge set with \(P(n-5,5)\). The proof uses

\[
\operatorname{pw}(P(n-5,5))\le\operatorname{pw}(P(n,5))\le Z(P(n,5)).
\]

It does not assume that zero forcing is minor-monotone.
