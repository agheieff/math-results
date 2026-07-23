# From half-set boundaries to zero forcing

For a vertex order \(v_1,\ldots,v_N\), put

\[
L_i=\{v_1,\ldots,v_i\},\qquad
D_i=\{x\in L_i:N(x)\setminus L_i\ne\varnothing\}.
\]

Its vertex separation is \(\max_i|D_i|\).

## Vertex separation equals pathwidth

If an order has vertex separation \(k\), the bags

\[
D_{i-1}\cup\{v_i\}\qquad(1\le i\le N)
\]

form a path decomposition: every edge \(v_jv_i\), \(j<i\), occurs in the \(i\)-th bag, and a
vertex remains in consecutive bags until its final later neighbor. Each bag has at most
\(k+1\) vertices, so pathwidth is at most \(k\).

Conversely, make a width-\(k\) path decomposition nice, with one vertex introduced or forgotten
at each step, and order vertices by introduction. For the prefix ending immediately before the
next introduction, every prefix vertex having a neighbor not yet introduced must still be in
the current bag. That bag has at most \(k\) vertices, because the next introduction keeps the
following bag at size at most \(k+1\). Hence the order has vertex separation at most \(k\).
Thus vertex separation equals pathwidth under the convention
\(\operatorname{width}=\max|\text{bag}|-1\).

## A forcing order has separation at most its initial size

Let a zero forcing process start with \(S\), \(|S|=k\). Order the vertices of \(S\) first, then
list forced targets chronologically.

Prefixes contained in \(S\) have boundary at most \(k\). Suppose the next listed vertex \(w\)
is forced by \(v\). Immediately before adding \(w\), it is the unique unlisted neighbor of
\(v\), so \(v\) belongs to the prefix boundary. After adding \(w\), \(v\) leaves that boundary.
No old prefix vertex can newly acquire an unlisted neighbor, and at most the new vertex \(w\)
can enter. The boundary size therefore never increases beyond \(k\).

This order has vertex separation at most \(k\), and consequently

\[
\operatorname{pw}(G)\le k.
\]

Minimizing over zero forcing sets proves the standard implication

\[
\boxed{\operatorname{pw}(G)\le Z(G)}.
\]
