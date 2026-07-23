# Eventual zero forcing for \(P(n,8)\)

This package proves:

\[
\boxed{Z(P(n,8))=18\qquad(n\ge65).}
\]

An exact balanced-separator computation gives
\(\operatorname{pw}(P(n,8))\ge18\) at the eight consecutive orders
\(65,\ldots,72\). An eight-column topological-minor reduction transfers those bases to
all larger orders, and an explicit 18-vertex forcing schedule gives the matching upper
bound.

Order 64 is only a positive separator control: its explicit half-set has exact internal
boundary 16, and no claim about \(Z(P(64,8))\) is made.

Fast gates:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

The full frozen replay is:

```console
uv run zero-forcing-petersen-k8-eventual-check
```

The native C++20 verifier uses six workers. Its first run took about 46 minutes and
stayed below 0.5 GiB RSS on the development machine.
