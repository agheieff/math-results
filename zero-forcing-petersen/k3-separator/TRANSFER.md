# Exact transfer certificate

## Automaton

Use colors \(A,B,Y\) from the separator reduction. A pair of colors is compatible unless it is
\(A,Y\) in either order. The spoke-compatible column alphabet is

\[
\mathcal C=\{AA,AB,BA,BB,BY,YB,YY\}.
\]

A state is a triple \((c_0,c_1,c_2)\in\mathcal C^3\) whose consecutive outer coordinates are
compatible. There are exactly 247 states. Appending \(c_3\) is allowed when

- the outer coordinates of \(c_2,c_3\) are compatible; and
- the inner coordinates of \(c_0,c_3\) are compatible.

The second condition is precisely the edge \(v_iv_{i+3}\). There are 1,233 transitions.
A closed walk of length \(n\) is therefore exactly a valid cyclic coloring of \(P(n,3)\).

Give an appended column the weights

\[
\beta(c)=\#B\text{ in }c,\qquad
\delta(c)=\#Y\text{ in }c-1.
\]

The coloring is balanced exactly when its closed walk has
\(\sum\delta=|Y|-n=0\), and its proposed separator size is \(\sum\beta\).

## Boolean recurrence

For states \(p,q\), let \(R_t(p,q,b,d)\) say that a length-\(t\) path from \(p\) to \(q\) has
separator weight \(b\) and balance \(d\). Initialize

\[
R_0(p,q,b,d)=[p=q,\ b=0,\ d=0]
\]

and apply every transition with its \((\beta,\delta)\) weights. An order \(n\) is rejected
exactly when

\[
R_n(q,q,b,0)=0
\quad\text{for every state }q\text{ and }0\le b\le7.
\]

The implementation stores all starting states and balance values as exact integer bitsets.
It checks all lengths through 98 in one recurrence. No numerical, randomized, or pruning step
is used.

The result is:

- minimum \(b=5\) for \(n=7,8,9\);
- minimum \(b=6\) for \(n=10,11,12\);
- minimum \(b=7\) for \(n=13,14,15,16\);
- no \(b\le7\) for every \(17\le n\le98\).

Frozen identifiers:

```text
states: 247
transitions: 1233
automaton SHA-256:
c0d865280febdcad27e27b87e57517654d5a863b6235a1ff0baf23dbf1e1bb8a
accepting-state transcript SHA-256:
a297c0de728646d4968ccc9773a26d45b5a76413368928a62083855f4d0021be
```

The transcript hashes the complete set of accepting diagonal states for every
\((n,b)\in\{1,\ldots,98\}\times\{0,\ldots,7\}\), not merely the final theorem.
