# Construction audit

## Cardinalities

Each parity block has exactly \(k\) columns, exactly \(k\) symbols \(Y\), and exactly two
symbols \(B\). Repeating it \(m\) times gives \(n=km\) \(Y\)-vertices, so the non-\(Y\)
vertices form an \(n\)-vertex half-set.

## Edge check

The outer colors consist of an \(A\)-run and a \(Y\)-run separated by the two outer
\(B\)'s. Every spoke is one of \(AA,BA,BY,YY\), so no spoke is \(A\)-\(Y\).
Because the block is repeated with period \(k\), every step-\(k\) inner edge joins equal
positions in consecutive blocks and therefore equal colors.

Thus there is no \(A\)-\(Y\) edge. Both outer \(B\)'s in every block have a \(Y\)-neighbor,
while every \(A\)-vertex has only \(A\)- or \(B\)-neighbors. The exact internal boundary
is therefore precisely the \(2m\) displayed \(B\)-vertices.

## Replay scope

The verifier independently constructs graph adjacency and recomputes the internal
boundary for every \(3\le k\le40\) and \(3\le m\le10\), plus the square cases
\(6\le k\le40\). These finite checks audit the implementation; the proof above is
symbolic for all \(k,m\ge3\).
