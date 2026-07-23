# Source and prior-art audit

Audit date: 2026-07-23.

## Primary problem source

José A. R. Fonollosa, *Minimum modulus for the unique multiset-sum problem*,
[arXiv:2607.08366v2](https://arxiv.org/abs/2607.08366v2), revised
2026-07-14.

- Lines 187--195 of the TeX define validity using
  \(k\in\mathbb Z_{\ge0}^n\), \(\sum k_i=n\), and a congruence modulo \(N\).
- Conjecture 1 asks whether every valid cyclic set satisfies
  \(N\ge2^n-2^{\lfloor\log_2n\rfloor}\).
- Open Problem 4 asks whether \(2^{n-1}\) is the least order over all finite
  abelian groups. The paper proves this only within elementary abelian
  \(2\)-groups and reports exhaustive confirmation through \(n=6\).
- Its statement that even a general exponential cyclic lower bound appears
  open was written before the later companion-paper revision below.

## Companion source and existing general lower bound

José A. R. Fonollosa, *Ryser, Glynn, and the discrete Fourier transform:
orthogonal schemes for the permanent*,
[arXiv:2607.09949v2](https://arxiv.org/abs/2607.09949v2), revised
2026-07-16.

Version 2 explicitly added Corollary 1. It proves that every finite abelian
group with a size-\(n\) unique-multiset-sum embedding satisfies

\[
|G|\ge\binom{2n}{n}/2^n
\sim 2^n/\sqrt{\pi n}.
\]

The proof uses the dimension of all partial derivatives of the permanent.
The same paper gives the order-\(2^{n-1}\) construction in
\((\mathbb Z_2)^{n-1}\) and leaves exact optimality over all finite abelian
groups open.

The present dissociation argument raises the lower bound to \(2^{n-1}\).
Relative to Corollary 1's displayed real-valued right side, the exact
improvement factor is

\[
2^{2n-1}/\binom{2n}{n}\sim\sqrt{\pi n}/2.
\]

## Classical Waring-rank implication

Enrico Carlini, Maria Virginia Catalisano, and Anthony V. Geramita,
*The Solution to Waring's Problem for Monomials*,
[arXiv:1110.0745](https://arxiv.org/abs/1110.0745), prove that for
\(0<d_0\le\cdots\le d_m\), over an algebraically closed field of
characteristic zero,

\[
\operatorname{rk}_{\mathbb C}
(x_0^{d_0}\cdots x_m^{d_m})
=\frac{\prod_i(d_i+1)}{d_0+1}.
\]

In particular,
\(\operatorname{rk}_{\mathbb C}(x_0\cdots x_{n-1})=2^{n-1}\).
This already implies the sharp lower bound for the companion paper's
evaluation schemes. Indeed, setting all matrix rows equal to \(x\) turns an
\(|R|\)-term scheme into an \(|R|\)-term Waring decomposition

\[
n!x_0\cdots x_{n-1}
=c\sum_{r\in R}w_rL_r(x)^n.
\]

Over \(\mathbb C\), \(n!\ne0\), and each nonzero scalar coefficient has an
\(n\)-th root that can be absorbed into its linear form; zero terms can be
deleted. Thus the Waring decomposition has at most \(|R|\) summands and
\(|R|\ge2^{n-1}\). Character schemes have \(|R|=|G|\), so the same
group-order bound follows. The present proof is therefore not the first
latent route to the numerical lower bound; its contribution is the direct
and elementary basepoint-dissociation reduction for the newly posed group
condition.

## Classical ingredient

A finite set in an abelian group is called **dissociated** (or
subset-sum-distinct) when all of its subset sums are different; equivalently,
it has no nonzero relation with coefficients in \(\{-1,0,1\}\). The elementary
count \(|G|\ge2^{|D|}\) for a dissociated \(D\subseteq G\) is immediate by
pigeonhole.

The new step here is the reduction from the paper's single-target,
fixed-cardinality multiset condition to dissociation of every
\((n-1)\)-element basepoint-difference set. No deep result about dissociated
sets, Sidon sets, or \(B_h\)-sets is used. Sidon and \(B_h\) conditions concern
fixed-order sums and are not the exact intermediary.

## Status searches

Searches on 2026-07-23 covered:

- the exact titles and arXiv identifiers of both papers;
- exact phrases from the two open questions;
- combinations of “unique multiset sums”, “dissociated”, “subset sums”, and
  “finite abelian group”;
- the equal-row/Waring-rank reduction and the exact monomial-rank theorem;
- the current arXiv version histories; and
- the public `jarfo/min-modulus` repository at commit
  `b2b91e6f9517275a956daa57405e0071ca68d2d8`.

No later arXiv version, cited resolution, or occurrence of the basepoint
dissociation reduction was found. Because the problem and terminology are
new, this is a novelty audit rather than a proof of bibliographic priority.
