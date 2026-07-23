# Zero forcing in \(P(n,4)\): finite threshold certificate

This package proves

\[
Z(P(n,4))=10\qquad(18\le n\le22).
\]

It exhausts one representative of every cyclic orbit of 9-subsets, with \(n=17\) as a
positive control, and independently replays a symbolic 10-vertex forcing schedule for every
tested \(9\le n\le200\). The schedule is valid symbolically for every \(n\ge9\).

The finite interval is the bridge to the separate half-separator certificate beginning at
\(n=23\).

Reproduce the frozen certificate:

```sh
uv sync --group dev
uv run zero-forcing-petersen-k4-check
```

A C++20 compiler and OpenSSL development headers are required for the exact orbit census.
