# Exact finite theorem

Write

\[
P(n,4)=\bigl(\{u_i,v_i:i\in\mathbb Z/n\mathbb Z\},
\{u_iu_{i+1},u_iv_i,v_iv_{i+4}\}\bigr).
\]

The certificate proves

\[
\boxed{Z(P(n,4))=10\quad\text{for }18\le n\le22.}
\]

## Uniform upper bound

For every \(n\ge9\), start with

\[
S=\{u_0,u_1,\ldots,u_7,v_0,v_7\}.
\]

First use \(u_i\to v_i\) for \(1\le i\le6\). The vertices \(v_0,\ldots,v_7\) are then black.
For \(j=n-1,n-2,\ldots,8\), in that order, apply

\[
u_{j+1}\to u_j,\qquad v_{j+4}\to v_j,
\]

with indices modulo \(n\). For the outer force, the other outer neighbor and the spoke
neighbor are already black. For the inner force, \(u_{j+4}\) is black and the other inner
neighbor \(v_{j+8}\) is either in the initial inner interval or was forced at an earlier,
larger value of \(j\). Hence every displayed force is legal and \(Z(P(n,4))\le10\).

## Exact lower census

Encode a subset by a word of \(n\) columns over

\[
0,\ U,\ V,\ UV
\]

with weights \(0,1,1,2\). Rotation of the word is an automorphism of \(P(n,4)\), so it is
enough to inspect one necklace in every cyclic orbit. The Fredricksen--Kessler--Maiorana
recursion in `native_census.cpp` generates each fixed-weight necklace exactly once.

For each weight-nine representative, the checker computes the full deterministic
zero-forcing closure. The result is:

| \(n\) | cyclic orbits | forcing orbits |
|---:|---:|---:|
| 17 | 3,085,368 | 48,100 |
| 18 | 5,230,208 | 0 |
| 19 | 8,579,560 | 0 |
| 20 | 13,671,944 | 0 |
| 21 | 21,232,978 | 0 |
| 22 | 32,224,114 | 0 |

The first \(n=17\) control witness is

\[
\{u_{15},u_{16},v_{10},v_{11},v_{12},v_{13},v_{14},v_{15},v_{16}\}.
\]

If a zero-forcing set had size below nine, any extension to nine vertices would also force.
Thus exhaustion of all 9-subsets excludes every forcing set of size at most nine. Together
with the uniform upper bound, this proves the theorem.

Each transcript SHA-256 hashes, in deterministic necklace order, the initial mask and its full
closure. The tests also verify every orbit total by Burnside's lemma.
