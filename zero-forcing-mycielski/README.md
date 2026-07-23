# Zero forcing for cycle Mycielskians

For every integer \(q\ge4\), this lane proves

\[
Z(M(C_q))=5.
\]

For odd \(q\), \(M(C_q)\) consequently has

\[
(\chi,\omega,Z)=(4,2,5),
\]

so the Annor--Howerton \((\chi,\omega,Z)\)-conjecture holds with equality.
The independent set of all shadow vertices also witnesses their Condition
\((R)\) for the entire odd family.

The lower bound uses symmetric nullity-five matrices except at \(q=6\),
where a 16-fort hitting certificate handles the exceptional case. The upper
bound is a uniform five-vertex forcing sequence. See
[THEOREM.md](THEOREM.md).

An independent audit of the full argument is recorded in
[RED_TEAM.md](RED_TEAM.md).

The checker exactly replays the forcing sequence, exhausts all four-vertex
initial sets over a finite regression range, checks the integral
nullity-five matrices at \(q=4,5\), and replays the \(q=6\) fort
certificate. The infinite part of the theorem rests on the written spectral
proof, not on finite computation.

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run zero-forcing-mycielski-check
```
