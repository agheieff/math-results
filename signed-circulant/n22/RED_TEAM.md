# Independent reproduction

Audit date: 2026-07-23.

Verdict: **PASS** for the frozen \(n=22\) gate.

The target minimal polynomial and rational Sturm interval were independently
derived from \(u=2\cos(\pi/11)\). A separate exact C++ exhaustion reproduced
the split

\[
8{,}388{,}070+522+14+2=2^{23}
\]

and the two survivor masks \(3495253\) and \(4893355\). A full
undefined-behavior-sanitized replay reported no overflow.

For both independently reconstructed survivor matrices, Bareiss
determinants at 23 integer points followed by exact interpolation gave

\[
(x^2-4)
\left(x^{10}-20x^8+149x^6-519x^4+851x^2-529\right)^2.
\]

The locked dependency check, five tests, Ruff, format check, strict mypy, and
the full shipped replay also passed. This establishes only \(n=22\), not the
all-even conjecture or literature priority.
