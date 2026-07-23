# Independent audit

Audit date: 2026-07-23.

An independent script reconstructed each twisted matrix directly from
\(\tau_i=\tau_0(-1)^i\) and negative Hamilton holonomy, without importing the
package model. The resulting matrix SHA-256 hashes are:

| mask | matrix SHA-256 |
| ---: | --- |
| 55924053 | `c7f2f217dd5939a1348fa42ca7e04157b8e13fe4c1e073a521b5c095cd41a3ea` |
| 78293675 | `de4087b70d14ab64515f456ff7e730f212b202891e128542792183d9706090bc` |

For each matrix, fraction-free Bareiss determinants evaluated
\(\det(jI-A)\) at every integer \(0\le j\le26\). Exact forward-difference
interpolation returned the saved characteristic polynomial and the factorization

\[
(x^2-4)
\left(x^{12}-24x^{10}+227x^8-1085x^6+2774x^4-3609x^2+1873\right)^2.
\]

The full enumerator was separately compiled and replayed with:

```sh
c++ -O2 -std=c++20 -Wall -Wextra -Werror \
  -fsanitize=undefined,signed-integer-overflow \
  cpp/enumerate.cpp -o /tmp/n26-enumerate-ubsan
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
  /tmp/n26-enumerate-ubsan
```

It reproduced the artifact without a sanitizer report. Lock checking, Ruff,
format checking, strict mypy, all tests, and the normal full replay also
passed.
