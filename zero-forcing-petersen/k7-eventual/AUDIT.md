# Certificate audit

## Exact DP semantics

The native verifier uses a flat table of packed integer states and exact integer
transitions. Its retained key consists of:

- the color of \(u_0\) and the colors of \(v_0,\ldots,v_6\);
- the latest outer color and latest seven inner colors;
- the exact \(Y\)-count.

For each key it stores the minimum \(B\)-count. This is exact dominance: future legality
and cyclic closure depend only on the key, every continuation adds the same \(B\)-cost,
and the final question is whether that cost is at most 15.

The key occupies bits 0–33 and its minimum cost starts at bit 40. Every transition checks
the new spoke, outer edge, and step-seven inner edge. Closure checks the outer wrap edge,
all seven inner wrap edges, and \(|Y|=n\).

The pruning \(Y\ge2\ell-56\) at length \(\ell\) removes only states that cannot reach
\(|Y|=t\) at any endpoint \(t\le56\), because each future column contributes at most two
\(Y\)'s. The frozen transcript contains every reduced layer size and two 64-bit
fingerprints of every layer and cyclic closure.

## Outer-\(B\) anchoring

The verifier fixes \(u_0=B\) by rotation. This is complete. If an admissible coloring had
no outer \(B\), the outer cycle could not contain both \(A\) and \(Y\), so it would be
monochromatic. If it were all \(A\), the spokes would forbid every inner \(Y\), contrary
to \(|Y|=n\). If it were all \(Y\), those outer vertices already supply all \(n\)
\(Y\)'s; every inner vertex would then be \(B\), contrary to \(|B|\le15<n\).

## Positive control

The repeated seven-column word for \(P(49,7)\) is replayed against adjacency generated
independently in Python. It selects exactly 49 vertices and has exact internal boundary
14. More generally, the same block on \(P(7m,7)\) has exact boundary \(2m\).
This family concerns only the balanced-separator lower-bound route, not zero forcing
sets.

## Independent anchoring cross-check

An earlier full DP required only that column zero contain \(B\), without the outer-\(B\)
reduction. On orders \(44,\ldots,51\), it independently gave positive closures at 44 and
49 and zero closures at \(45,\ldots,48,50,51\), exactly matching the anchored verifier's
existence results. Its reduced closure counts differ because the state quotient and
rotation convention differ.

## Transfer direction

The verifier compares the complete contracted edge set with \(P(n-7,7)\). The proof uses

\[
\operatorname{pw}(P(n-7,7))\le\operatorname{pw}(P(n,7))\le Z(P(n,7)).
\]

It does not assume that zero forcing is minor-monotone. The \(n=49\) control is irrelevant
to \(n\ge50\): its residue class stops at base 56 under the seven-column transfer.
