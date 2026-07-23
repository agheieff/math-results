# Reproduction

## Environment

```sh
uv sync --group dev
```

Run the exact census, paper-seed audit, and seven-vertex Burnside boundary:

```sh
uv run duval-reiner-r3-r4-check
```

The run takes several seconds on a typical workstation. Its frozen output is
[artifacts/census-summary.json](artifacts/census-summary.json).

## Quality gates

```sh
uv run --group dev pytest
uv run --group dev ruff check .
uv run --group dev ruff format --check .
uv run --group dev mypy
```

The integration test reruns all 2,136 exact orbit certificates and checks the final status
counts.

## Trust boundary

`families.py` performs full permutation-orbit reduction. `laplacian.py` constructs the signed
integer boundary Gram matrix. `spectrum.py` uses exact characteristic polynomials,
factorization, Vieta traces, and rational real-root isolation. `census.py` requires one exact
certificate for every orbit representative.

NumPy eigenvalues select and summarize screening cases only. Removing the numerical screen
does not change any exact status.

The SHA-256 digest in the artifact commits, in representative order, to every mask, degree
sequence, characteristic polynomial, factorization, and partial-sum certificate.
