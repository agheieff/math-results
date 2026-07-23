# Independent red-team audit

Audit date: 2026-07-23.

Verdict: **PASS** for the frozen \(n=20\) statement.

The audit independently checked the path-tree gauge and bit mapping, the
quartic and Sturm isolation for the target radius, the Rayleigh certificates,
and all exhaustion counts. A full replay with undefined-behavior sanitization
found no integer overflow.

The exact count split reproduced as

\[
2{,}096{,}980+162+8+2=2^{21}.
\]

The two survivors were independently reconstructed from alternating triangle
flux and negative Hamilton holonomy. Bareiss determinants evaluated at 21
integer points, followed by exact interpolation, gave for each survivor

\[
(x^2-2)^2
\left(x^8-18x^6+114x^4-302x^2+281\right)^2.
\]

The audit also passed the locked dependency check, five tests, Ruff, format
check, strict mypy, and the full command-line replay. It confirms only
\(C_{20}(1,2)\), not the source's all-even-\(n\) conjecture or a
literature-wide priority claim.
