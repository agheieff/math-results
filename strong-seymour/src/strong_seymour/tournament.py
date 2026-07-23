from __future__ import annotations

from collections.abc import Sequence


class TournamentError(ValueError):
    """Raised when an adjacency matrix is not a tournament."""


def validate_adjacency(adjacency: Sequence[Sequence[int]]) -> None:
    n = len(adjacency)
    if any(len(row) != n for row in adjacency):
        raise TournamentError("adjacency matrix must be square")
    for source in range(n):
        if adjacency[source][source] != 0:
            raise TournamentError(f"loop at vertex {source}")
        for target in range(source + 1, n):
            if adjacency[source][target] + adjacency[target][source] != 1:
                raise TournamentError(f"pair {source}, {target} has wrong arc count")
            if adjacency[source][target] not in (0, 1):
                raise TournamentError(f"entry {source}, {target} is not Boolean")


def out_neighbours(adjacency: Sequence[Sequence[int]], vertex: int) -> tuple[int, ...]:
    return tuple(target for target, arc in enumerate(adjacency[vertex]) if arc == 1)


def second_out_neighbours(
    adjacency: Sequence[Sequence[int]], vertex: int
) -> tuple[int, ...]:
    first = set(out_neighbours(adjacency, vertex))
    return tuple(
        target
        for target in range(len(adjacency))
        if target != vertex
        and target not in first
        and any(adjacency[middle][target] for middle in first)
    )


def maximum_matching(
    adjacency: Sequence[Sequence[int]], left: Sequence[int], right: Sequence[int]
) -> tuple[tuple[int, int], ...]:
    """Return a maximum matching using an independent augmenting-path algorithm."""
    right_set = set(right)
    matched_left_by_right: dict[int, int] = {}

    def augment(source: int, seen: set[int]) -> bool:
        for target in right_set:
            if not adjacency[source][target] or target in seen:
                continue
            seen.add(target)
            previous = matched_left_by_right.get(target)
            if previous is None or augment(previous, seen):
                matched_left_by_right[target] = source
                return True
        return False

    for source in left:
        augment(source, set())
    return tuple(sorted((source, target) for target, source in matched_left_by_right.items()))


def strong_seymour_matching(
    adjacency: Sequence[Sequence[int]], vertex: int
) -> tuple[tuple[int, int], ...] | None:
    first = out_neighbours(adjacency, vertex)
    second = second_out_neighbours(adjacency, vertex)
    matching = maximum_matching(adjacency, first, second)
    return matching if len(matching) == len(first) else None


def hall_neighbours(
    adjacency: Sequence[Sequence[int]], vertex: int, witness: Sequence[int]
) -> tuple[int, ...]:
    first = set(out_neighbours(adjacency, vertex))
    if not witness or not set(witness) <= first:
        raise TournamentError(f"invalid Hall witness at vertex {vertex}")
    return tuple(
        target
        for target in range(len(adjacency))
        if target != vertex
        and target not in first
        and any(adjacency[source][target] for source in witness)
    )

