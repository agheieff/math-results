# Certificate format and replay

## Coverage

`cpp/enumerate.cpp` fixes the path-tree gauge and loops over every integer

\[
0\le m<2^{21}.
\]

For each nonexceptional mask it produces, and immediately verifies, an integer
Rayleigh witness \(x=A_m^{2k}e_s\) above the exact separator \(38/5\). The JSON
histograms count masks by \((s,k)\). Their sum plus the two unresolved masks is
exactly \(2^{21}\).

The saved run is [artifacts/n20-certificate.json](artifacts/n20-certificate.json).
It is a summary, not a trusted witness database: replay reconstructs every
witness from its mask.

## Independent exceptional-mask check

`signed_circulant/model.py` constructs the two twisted masks from alternating
triangle flux and negative Hamilton holonomy, independently of the C++
enumerator. `signed_circulant/exact.py` then:

1. computes both characteristic polynomials using integer matrix powers and
   Newton identities;
2. compares them with the explicit factored polynomial; and
3. checks the target quartic with rational Sturm arithmetic.

## Replay

```sh
uv run signed-circulant-check
```

The command recompiles the C++ source, exhausts all \(2^{21}\) classes, parses
its JSON output, compares the two implementations' exceptional masks, and runs
the independent characteristic-polynomial check.
