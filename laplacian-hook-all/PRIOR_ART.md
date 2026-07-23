# Prior-art audit

Li and Wang, *Almost complete graphs determined by Laplacian hook immanantal
polynomials*, arXiv:2607.19411v1, claim the theorem for \(n>7\) and
\(n\ne2k-1\), and pose \(n=2k-1\) as an open problem.

Their Lemma 2.1, in the displayed third- and fourth-coefficient formulas on
pp. 3--4, substitutes

\[
\binom{n-4}{k-4}-\binom{n-4}{k-1}
\]

for the character of a three-cycle. The correct sign is plus. Their Lemmas
3.2--3.4 repeatedly use this term, so the written proof of their
nonexceptional theorem requires re-audit; the sign error alone does not
disprove the claimed result.

Dong and Wu, arXiv:2604.04489v1, give the correct general single-cycle
character in Lemma 2.12 and Claim 4.1, but their Theorem 4.3 and Corollary
6.1 contain the same inconsistent minus sign in coefficient displays.

The theorem here starts again from the exterior-power character identity.
It proves the claimed nonexceptional cases with the corrected coefficients
and also proves the formerly excluded self-conjugate cases.

Sources:

- <https://arxiv.org/abs/2607.19411v1>
- <https://arxiv.org/abs/2604.04489v1>
