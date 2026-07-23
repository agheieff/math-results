"""Finite lower and upper zero-forcing certificates."""

from __future__ import annotations

import hashlib
import math
from collections import Counter
from dataclasses import dataclass

from .graph import closure, petersen_adjacency
from .pathwidth import fixed_weight_masks


@dataclass(frozen=True)
class SevenSetCertificate:
    n: int
    tested: int
    forcing_sets: int
    maximum_closure_size: int
    closure_histogram: tuple[tuple[int, int], ...]
    replay_digest_sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "graph": f"P({self.n},3)",
            "seven_sets_tested": self.tested,
            "forcing_seven_sets": self.forcing_sets,
            "maximum_closure_size": self.maximum_closure_size,
            "closure_histogram": {str(size): count for size, count in self.closure_histogram},
            "replay_digest_sha256": self.replay_digest_sha256,
        }


def certify_seven_sets(n: int) -> SevenSetCertificate:
    adjacency = petersen_adjacency(n)
    byte_width = (2 * n + 7) // 8
    digest = hashlib.sha256()
    histogram: Counter[int] = Counter()
    forcing_sets = 0
    tested = 0
    maximum = 0
    full_mask = (1 << (2 * n)) - 1
    for initial in fixed_weight_masks(2 * n, 7):
        closed = closure(adjacency, initial)
        closed_size = closed.bit_count()
        histogram[closed_size] += 1
        maximum = max(maximum, closed_size)
        forcing_sets += closed == full_mask
        tested += 1
        digest.update(initial.to_bytes(byte_width, "little"))
        digest.update(closed.to_bytes(byte_width, "little"))
    if tested != math.comb(2 * n, 7):
        raise AssertionError("fixed-weight enumeration is incomplete")
    return SevenSetCertificate(
        n=n,
        tested=tested,
        forcing_sets=forcing_sets,
        maximum_closure_size=maximum,
        closure_histogram=tuple(sorted(histogram.items())),
        replay_digest_sha256=digest.hexdigest(),
    )


def eight_outer_vertices_force(n: int) -> bool:
    adjacency = petersen_adjacency(n)
    initial = (1 << 8) - 1
    return closure(adjacency, initial) == (1 << (2 * n)) - 1


def replay_symbolic_upper_bound(n: int) -> tuple[tuple[int, int], ...]:
    """Replay exactly the parameterized force schedule in THEOREM.md."""
    if n < 13:
        raise ValueError("the symbolic schedule is asserted only for n at least thirteen")
    adjacency = petersen_adjacency(n)
    black = (1 << 8) - 1
    forces: list[tuple[int, int]] = []

    def apply(source: int, target: int) -> None:
        nonlocal black
        target_bit = 1 << target
        if black & target_bit:
            return
        if adjacency[source] & ~black != target_bit:
            raise AssertionError(f"{source}->{target} is not a legal force at n={n}")
        black |= target_bit
        forces.append((source, target))

    for index in range(1, 7):
        apply(index, n + index)
    for source_index, target_index in (
        (1, n - 2),
        (2, n - 1),
        (3, 0),
        (4, 7),
        (5, 8),
        (6, 9),
    ):
        apply(n + source_index, n + target_index)
    apply(0, n - 1)
    apply(7, 8)
    apply(n, n + n - 3)
    apply(n + 7, n + 10)

    wave_count = max(0, (n - 13) // 2)
    for step in range(wave_count):
        apply(8 + step, 9 + step)
        apply(n - 1 - step, n - 2 - step)
        apply(n + 8 + step, n + 11 + step)
        apply(n + n - 1 - step, n + n - 4 - step)

    inner_mask = ((1 << n) - 1) << n
    if black & inner_mask != inner_mask:
        raise AssertionError("the symbolic waves did not color the entire inner layer")
    first_white_outer = 9 + wave_count
    last_white_outer = n - wave_count - 2
    for target in range(first_white_outer, last_white_outer + 1):
        apply(target - 1, target)
    if black != (1 << (2 * n)) - 1:
        raise AssertionError("the symbolic schedule did not color the graph")
    return tuple(forces)
