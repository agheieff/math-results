from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .forcing import vertex_mask
from .model import MycielskiCycle


@dataclass(frozen=True)
class FortFamilies:
    parity: tuple[int, ...]
    antipodal: tuple[int, ...]
    local: tuple[int, ...]
    complements: tuple[int, ...]

    @property
    def all(self) -> tuple[int, ...]:
        return self.parity + self.antipodal + self.local + self.complements


def q6_fort_families(graph: MycielskiCycle) -> FortFamilies:
    if graph.order != 6:
        raise ValueError("the fort certificate is specific to q=6")

    parity = (
        vertex_mask(graph.original(index) for index in (0, 2, 4)),
        vertex_mask(graph.original(index) for index in (1, 3, 5)),
        vertex_mask(graph.shadow(index) for index in (0, 2, 4)),
        vertex_mask(graph.shadow(index) for index in (1, 3, 5)),
    )
    antipodal = tuple(
        vertex_mask(
            (
                graph.original(index),
                graph.original(index + 3),
                graph.shadow(index),
                graph.shadow(index + 3),
                graph.apex,
            )
        )
        for index in range(3)
    )
    local = tuple(
        vertex_mask(
            (
                graph.original(center - 1),
                graph.original(center),
                graph.original(center + 1),
                graph.shadow(center + 3),
                graph.apex,
            )
        )
        for center in range(6)
    )
    complements = tuple(
        vertex_mask(
            [graph.original(index) for index in range(6) if index % 3 != omitted] + [graph.apex]
        )
        for omitted in range(3)
    )
    return FortFamilies(parity, antipodal, local, complements)


def is_fort(graph: MycielskiCycle, vertices: int) -> bool:
    if not vertices:
        return False
    for vertex, neighbors in enumerate(graph.adjacency):
        if vertices & (1 << vertex):
            continue
        if (neighbors & vertices).bit_count() == 1:
            return False
    return True


def _members(vertices: int) -> tuple[int, ...]:
    return tuple(index for index in range(vertices.bit_length()) if vertices & (1 << index))


@dataclass(frozen=True)
class FortCertificateResult:
    fort_count: int
    candidate_count: int
    survivors_after_first_two_families: tuple[int, ...]
    final_survivors: tuple[int, ...]


def q6_fort_certificate() -> FortCertificateResult:
    graph = MycielskiCycle.build(6)
    families = q6_fort_families(graph)
    if not all(is_fort(graph, fort) for fort in families.all):
        raise AssertionError("listed set is not a fort")

    candidates = tuple(
        vertex_mask(choice) for choice in product(*(_members(fort) for fort in families.parity))
    )
    first_two = families.antipodal + families.local
    survivors = tuple(
        candidate for candidate in candidates if all(candidate & fort for fort in first_two)
    )
    expected = {
        vertex_mask(
            (
                graph.original(index),
                graph.original(index + 3),
                graph.shadow(index + 1),
                graph.shadow(index + 2),
            )
        )
        for index in range(6)
    }
    if set(survivors) != expected:
        raise AssertionError("unexpected intermediate transversals")
    final = tuple(
        candidate
        for candidate in survivors
        if all(candidate & fort for fort in families.complements)
    )
    return FortCertificateResult(len(families.all), len(candidates), survivors, final)
