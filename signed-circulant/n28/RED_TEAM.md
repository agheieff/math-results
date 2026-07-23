# Independent audit

Audit date: 2026-07-23.

An independent script reconstructed each twisted matrix directly from
\(\tau_i=\tau_0(-1)^i\) and negative Hamilton holonomy, without importing the
package model. The resulting matrix SHA-256 hashes are:

| mask | matrix SHA-256 |
| ---: | --- |
| 223696213 | `c820320762aaf8a89deec7e5b2fb3f1029aa47ead503e96eafd8111d5e208f26` |
| 313174699 | `0cf940d6f3ff4defe747db9ac5e942c7267773557fe52ce1863f3cadc4d6684e` |

For each matrix, fraction-free Bareiss determinants evaluated
\(\det(jI-A)\) at every integer \(0\le j\le28\). Exact forward-difference
interpolation independently returned the saved characteristic polynomial and
the factorization

\[
(x^2-2)^2
\left(x^{12}-26x^{10}+270x^8-1434x^6+
4111x^4-6030x^2+3529\right)^2.
\]

The full enumerator was separately compiled and replayed with:

```sh
c++ -O2 -std=c++20 -Wall -Wextra -Werror \
  -fsanitize=undefined,signed-integer-overflow \
  cpp/enumerate.cpp -o /tmp/n28-enumerate-ubsan
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
  /tmp/n28-enumerate-ubsan
```

A \(2^{25}\)-class prefix benchmark took \(7.15\) seconds, projecting
\(114.4\) seconds for the full space. The optimized full run took \(122.5\)
seconds, and the sanitizer run took \(274.3\) seconds.

It reproduced the artifact without a sanitizer report. Lock checking, Ruff,
format checking, strict mypy, all tests, and the normal full replay also
passed.
