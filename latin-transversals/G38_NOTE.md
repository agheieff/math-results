# A counterexample to a claim about `G_38`

Ghafari--Wanless arXiv:2607.17547v1 says that every transversal of `G_n`
containing exactly two of its three delta-3 entries must also contain
`E=(16,12,29)`. The following row-indexed column permutation disproves that
sentence already for `n=38`:

```text
21,29,18,28,19,17,6,15,8,24,33,10,16,14,35,13,27,31,37,
32,26,36,23,9,20,34,30,25,22,12,4,11,3,7,5,1,2,0
```

It is a transversal. Its only nonzero `(row,column,delta)` triples are

```text
(0,21,4), (5,17,4), (6,6,3), (10,33,4), (11,10,3), (15,13,1).
```

Their deltas sum to `19=n/2`. Thus the transversal contains the second and
third delta-3 entries, omits the first, and also omits `E`. The alternate
delta-1 entry `(15,13,29)` supplies the needed unit.

This does not refute Lemma 7: the transversal still contains two of the three
delta-3 entries. It also does not refute the paper's Theorem 6. It only
invalidates the quoted justification for why a fourth computational witness
was needed.

The certificate is checked directly in `tests/test_g38_claim.py`. The
comma-separated column string has SHA-256
`d8665d91634aa832a0db4968d1f994d0ab42e2b290d89581473c44812b5e906f`.

Source: <https://arxiv.org/abs/2607.17547>
