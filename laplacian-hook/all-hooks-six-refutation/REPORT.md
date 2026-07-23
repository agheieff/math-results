# Refutation of the universal six-deletion extension

## Statement

The claim that every graph obtained from \(K_n\) by deleting at most six
edges is determined by every Laplacian hook immanantal polynomial is false.
It already fails at \(k=1\) for every \(n\ge8\).

For the hook \((1^n)\), the irreducible character is the sign character.
Consequently

\[
\Phi_1(L(G),x)=\operatorname{Imm}_{(1^n)}(xI-L(G))
=\det(xI-L(G)).
\]

Thus a Laplacian-cospectral pair is a \(k=1\) counterexample.

## Three exact sparse classes

The notation `vsehex` is the canonical upper-triangle adjacency code for a
connected component on \(s\) vertices; hyphens denote disjoint union.
Every graph below has exactly six edges. Isolated vertices are added to reach
order \(n\).

### Class A

\[
\{\texttt{v2e1-v2e1-v4e3c},\ \texttt{v3e6-v4e33}\}.
\]

These graphs are nonisomorphic and, for every \(n\ge8\), have characteristic
polynomial

\[
x^{n-5}(x-4)(x-3)(x-2)^2(x-1).
\]

### Class B

\[
\{\texttt{v3e6-v4e3c},\ \texttt{v3e7-v4e34},\
\texttt{v6e6443}\}.
\]

For every \(n\ge7\), all three nonisomorphic graphs have polynomial

\[
x^{n-5}(x-4)(x-3)^2(x-1)^2.
\]

The last member is \(C_6\); the other two are disconnected, which makes
nonisomorphism immediate for those comparisons. Canonical codes separate the
remaining pair.

### Class C

\[
\{\texttt{v2e1-v5e3c4},\ \texttt{v6e6885}\}.
\]

For every \(n\ge7\), the shared polynomial is

\[
x^{n-5}(x-2)(x^2-5x+3)(x^2-5x+5).
\]

The first graph is disconnected and the second connected.

## Persistence under complementation

For an \(n\)-vertex sparse graph \(H\),

\[
L(K_n-H)=nI-J-L(H).
\]

All nonzero Laplacian eigenvectors of \(H\) lie in \(\mathbf1^\perp\).
If the five nonzero eigenvalues are \(\mu_1,\ldots,\mu_5\), the complement
spectrum is

\[
\{0,n^{(n-6)},n-\mu_1,\ldots,n-\mu_5\}.
\]

Hence each sparse class gives a dense cospectral class. Their dense
characteristic polynomials are:

\[
\begin{aligned}
A:\;&x(x-n)^{n-6}(x-n+4)(x-n+3)(x-n+2)^2(x-n+1),\\
B:\;&x(x-n)^{n-6}(x-n+4)(x-n+3)^2(x-n+1)^2,\\
C:\;&x(x-n)^{n-6}(x-n+2)\\
&\quad\cdot((x-n)^2+5(x-n)+3)((x-n)^2+5(x-n)+5).
\end{aligned}
\]

Complementation preserves nonisomorphism. Class A exists for every \(n\ge8\),
so the proposed universal-in-\(k\) extension fails throughout the full
admissible range.

At reference order \(n=9\), the three dense coefficient tuples are frozen in
the JSON certificate. All arithmetic is exact.

## Scope

This refutes the assertion quantified over every individual hook parameter.
It does not assert that two witnesses agree for all hook parameters
simultaneously; another hook may separate them.
