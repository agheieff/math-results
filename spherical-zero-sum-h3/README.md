# Spherical zero-sum search in dimension three

The normalized \(H_3\) root system has exactly 30 points, 20 zero-sum triples, and
independence number 20. It therefore reproduces the known finite-configuration bound
\(m_3\leq 2/3\) and does not improve it.

A bounded search over shared-axis \(A_3/H_3\) gluings and natural icosahedral orbits found no
configuration with independence ratio below \(2/3\). That broader target remains
**inconclusive**: the search is finite, and its geometric layer uses floating-point recovery.

The exact \(H_3\) result is proved by a perfect matching of ten zero-sum triples and an explicit
independent 20-set, both checked in \(\mathbb Q(\sqrt5)\). See [REPORT.md](REPORT.md) for the
mathematics, [SEARCH.md](SEARCH.md) for the search boundary, and
[CERTIFICATE.md](CERTIFICATE.md) for reproduction commands.

```sh
uv run spherical-zero-sum-h3-check
uv run spherical-zero-sum-h3-check --full-search
```
