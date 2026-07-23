# All-orders theorem

Let \(P(n,3)\) have vertices \(u_i,v_i\), with indices modulo \(n\), and edges

\[
u_i u_{i+1},\qquad u_i v_i,\qquad v_i v_{i+3}.
\]

## Theorem

For every integer \(n\ge13\),

\[
\boxed{Z(P(n,3))=8.}
\]

## 1. Zero forcing dominates pathwidth

Fix a zero-forcing set \(S\) and a sequential list of its forces. Order the vertices by first
listing \(S\), then listing the forced targets in force order. For a prefix \(X\), write

\[
\partial X=\{x\in X:N(x)\not\subseteq X\}.
\]

The forces split the vertices into \(|S|\) forcing chains. After all of \(S\) has been listed,
at most the last listed vertex of each chain can lie in \(\partial X\): when an earlier chain
vertex forced its successor, every other neighbor was already black and hence earlier in the
order. Prefixes inside the initial block have boundary at most \(|S|\) trivially. Thus the
ordering has vertex separation at most \(|S|\). Since vertex separation equals pathwidth,

\[
\operatorname{pw}(G)\le Z(G).
\]

## 2. Three exact pathwidth bases

For an ordering \(v_1,\ldots,v_N\), its width is

\[
\max_j |\partial\{v_1,\ldots,v_j\}|.
\]

For \(k=7\), define \(\mathcal R_0=\{\varnothing\}\) and

\[
\mathcal R_j=\left\{X:\begin{array}{l}
|X|=j,\ |\partial X|\le7,\ \text{and}\\
X\setminus\{x\}\in\mathcal R_{j-1}\text{ for some }x\in X
\end{array}\right\}.
\]

This recurrence is exact: \(\mathcal R_j\) is precisely the collection of possible
\(j\)-vertex prefixes of width-seven orderings. The verifier enumerates these bitsets without
symmetry reduction. It reaches the empty layer before the full vertex set for each of
\(P(14,3),P(15,3),P(16,3)\). Hence each has pathwidth at least eight.

## 3. Transfer to every \(n\ge14\)

In \(P(n,3)\), delete the spokes in columns \(n-3,n-2,n-1\). Suppress the three exposed outer
vertices and the three exposed inner vertices. The outer cycle loses three vertices, while
the three inner step-three strands each lose one vertex, leaving exactly \(P(n-3,3)\).
Therefore

\[
P(n-3,3)\preccurlyeq P(n,3)\qquad(n\ge10).
\]

Pathwidth is minor-monotone. Repeated reduction takes every \(n\ge14\) to the unique
\(b\in\{14,15,16\}\) congruent to \(n\) modulo three, so

\[
8\le\operatorname{pw}(P(b,3))
\le\operatorname{pw}(P(n,3))
\le Z(P(n,3)).
\]

For \(n=13\), the verifier tests all \(\binom{26}{7}=657800\) seven-sets and finds none that
forces the graph. Monotonicity under enlarging the initial black set excludes all smaller
sets as well.

## 4. Uniform upper bound

Start with \(u_0,\ldots,u_7\). First force

\[
u_i\to v_i\quad(1\le i\le6),
\]

then

\[
v_1\to v_{n-2},\quad v_2\to v_{n-1},\quad v_3\to v_0,\quad
v_4\to v_7,\quad v_5\to v_8,\quad v_6\to v_9,
\]

and then

\[
u_0\to u_{n-1},\quad u_7\to u_8,\quad
v_0\to v_{n-3},\quad v_7\to v_{10}.
\]

If two displayed targets coincide, as they do at \(n=13\), use either force.
At this point the black outer indices include
\([0,8]\cup[n-1,n-1]\), and the black inner indices include
\([0,10]\cup[n-3,n-1]\). Repeatedly use the four wave forces

\[
\begin{aligned}
u_{8+t}&\to u_{9+t},&
u_{n-1-t}&\to u_{n-2-t},\\
v_{8+t}&\to v_{11+t},&
v_{n-1-t}&\to v_{n-4-t},
\end{aligned}
\]

skipping a force if its target is already black; this also handles the coincident inner
targets in the final wave at odd orders. Each displayed new target is the unique white
neighbor of its source when it is needed. After
\(\lceil(n-14)/2\rceil\) waves the two black inner intervals meet, so every \(v_i\) is black.
The remaining white outer vertices form one path of length at most four, whose two black
end-neighbors force inward. Thus the initial eight-set forces every \(P(n,3)\) with \(n\ge13\).

Combining the lower and upper bounds proves the theorem.
