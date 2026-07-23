# Independent audit

Audit date: 2026-07-23.

An independent script reconstructed each twisted matrix directly from
\(\tau_i=\tau_0(-1)^i\) and negative Hamilton holonomy, without importing the
package model. The results were:

| mask | matrix SHA-256 |
| ---: | --- |
| 13981013 | `56a054fe81c709dea5e430f516082c4af46e543d92b1e9f3d49fd540e74c741f` |
| 19573419 | `5bf2ceb7c22fcf823611675b86a63a8f318d85e2056789475700fb480f27ae58` |

For each matrix, fraction-free Bareiss determinants evaluated
\(\det(jI-A)\) at every integer \(0\le j\le24\). Exact forward-difference
interpolation returned the saved degree-24 characteristic polynomial and its
factorization

\[
(x^4-8x^2+14)^2
(x^8-16x^6+86x^4-188x^2+142)^2.
\]

The full enumerator was also compiled and replayed with:

```sh
c++ -O2 -std=c++20 -Wall -Wextra -Werror \
  -fsanitize=undefined,signed-integer-overflow \
  cpp/enumerate.cpp -o /tmp/n24-enumerate-ubsan
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
  /tmp/n24-enumerate-ubsan
```

It completed all \(2^{25}\) masks without a sanitizer report and reproduced
the artifact histograms and survivor masks exactly. Lock checking, Ruff,
format checking, strict mypy, all five tests, and the normal full replay also
passed.
