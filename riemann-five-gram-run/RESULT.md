# Turing-checked five-Gram run

Let

\[
\zeta\!\left(\tfrac12+it\right)=e^{-i\theta(t)}Z(t),
\qquad Z(t)\in\mathbb R.
\]

Set

\[
T=10121598453421191913984785.
\]

Lines 168 and 169 of Hiary's
[zero table](https://people.math.osu.edu/hiary.1/outd3/out.10121598453421191913984785.zeros)
give

\[
\gamma_-=T+20.3667281680,\qquad
\gamma_+=T+20.8915047612.
\]

The table states that Turing's method found all 220 zeros in the offset
interval \([7.31947788270188,32.1190762913185]\). Thus these adjacent rows are
consecutive zeros of zeta, not merely consecutive roots in an unchecked
critical-line list.

Independent high-precision evaluation gives

\[
\begin{aligned}
\theta(\gamma_-)/\pi
 &=88178924935987153863309894.74361066138330323684\ldots,\\
\theta(\gamma_+)/\pi
 &=88178924935987153863309899.39896227642745742655\ldots.
\end{aligned}
\]

The open gap therefore contains exactly

\[
g_{88178924935987153863309895},\ldots,
g_{88178924935987153863309899}.
\]

Hiary's corresponding
[\(Z\)-value table](https://people.math.osu.edu/hiary.1/outd3/out.10121598453421191913984785.max)
gives

\[
Z(T+20.6291751296)=-4474.45057124310.
\]

Since \(Z\) is continuous and nonzero between the consecutive zeros, it is
negative throughout the gap. At an ordinary Gram point,

\[
\operatorname{Re}\zeta\!\left(\tfrac12+ig_n\right)=(-1)^nZ(g_n).
\]

The first Gram index is odd, so the five signs are \(+,-,+,-,+\).

## Scope

This establishes an explicit maximal five-Gram numerical witness backed by a
Turing zero count. It does not identify the globally first such gap. Hiary
describes the reported ordinates and \(Z\)-values as high-accuracy numerical
values rather than interval-arithmetic certificates; the theta margins exceed
\(0.25\), and the sign sample has magnitude above \(4{,}400\), so the
classification is insensitive to the stated errors. See
[Hiary's methods page](https://people.math.osu.edu/hiary.1/fastmethods.html).
