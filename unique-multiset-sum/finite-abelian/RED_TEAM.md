# Independent red-team report

Review date: 2026-07-23.

## Verdict

No substantive mathematical or computational flaw was found.

The lane establishes a verified theorem:

\[
|G|\ge2^{n-1}
\]

for every finite abelian group carrying a size-\(n\) unique-multiset-sum
family, with equality attained in \((\mathbb Z_2)^{n-1}\). It therefore
resolves the all-finite-abelian-groups optimum posed in Open Problem 4 of
arXiv:2607.08366v2.

This verdict does not claim that the numerical lower bound itself is new.
The 2011 Carlini--Catalisano--Geramita Waring-rank theorem already implies it
after the equal-row reduction. The potentially new contribution is the
elementary basepoint-dissociation proof and its application to the new group
formulation. Public priority and specialist review remain open.

The cyclic conjecture

\[
N\ge2^n-2^{\lfloor\log_2n\rfloor}
\]

is not resolved.

## Proof audit

The review independently checked:

- the definitions against arXiv:2607.08366v2 and arXiv:2607.09949v2;
- orientation of the colliding subsets so that \(c_j=|V|-|U|\ge0\);
- cancellation of overlap \(U\cap V\);
- equality in an arbitrary abelian group, not merely equality of integers;
- \(c_i\ge-1\), hence nonnegativity of \(k=\mathbf1+c\);
- \(\sum_i k_i=n\);
- \(k\ne\mathbf1\) when \(U\ne V\);
- the immediate collision caused by repeated family elements;
- the injection of all \(2^{n-1}\) subset sums into \(G\); and
- validity of \((0,e_1,\ldots,e_{n-1})\) in
  \((\mathbb Z_2)^{n-1}\).

All checks passed.

## Prior-art audit

The review confirmed:

- companion Corollary 1 gives
  \(\binom{2n}{n}/2^n\sim2^n/\sqrt{\pi n}\);
- the ratio to the displayed real lower bound is exactly
  \(2^{2n-1}/\binom{2n}{n}\sim\sqrt{\pi n}/2\);
- integer consequences instead compare against
  \(\left\lceil\binom{2n}{n}/2^n\right\rceil\); and
- the equal-row reduction and the complex Waring-rank formula give the
  independent classical route recorded in `PRIOR_ART.md`.

## Computational audit

The reviewer ran:

- Ruff lint and formatting checks;
- strict mypy;
- all 18 tests;
- the default exhaustive CLI through \(n=5\);
- an independent finite-abelian-group classification check through order 100;
- a direct audit of 1,237 small families, including 440 valid families; and
- independent equality-construction checks through \(n=8\).

The direct multiplicity enumerator is independent of the subset-collision
witness. The primary cyclic-factor enumeration covers every finite abelian
group isomorphism type.

One documentation error was found and fixed: the companion paper's
noncyclic discussion is Remark 1, not Remark 4.

## Lean audit

A second independent reviewer checked `lean/UniqueMultisetSum.lean` against
the frozen definition and proof. The size-`n + 1` indexing, multiplicity
construction, subset-sum injection, and cardinal conversion all match the
stated size-\(N\) bound \(2^{N-1}\).

`lake build` and warning-as-error checks pass. `CheckAxioms.lean` reports only
`propext`, `Classical.choice`, and `Quot.sound`; there is no `sorry`, `admit`,
custom axiom, unsafe declaration, or `sorryAx`.

The formal theorem uses the canonical last basepoint. The corresponding
statement for every basepoint follows by reindexing and remains in the
conventional proof rather than as a separate Lean theorem.
