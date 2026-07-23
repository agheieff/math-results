# Audit

The certificate records the exact two zero rows, the left derivative row, both source
URLs, and SHA-256 hashes of the complete gzip files. The verifier independently:

1. recomputes both \(\theta/\pi\) values at 90-decimal precision;
2. derives the four open-interval Gram indices;
3. derives the sign pattern from the first-index parity and \(Z'(\gamma_-)\);
4. checks large endpoint and derivative safety margins.

With source files supplied, it also verifies both whole-file hashes and the frozen
rows. `--full-scan` streams all ten million paired rows, refines near-integer theta
values at high precision, and reproduces the count histogram and first counterexample.

The Riemann--Siegel expansion retains terms through \(t^{-7}\). At \(t\approx10^{25}\),
the omitted asymptotic correction is negligible compared with the displayed endpoint
margins.
