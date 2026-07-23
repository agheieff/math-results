# Certificate and replay

The path edges \(01,12,\ldots,22\,23\) are fixed positive. Bit zero is the
remaining step-1 edge \(23\,0\), and bit \(i+1\) is the step-2 edge
\(\{i,i+2\}\). Thus masks \(0\le m<2^{25}\) enumerate every switching class
exactly once.

For each resolved mask, `cpp/enumerate.cpp` reconstructs
\(x=A_m^{2k}e_s\) and verifies

\[
125\lVert A_mx\rVert^2>958\lVert x\rVert^2.
\]

The saved [summary](artifacts/n24-certificate.json) is not a trusted witness
database: replay re-enumerates every mask and reconstructs every witness.

The two unresolved masks are rebuilt independently from alternating triangle
flux and negative Hamilton holonomy. Pure Python integer arithmetic checks
their characteristic polynomials, the target algebraic polynomial, and its
rational Sturm isolation.

Run:

```sh
uv run signed-circulant-n24-check
```
