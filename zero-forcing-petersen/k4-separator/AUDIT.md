# Certificate audit

The transfer recurrence is Boolean and exact. It retains, for every current state and
separator weight \(0\le b\le9\), an integer bitset encoding every starting state and balance
value. A diagonal bit at balance zero is equivalent to a balanced closed walk.

The accepting-state digest hashes the full diagonal-state set for every
\((n,b)\in\{1,\ldots,162\}\times\{0,\ldots,9\}\), not only the final exclusions.

The finite computation proves only \(23\le n\le162\). Infinite scope comes from the explicit
clean-run deletion in [THEOREM.md](THEOREM.md); no extrapolation from sampled orders is used.

The package also checks both threshold witnesses directly and tests the paired deletion on a
large balanced coloring.
