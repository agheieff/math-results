# Zero forcing for path Mycielskians

For the path \(P_n\), this lane proves

\[
Z(M(P_n))=
\begin{cases}
2,&n=2,\\
3,&n\ge3.
\end{cases}
\]

Consequently, the Annor--Howerton \((\chi,\omega,Z)\)-bound is sharp for
every \(M(P_n)\), \(n\ge2\).

The upper bound is an explicit three-vertex forcing sequence. The generic
lower bound uses a nullity-three symmetric matrix; \(n=3,5\) have three
pairwise disjoint forts. See [THEOREM.md](THEOREM.md).

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-mycielski-paths-check
```
