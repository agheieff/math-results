import json
from dataclasses import asdict, dataclass
from itertools import combinations

from hadwiger_k7.graph import (
    degrees,
    graph_sha256,
    independent_sets,
    is_clique,
    is_independent,
    missing_edge_matchings,
)
from hadwiger_k7.minor_connected_sets import has_complete_minor as connected_set_check
from hadwiger_k7.minor_partitions import has_complete_minor as partition_check
from hadwiger_k7.obstruction import EXPECTED_ROOK_SHA256, rook_graph


@dataclass(frozen=True)
class VerificationReport:
    graph_sha256: str
    independent_triples: int
    completions_per_triple: tuple[int, ...]
    checked_triple_completion_pairs: int
    minor_checkers: int


def verify_counterexample() -> VerificationReport:
    graph = rook_graph()
    digest = graph_sha256(graph)
    _require(digest == EXPECTED_ROOK_SHA256, "raw graph hash mismatch")
    _require(graph.order == 9, "wrong order")

    graph_degrees = degrees(graph)
    _require(min(graph_degrees) >= 1, "minimum degree is below 1")
    _require(min(graph_degrees) <= 4, "minimum degree is above 4")
    _require(
        not any(is_clique(graph, vertices) for vertices in combinations(range(9), 4)),
        "graph contains K4",
    )

    triples = independent_sets(graph, 3)
    _require(bool(triples), "independence number is below 3")
    _require(
        not any(is_independent(graph, vertices) for vertices in combinations(range(9), 4)),
        "independence number is above 3",
    )
    _require(not partition_check(graph, 6), "partition checker found a K6 minor")
    _require(not connected_set_check(graph, 6), "connected-set checker found a K6 minor")

    completion_counts: list[int] = []
    total = 0
    for triple in triples:
        allowed = tuple(vertex for vertex in range(graph.order) if vertex not in triple)
        count = 0
        for matching in missing_edge_matchings(graph, allowed):
            _require(_is_valid_completion(graph.edges, allowed, matching), "invalid completion")
            completed = graph.with_added_edges(matching)
            _require(
                not partition_check(completed, 6),
                f"partition checker found a K6 minor for S={triple}, M={matching}",
            )
            _require(
                not connected_set_check(completed, 6),
                f"connected-set checker found a K6 minor for S={triple}, M={matching}",
            )
            count += 1
        completion_counts.append(count)
        total += count

    _require(len(triples) == 6, "unexpected independent-triple count")
    _require(completion_counts == [32] * 6, "unexpected matching count")
    _require(total == 192, "unexpected search total")
    return VerificationReport(
        graph_sha256=digest,
        independent_triples=len(triples),
        completions_per_triple=tuple(completion_counts),
        checked_triple_completion_pairs=total,
        minor_checkers=2,
    )


def _is_valid_completion(
    original_edges: frozenset[tuple[int, int]],
    allowed: tuple[int, ...],
    matching: tuple[tuple[int, int], ...],
) -> bool:
    allowed_set = set(allowed)
    endpoints: set[int] = set()
    for edge in matching:
        if edge in original_edges or not set(edge) <= allowed_set:
            return False
        if endpoints & set(edge):
            return False
        endpoints.update(edge)
    return True


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    print(json.dumps(asdict(verify_counterexample()), sort_keys=True))


if __name__ == "__main__":
    main()
