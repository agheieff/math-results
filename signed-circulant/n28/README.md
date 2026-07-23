# Exact \(n=28\) signed-circulant gate

This directory checks only the \(n=28\) case of Conjecture 3 in
[arXiv:2607.18334v1](https://arxiv.org/abs/2607.18334).

## Frozen statement

For all signings of \(C_{28}(1,2)\),

\[
\min_\sigma \rho(A_\sigma)
=2\sqrt{\cos^2(\pi/28)+\cos^2(\pi/14)}.
\]

Exactly the two twisted switching classes attain the minimum. This is not a
proof for any other order.

## Replay

```sh
uv lock --check
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run signed-circulant-n28-check
```

See [REPORT.md](REPORT.md), [CERTIFICATE.md](CERTIFICATE.md), and
[RED_TEAM.md](RED_TEAM.md).
