# Exact checker

The checker has four independent finite duties.

1. It constructs \(M(C_q)\) directly from the edge definition and replays
   the explicit five-vertex forcing sequence one force at a time.
2. It exhausts every one of the \(\binom{2q+1}{4}\) four-vertex initial
   sets for each requested \(q\). Closure uses integer bitsets only.
3. At \(q=4\), it constructs the integral matrix
   \[
   \begin{pmatrix}C&C&0\\C&0&\mathbf1\\0&\mathbf1^{\mathsf T}&-2\end{pmatrix},
   \]
   checks its exact off-diagonal support, and computes rank \(4\) over
   \(\mathbb Q\), hence nullity \(5\). At \(q=5\), it similarly checks the
   integral specialization \((a,b,f)=(1,-1,1)\) of the infinite spectral
   certificate, obtaining rank \(6\) and nullity \(5\).
4. At \(q=6\), it checks all 16 listed sets are forts, generates the 81
   transversals of the four disjoint parity forts, and verifies that none
   meets all 12 remaining forts. After the first nine additional forts,
   exactly the six candidates stated in [THEOREM.md](THEOREM.md) remain.

The default regression range is every \(q\) from \(4\) through \(13\). It
can be changed:

```sh
uv run zero-forcing-mycielski-check --orders 4 6 8 15
```

The exhaustive closure sweep is corroboration only. The all-\(q\) proof is
the spectral argument plus the isolated exact certificates for \(q=4,6\)
in [THEOREM.md](THEOREM.md).
