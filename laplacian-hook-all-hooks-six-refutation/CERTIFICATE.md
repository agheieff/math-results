# Certificate and replay

The saved JSON contains all seven explicit sparse witnesses, their canonical
keys, shared sparse factorizations, general dense-complement factorizations,
and full reference-order coefficient tuples.

Replay:

- recomputes every canonical component key;
- proves each class contains distinct graph types;
- recomputes sparse and dense characteristic polynomials from matrix traces;
- checks \(L(K_n-H)=nI-J-L(H)\) entrywise;
- verifies the padded identities directly through order twelve;
- compares the regenerated result with the saved JSON.

```sh
uv run laplacian-hook-six-refutation-check
```

The all-order conclusion uses the displayed exact matrix identity, not
finite-order extrapolation.
