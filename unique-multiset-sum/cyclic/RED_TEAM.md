# Independent red-team audit

Audit date: 2026-07-23.

Verdict: **PASS**.

The audit independently checked both cases of the doubled-subset witness
\(2d_i=\sum_{j\in S}d_j\), the doubling-fiber argument, parity rounding for
every \(n\ge2\), and equality rigidity at group order \(2^{n-1}\).

For even \(N\), two distinct doubling-collision pairs would give equal sums
for two distinct two-element subsets. An order-two difference and a
doubling-collision pair would similarly give equal sums for a singleton and
a two-element subset. Therefore the set of \(m=n-1\) differences has at least
\(m-1\) distinct nonzero doubles, confirming

\[
N\ge2^{n-1}+2\left\lfloor\frac{n-1}{2}\right\rfloor.
\]

Independent exhaustive checks covered:

- 55,430 difference sets in cyclic groups through order 24, including all
  13,296 subset-sum-injective cases;
- 104,560 doubled-subset collision witnesses, split across both
  \(i\in S\) and \(i\notin S\); and
- finite abelian groups through order 16 for the equality-rigidity claim.

The shipped tests, Ruff lint and formatting, strict mypy, and command-line
audit all passed. This audit establishes correctness, not literature priority.
