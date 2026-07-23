# Certificate audit

## Force schedule

The verifier does not merely compute a closure. It replays the symbolic force list in order
and checks that every source is black and every target is its unique white neighbor. The
number of recorded forces is checked against the number of vertices outside the initial set.

## Minor construction

The verifier deletes exactly the last \(k\) spokes and applies the contractions from the
proof. It compares the complete resulting simple edge set with a fresh construction of
\(P(n-k,k)\). No graph-isomorphism heuristic or symmetry reduction is used.

## Infinite scope

Finite replay ranges are regression tests for the two implementations. The claims for all
valid \(k,n\) follow from the index arguments in `THEOREM.md`.

## Transfer direction

The proof uses

\[
P(n-k,k)\preccurlyeq P(n,k)
\quad\Longrightarrow\quad
\operatorname{pw}(P(n-k,k))\le\operatorname{pw}(P(n,k)).
\]

It never assumes that zero forcing itself is minor-monotone.
