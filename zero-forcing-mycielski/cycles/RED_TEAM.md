# Independent proof audit

Audit date: 2026-07-23.

Verdict: **PASS** for the stated family \(M(C_q)\), every integer \(q\ge4\).

## Uniform upper bound

The five initial vertices and every displayed force were reconstructed from
the edge definition, independently of the package implementation. The
sequence was replayed for every \(4\le q\le64\). It performs \(2q-4\) valid
forces after the five initial vertices and ends with all \(2q+1\) vertices
black. The empty final range at \(q=4\) and the one-index range at \(q=5\)
are both correct.

## Generic matrix certificate

For \(q=5\) or \(q\ge7\), the audit checked:

- \(b=r+s=4\cos(3\pi/q)\cos(\pi/q)\ne0\). At \(q=5\), \(b=-1\);
  for \(q\ge7\), both cosine factors are positive. Thus every original
  cycle edge has a nonzero matrix entry.
- \(A_0-4=-(2-r)(2-s)\ne0\), so the apex diagonal \(f\) is defined.
- The cycle eigenspaces for \(r=\lambda_1\) and \(s=\lambda_2\) are
  distinct and each has real dimension two. This remains true for even
  \(q\ge8\); the \(q=4\) multiplicity exception is handled separately.
- On a nonconstant \(\lambda\)-eigenspace,
  \[
  \det\begin{pmatrix}a+b\lambda&\lambda\\\lambda&1\end{pmatrix}
  =-(\lambda-r)(\lambda-s),
  \]
  giving four kernel dimensions in total.
- The normalized constant/apex block has determinant
  \(f(A_0-4)-qA_0=0\) and nonzero leading \(2\times2\) minor
  \(A_0-4\), giving exactly one further dimension.

These identities were rechecked symbolically. A separate exact algebraic
row reduction at the first even generic case \(q=8\) gave rank \(12\) and
nullity \(5\). Numerical spectra for \(q=5\), every \(7\le q\le30\), and
\(q=64,101\) supplied a non-proof regression check and always had exactly
five zero eigenvalues.

## Exceptional case \(q=4\)

The matrix

\[
Y=\begin{pmatrix}
C_4&C_4&0\\
C_4&0&\mathbf1\\
0&\mathbf1^{\mathsf T}&-2
\end{pmatrix}
\]

was rebuilt independently. Its off-diagonal support is exactly
\(M(C_4)\), and exact Gaussian elimination over \(\mathbb Q\) gives rank
\(4\), hence nullity \(5\). The written spectral explanation agrees:
the two-dimensional \(0\)-eigenspace of \(C_4\) contributes four kernel
dimensions, the \(-2\) block is nonsingular, and the constant/apex block
has nullity one.

## Exceptional case \(q=6\)

The 16 listed sets were regenerated directly from their formulas. For
vertices outside a set, the possible neighbor counts are respectively

\[
\{0,2,3\},\quad\{2\},\quad\{0,2,3\},\quad\{2,3\}
\]

for the parity, \(A_i\), \(B_i\), and \(D_i\) families, so every listed set
is a fort.

The four parity forts are pairwise disjoint. An independent enumeration of
their \(3^4=81\) four-vertex transversals found that hitting all \(A_i\) and
\(B_i\) leaves exactly

\[
\{v_i,v_{i+3},u_{i+1},u_{i+2}\}\qquad(i\in\mathbb Z/6\mathbb Z).
\]

Each misses \(D_{i\bmod3}\), so no four-set hits every fort and therefore
no four-set is zero forcing. A separate raw closure sweep over all
\(\binom{13}{4}=715\) sets found maximum closure size \(6\), corroborating
the fort proof.

## Consequences and replay

The coloring consequences are correctly scoped: odd \(q\) gives
\((\chi,\omega,Z)=(4,2,5)\), equality in the Annor--Howerton conjecture,
and the all-shadow witness for Condition \((R)\); even \(q\) gives
\((3,2,5)\), while Condition \((R)\) is outside its hypothesis.

The final package passed Ruff, format checking, strict mypy, 20 tests, both
exact matrix checks, the fort replay, and exhaustive four-set regressions
for every \(4\le q\le13\). This audit establishes correctness, not
literature priority.
