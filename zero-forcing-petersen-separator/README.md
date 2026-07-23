# Balanced separators in \(P(n,3)\)

This package proves the all-order theorem

\[
\left|\,\{x\in X:N(x)\not\subseteq X\}\,\right|\ge8
\]

for every \(n\ge17\) and every \(n\)-vertex subset \(X\subseteq V(P(n,3))\).
The threshold is exact: a displayed 16-vertex subset of \(P(16,3)\) has boundary seven.

The proof has two parts:

1. a 247-state exact transfer computation excludes boundary at most seven for
   \(17\le n\le98\);
2. a clean-run deletion lemma reduces every hypothetical counterexample at \(n\ge99\) to one
   at \(n-2\).

Consequently every vertex layout of \(P(n,3)\) has a prefix boundary of at least eight, so

\[
\operatorname{pw}(P(n,3))\ge8
\quad\text{and}\quad
Z(P(n,3))\ge8
\qquad(n\ge17).
\]

The implication \(\operatorname{pw}(G)\le Z(G)\) is proved directly from a forcing order in
[PATHWIDTH.md](PATHWIDTH.md).

```sh
uv run zero-forcing-petersen-separator-check
```
