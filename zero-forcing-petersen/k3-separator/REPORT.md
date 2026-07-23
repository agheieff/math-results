# Boundary-eight theorem

## Statement

Write

\[
P(n,3)=\bigl(\{u_i,v_i:i\in\mathbb Z/n\mathbb Z\},
\{u_iu_{i+1},u_iv_i,v_iv_{i+3}\}\bigr).
\]

For \(X\subseteq V(P(n,3))\), let

\[
\partial_X X=\{x\in X:N(x)\cap(V\setminus X)\ne\varnothing\}.
\]

The certificate proves

\[
|X|=n,\ n\ge17\quad\Longrightarrow\quad |\partial_X X|\ge8.
\]

It also verifies the exact minimum boundary for \(7\le n\le16\):

| \(n\) | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Minimum | 5 | 5 | 5 | 6 | 6 | 6 | 7 | 7 | 7 | 7 |

Thus 17 is the exact eventual threshold.

## Separator-coloring equivalence

Suppose \(|X|=n\), put \(B=\partial_X X\), \(A=X\setminus B\), and
\(Y=V\setminus X\). No edge joins \(A\) to \(Y\), and

\[
|B|=b,\qquad |A|=n-b,\qquad |Y|=n.
\]

Conversely, any coloring \(V=A\sqcup B\sqcup Y\) with these cardinalities and no \(A\)-\(Y\)
edge gives the half-set \(X=A\cup B\), whose boundary is contained in \(B\). Therefore a
boundary-seven counterexample exists exactly when such a coloring exists with \(b\le7\).

At index \(i\), record the colors of \((u_i,v_i)\). A column without \(B\) must be \(AA\) or
\(YY\), since \(u_iv_i\) is an edge. The seven allowed column types are

\[
AA,\ AB,\ BA,\ BB,\ BY,\ YB,\ YY.
\]

The transfer certificate in [TRANSFER.md](TRANSFER.md) excludes every balanced cyclic coloring
with \(b\le7\) for \(17\le n\le98\).

## Reduction above 98

Call a column dirty if it contains \(B\), and let \(d\) be the number of dirty columns. Then
\(d\le b\le7\). Every clean column is \(AA\) or \(YY\). Consecutive clean columns have the same
color because their outer vertices are adjacent. Balance rules out \(d=0\), since the entire
outer cycle would then force all columns to have one color. Thus \(d\ge1\), and the clean
columns form at most \(d\) runs.

Let \(r_A,r_Y\) be the numbers of clean \(AA,YY\) columns, and let \(a_D,y_D\) count \(A,Y\)
vertices in dirty columns. Each dirty column contains at most one \(A\) and at most one \(Y\),
so \(a_D,y_D\le d\). The cardinality equations give

\[
r_A=\frac{n-b-a_D}{2}\ge\frac{n-14}{2},\qquad
r_Y=\frac{n-y_D}{2}\ge\frac{n-7}{2}.
\]

For \(n\ge99\), both \(r_A\) and \(r_Y\) exceed 42. Since each color occupies at most seven
runs, there is both an \(AA\)-run and a \(YY\)-run of length at least seven.

Delete the fourth column of such a seven-column monochromatic run. The new outer edge joins
equal colors. The only new inner step-three edges join the old position pairs

\[
(i-3,i+1),\quad(i-2,i+2),\quad(i-1,i+3),
\]

whose endpoints lie in the same clean run. Hence deletion creates no \(A\)-\(Y\) edge.
Delete one \(AA\) column and one \(YY\) column. This leaves \(b\) unchanged and changes

\[
(|A|,|B|,|Y|)=(n-b,b,n)
\quad\text{to}\quad
(n-2-b,b,n-2).
\]

Thus a counterexample at \(n\ge99\) produces one at \(n-2\). Repetition reaches 97 or 98,
contradicting the finite transfer check.

## Sharpness

In \(P(16,3)\), take

\[
\begin{aligned}
X=\{&u_2,u_3,u_4,u_5,u_6,u_7,u_8,\\
    &v_0,v_1,v_3,v_4,v_5,v_6,v_7,v_9,v_{10}\}.
\end{aligned}
\]

Its internal boundary is

\[
\{u_2,u_8,v_0,v_1,v_5,v_9,v_{10}\},
\]

of size seven.

## Pathwidth and zero forcing

For any ordering of the \(2n\) vertices, its first \(n\) vertices form a half-set. The theorem
therefore makes every layout's maximum prefix boundary at least eight. The vertex-separation
characterization of pathwidth, proved in [PATHWIDTH.md](PATHWIDTH.md), gives
\(\operatorname{pw}(P(n,3))\ge8\). The same file proves directly that
\(\operatorname{pw}(G)\le Z(G)\), hence

\[
Z(P(n,3))\ge8\qquad(n\ge17).
\]
