# Independent counterexample audit

Audit date: 2026-07-23.

Verdict: the \(3\times3\) rook graph exactly refutes the frozen local
matching-completion lemma; it does not address the parent colouring target.

The graph was regenerated independently from row/column adjacency. It has 18
edges, degree sequence \(4^9\), no \(K_4\), no independent four-set, and
exactly six independent triples. For each triple, deleting it leaves \(C_6\);
the missing-edge matchings have counts \(1,9,18,4\) by sizes \(0,1,2,3\), so
there are 32 completions per triple and 192 in total.

An independent exact minor checker enumerated forests with at most three
edges, contracted each forest, and searched the quotient for a literal
\(K_6\). This is complete because six nonempty branch sets in a nine-vertex
graph use at most three contraction edges. It found no \(K_6\) minor in the
raw rook graph or in any of the 192 completions, and it passed positive,
negative, and three-subdivision controls.

The Rolek--Song linkage hypotheses were also checked: for a matching of size
\(m\le3\), choosing \(r_i=1\) gives
\(\sum r_i+m=2m\le6=k-2\) at \(k=8\), and distinct matching endpoints give
the required disjoint paths. Including the empty matching is harmless.

`uv lock --check`, three tests, Ruff lint and formatting, strict mypy, and the
CLI verifier all pass.
