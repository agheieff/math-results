# Cyclic unique-multiset-sum gap

This lane strengthens the elementary cyclic lower bound for the
unique-multiset-sum problem of arXiv:2607.08366v2.

If \(n\ge2\) residues in \(\mathbb Z_N\) have unique multiset sums, then

\[
N\ge 2^{n-1}+2\left\lfloor\frac{n-1}{2}\right\rfloor.
\]

The proof first shows that every nonzero doubled basepoint difference lies
outside the \(2^{n-1}\)-element subset-sum image. Subset-sum injectivity
allows at most one collision pair under doubling and prevents that pair from
coexisting with an order-two difference; parity then gives the displayed
bound. This does not prove the conjectured
\(N\ge2^n-2^{\lfloor\log_2n\rfloor}\).

The checker exhausts normalized small cyclic families and dissociated
difference sets, and also converts a doubled-subset collision into its
forbidden multiplicity vector. Computation is regression evidence, not part
of the proof.

See `PROOF.md` for the argument, `RED_TEAM.md` for the independent audit, and
`PRIOR_ART.md` for the novelty boundary.

```sh
uv sync --extra dev
uv run cyclic-ums-check
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
```
