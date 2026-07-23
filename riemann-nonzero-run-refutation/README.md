# Four-crossing sign-pattern refutation near \(10^{25}\)

Hiary's published sample of ten million critical-line zeros near \(T=10^{25}\)
contains a consecutive listed zero gap with four Gram points whose real-zeta signs are

\[
\;-\;+\;-.
\]

Thus the empirical conjecture that this pattern never occurs in a nonzero critical-line
crossing run is refuted in that published sample. This is a reproducible numerical
counterexample, not a rigorous theorem about the zeros of \(\zeta\): the source describes
the table's errors as typical root-mean-square accuracies rather than certified bounds.

Replay the frozen witness:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run riemann-nonzero-run-check
```

To check the whole downloaded tables and reproduce the 30 forbidden gaps:

```console
uv run riemann-nonzero-run-check \
  --zeros /path/to/1e25.zeros.501_10000501.gz \
  --derivatives /path/to/1e25.zeros.501_10000501.der.gz \
  --full-scan
```
