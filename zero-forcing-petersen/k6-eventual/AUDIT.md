# Certificate audit

## Exact DP semantics

The native verifier uses a flat table of packed integer states. It performs exact integer
transitions and no numerical optimization. The retained key consists of:

- the colors of \(u_0\) and \(v_0,\ldots,v_5\);
- the latest outer color and latest six inner colors;
- the exact \(Y\)-count.

For each key it stores the minimum \(B\)-count. This dominance is exact: future legality
and cyclic closure depend only on the key, every continuation adds the same \(B\)-cost,
and the final question is only whether the cost is at most 13.

The key occupies bits 0–29 and its minimum cost occupies bits 32–35. Every generated key
is nonzero because column zero contains \(B\). Each transition checks the new spoke, outer
edge, and step-six inner edge. Closure checks the outer wrap edge, all six inner wrap
edges, and the half-set condition \(|Y|=n\).

The pruning \(Y\ge2\ell-42\) at length \(\ell\) removes only states that cannot reach
\(|Y|=t\) at any endpoint \(t\le42\), since each future column contributes at most two
\(Y\)'s. The frozen transcript includes every reduced layer size and two 64-bit
fingerprints of every layer and cyclic closure.

## Positive control

The displayed \(n=36\) word is replayed against adjacency generated independently in
Python. It selects exactly 36 vertices and has exact internal boundary 13. The native
automaton also finds boundary-at-most-13 closures at \(n=34\) and \(n=36\), while finding
none at the isolated exact order 35 or at the six eventual theorem bases.

## Off-by-one convention

Internal boundary at least 14 for every \(n\)-vertex half-set makes every layout's
\(n\)-vertex prefix have boundary at least 14. Vertex separation equals pathwidth with
width equal to maximum bag size minus one.

## Transfer direction

The verifier compares the complete contracted edge set with \(P(n-6,6)\). The proof uses

\[
\operatorname{pw}(P(n-6,6))\le\operatorname{pw}(P(n,6))\le Z(P(n,6)).
\]

It does not assume that zero forcing is minor-monotone. The \(n=36\) positive control is
irrelevant to \(n\ge37\): the residue-zero chain stops at base 42, never at 36.

## Independent replay

The complete native transcript was compiled and run independently with g++ and clang++.
Both produced closure profile

\[
(40,0,124,0,0,0,0,0,0)
\]

for orders \(34,\ldots,42\) and transcript SHA-256
`4a85f75724dc7c70a2503feba361c93c151b77275877d43dbdda7ce09fc392a5`.
