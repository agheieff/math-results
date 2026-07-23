# Prior-art audit

## Current frontier

Huang's arXiv:2607.20051v1 defines

\[
s_r(F)=\sum_{i=1}^r\lambda_i(F),\qquad
D_r(F)=\sum_{v\in V}\min\{d_F(v),r\},
\]

and records the following state:

- \(s_1(F)\leq D_1(F)\) was already known in every uniformity;
- Huang proves \(s_2(F)\leq D_2(F)\) in every uniformity and classifies equality;
- for every \(r\ge5\), a counterexample exists in some uniformity;
- every uniformity \(q\ge3\) has a counterexample at some index \(r\ge5\);
- the only unresolved universal indices are exactly \(r=3\) and \(r=4\).

The quantifiers matter: the paper does not claim a counterexample for every pair
\((q,r)\) with \(q\ge3\) and \(r\ge5\). In particular, it neither proves nor refutes the
\(r=3,4\) inequalities for unrestricted 3-uniform families.

## Earlier results named by Huang

Duval and Reiner formulated the higher-dimensional majorization assertion and proved the
first partial-sum inequality. The graph case \(q=2\) is covered by the graph
Grone--Merris theorem. Lew proved all indices for \(q\)-partite \(q\)-families. Han, Lu, and
Wang proved \(r=2\) for 3-uniform families shortly before Huang's universal \(r=2\) theorem.

Primary references:

- Jing Huang, “The Duval--Reiner Conjecture: Counterexamples and the Second Partial-Sum
  Inequality,” [arXiv:2607.20051v1](https://arxiv.org/abs/2607.20051v1), 22 July 2026.
- Art M. Duval and Victor Reiner, “Shifted simplicial complexes are Laplacian integral,”
  *Transactions of the AMS* 354 (2002), 4313--4344,
  [AMS article](https://www.ams.org/journals/tran/2002-354-11/S0002-9947-02-03082-9/).
- Y. Han, L. Lu, and J. Wang, “On the sum of the two largest eigenvalues of the curl-curl
  operator on graphs,” [arXiv:2606.26512v1](https://arxiv.org/abs/2606.26512v1).
- Alan Lew, “Sums of Laplacian eigenvalues and sums of degrees,”
  [arXiv:2508.04209v1](https://arxiv.org/abs/2508.04209v1).

## Seven-vertex search wording

Huang reports that its two counterexample seeds were found by an exhaustive computer search
on seven vertices. The paper supplies exact certificates for those seeds but no exhaustive
\(r=3,4\) nonexistence statement or census certificate. The six-vertex gate here is therefore
reported as an independently reproducible bounded computation, not as a novelty claim and not
as evidence for a seven-vertex theorem.
