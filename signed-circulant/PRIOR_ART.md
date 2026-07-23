# Prior-art audit

Audit date: 2026-07-23.

## Primary source

- Vaibhav Suvagiya, *Signed circulants at the Ramanujan bound*,
  [arXiv:2607.18334v1](https://arxiv.org/abs/2607.18334), submitted
  2026-07-19.

Conjecture 3 gives the all-even-\(n\) statement. Its reported exhaustive range
is exactly

\[
n\in\{8,10,12,14,16,18\},
\]

with agreement to \(10^{-9}\). It does not report \(n=20\).

## Companion and source bundle

- Vaibhav Suvagiya, *Parity families and a kernel-averaged \(L\)-function for
  near-Ramanujan signings*,
  [arXiv:2607.17343v1](https://arxiv.org/abs/2607.17343), submitted
  2026-07-19.
- The author's linked
  [verification repository](https://github.com/Vaibhavs25/bilu-linial-parity)
  was inspected. Its switching-class code uses floating-point
  `eigvalsh`; its current paper and README retain the same \(n\le18\) range.

The arXiv record still had only v1 on 2026-07-23. Searches for the exact title,
the graph \(C_n(1,2)\), and signed-circulant spectral minima found no later
arXiv resolution of the \(n=20\) gate.

This is a current-source audit, not a guarantee of literature-wide novelty.
The result here is an exact extension of the source's reported finite range,
not a proof of its all-even-\(n\) conjecture.
