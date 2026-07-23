from __future__ import annotations

from dataclasses import dataclass

from .graph import GeneralizedPetersen


@dataclass(frozen=True)
class Force:
    source: int
    target: int

    def as_names(self, graph: GeneralizedPetersen) -> tuple[str, str]:
        return graph.vertex_name(self.source), graph.vertex_name(self.target)


def uniform_seed(n: int) -> int:
    graph = GeneralizedPetersen(n)
    outer = sum(1 << index for index in range(8))
    return outer | 1 << graph.n | 1 << (graph.n + 7)


def replay_uniform_schedule(n: int) -> tuple[Force, ...]:
    """Replay the ten-vertex schedule for P(n,4), n >= 9."""
    graph = GeneralizedPetersen(n)
    black = uniform_seed(n)
    forces: list[Force] = []

    def apply(source: int, target: int) -> None:
        nonlocal black
        target_bit = 1 << target
        if black & target_bit:
            raise AssertionError("the schedule repeats a target")
        if graph.neighbor_masks[source] & ~black != target_bit:
            raise AssertionError(
                f"{graph.vertex_name(source)} -> {graph.vertex_name(target)} is not legal"
            )
        black |= target_bit
        forces.append(Force(source, target))

    for index in range(1, 7):
        apply(index, n + index)

    for index in range(n - 1, 7, -1):
        apply((index + 1) % n, index)
        apply(n + (index + 4) % n, n + index)

    if black != graph.full_mask:
        raise AssertionError("the uniform schedule did not color the graph")
    return tuple(forces)
