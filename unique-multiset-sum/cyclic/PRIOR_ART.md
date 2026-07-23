# Prior-art boundary

Audit date: 2026-07-23.

The primary problem source is José A. R. Fonollosa,
*Minimum modulus for the unique multiset-sum problem*,
[arXiv:2607.08366v2](https://arxiv.org/abs/2607.08366v2). It conjectures the
stronger cyclic bound

\[
N\ge2^n-2^{\lfloor\log_2n\rfloor}.
\]

The companion paper
[arXiv:2607.09949v2](https://arxiv.org/abs/2607.09949v2) proves
\(\lvert G\rvert\ge\binom{2n}{n}/2^n\) for every finite abelian group and
records the order-\(2^{n-1}\) elementary-abelian construction. The classical
Carlini--Catalisano--Geramita Waring-rank theorem already implies the sharper
general lower bound \(2^{n-1}\) after equal-row restriction.

The present lane starts from the independently verified basepoint-dissociation
reduction in `../unique-multiset-sum/`. Its new candidate contribution is the
hole lemma for nonzero doubled differences, the restriction to at most one
doubling collision or one order-two difference, the resulting additive cyclic
gap, and equality rigidity. These claims require a fresh exact-phrase and
equivalent-language audit before any public priority claim. They do not settle
the cyclic conjecture.

## Search log

On 2026-07-23, web/arXiv searches used:

- `"unique multiset sums" doubled differences cyclic`;
- `"basepoint differences" dissociated finite abelian group multiset`;
- `"unique multiset-sum" "2^{n-1}" cyclic`; and
- `"unique multiset-sum" doubling collision order two`; and
- the source identifier `2607.08366` combined with `resolution` and
  `cyclic lower bound`.

The searches returned the two primary papers, unrelated notions of unique
sums, and general subset-sum literature, but no occurrence of the doubled-hole
lemma or the displayed additive cyclic bound. The source problem is only two
weeks old, so this is a limited novelty audit rather than proof of priority.
