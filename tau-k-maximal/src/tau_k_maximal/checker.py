"""Small exhaustive checker using two independent admissibility predicates."""

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from itertools import combinations

type Edge = tuple[int, int]
type Partition = tuple[tuple[int, ...], ...]


def _validate_parameters(q: int, order: int) -> None:
    if q < 2:
        raise ValueError("q must be at least 2")
    if order < 2:
        raise ValueError("order must be at least 2")


def complete_edges(order: int) -> tuple[Edge, ...]:
    """Return the lexicographically ordered edges of the simple K_order."""
    if order < 0:
        raise ValueError("order must be nonnegative")
    return tuple(combinations(range(order), 2))


def encode_edges(order: int, chosen_edges: Sequence[Edge]) -> int:
    """Encode a simple graph as a bit mask in complete_edges(order) order."""
    edge_indices = {edge: index for index, edge in enumerate(complete_edges(order))}
    mask = 0
    for raw_u, raw_v in chosen_edges:
        u, v = sorted((raw_u, raw_v))
        if u == v or u < 0 or v >= order:
            raise ValueError(f"invalid edge {(raw_u, raw_v)} for order {order}")
        try:
            index = edge_indices[(u, v)]
        except KeyError as error:
            raise ValueError(f"invalid edge {(raw_u, raw_v)} for order {order}") from error
        mask |= 1 << index
    return mask


def _set_partitions(vertices: tuple[int, ...]) -> Iterator[Partition]:
    if not vertices:
        yield ()
        return

    first = vertices[0]
    for partition in _set_partitions(vertices[1:]):
        yield ((first,), *partition)
        for index, block in enumerate(partition):
            extended = partition[:index] + ((first, *block),) + partition[index + 1 :]
            yield extended


def _induced_edge_mask(edges: Sequence[Edge], vertices: frozenset[int]) -> int:
    mask = 0
    for index, (u, v) in enumerate(edges):
        if u in vertices and v in vertices:
            mask |= 1 << index
    return mask


def _crossing_edge_mask(edges: Sequence[Edge], partition: Partition) -> int:
    part_of = {vertex: index for index, block in enumerate(partition) for vertex in block}
    mask = 0
    for index, (u, v) in enumerate(edges):
        if u in part_of and v in part_of and part_of[u] != part_of[v]:
            mask |= 1 << index
    return mask


@dataclass(frozen=True)
class PartitionConstraint:
    """One Nash--Williams--Tutte inequality."""

    edge_mask: int
    required: int


@dataclass(frozen=True)
class PackingCandidate:
    """All partition inequalities on one possible subgraph vertex set."""

    vertices: tuple[int, ...]
    constraints: tuple[PartitionConstraint, ...]


class DirectPackingOracle:
    """Test the original bar-tau condition via all vertex sets and partitions."""

    def __init__(self, q: int, order: int) -> None:
        _validate_parameters(q, order)
        self.q = q
        self.order = order
        self.edges = complete_edges(order)
        self.candidates = self._build_candidates()

    def _build_candidates(self) -> tuple[PackingCandidate, ...]:
        candidates: list[PackingCandidate] = []
        # A simple h-vertex graph cannot have q(h-1) edges when h < 2q.
        for size in range(2 * self.q, self.order + 1):
            for vertices in combinations(range(self.order), size):
                constraints: list[PartitionConstraint] = []
                for partition in _set_partitions(vertices):
                    if len(partition) < 2:
                        continue
                    constraints.append(
                        PartitionConstraint(
                            edge_mask=_crossing_edge_mask(self.edges, partition),
                            required=self.q * (len(partition) - 1),
                        )
                    )
                constraints.sort(key=lambda item: item.required, reverse=True)
                candidates.append(PackingCandidate(vertices, tuple(constraints)))
        return tuple(candidates)

    def contains_q_packing(self, graph_mask: int) -> bool:
        """Return whether some subgraph has q edge-disjoint spanning trees."""
        for candidate in self.candidates:
            if all(
                (graph_mask & constraint.edge_mask).bit_count() >= constraint.required
                for constraint in candidate.constraints
            ):
                return True
        return False


@dataclass(frozen=True)
class SparsityConstraint:
    """One induced-set form of the (q,q+1)-sparsity inequality."""

    edge_mask: int
    maximum: int


class SparsityOracle:
    """Test all induced-set (q,q+1)-sparsity inequalities."""

    def __init__(self, q: int, order: int) -> None:
        _validate_parameters(q, order)
        self.q = q
        self.order = order
        self.edges = complete_edges(order)
        self.constraints = self._build_constraints()

    def _build_constraints(self) -> tuple[SparsityConstraint, ...]:
        constraints: list[SparsityConstraint] = []
        for size in range(2, self.order + 1):
            maximum = self.q * size - (self.q + 1)
            for vertices in combinations(range(self.order), size):
                constraints.append(
                    SparsityConstraint(
                        edge_mask=_induced_edge_mask(self.edges, frozenset(vertices)),
                        maximum=maximum,
                    )
                )
        return tuple(constraints)

    def is_sparse(self, graph_mask: int) -> bool:
        """Return whether the graph is (q,q+1)-sparse."""
        return all(
            (graph_mask & constraint.edge_mask).bit_count() <= constraint.maximum
            for constraint in self.constraints
        )


@dataclass(frozen=True)
class CheckResult:
    """Summary of one exhaustive labeled-graph check."""

    q: int
    order: int
    total_graphs: int
    admissible_graphs: int
    maximal_graphs: int
    maximal_edge_counts: tuple[int, ...]

    @property
    def predicted_edge_count(self) -> int:
        return self.q * self.order - (self.q + 1)


def exhaustive_check(q: int, order: int, *, max_ground_edges: int = 18) -> CheckResult:
    """Compare both predicates and enumerate every maximal admissible graph."""
    _validate_parameters(q, order)
    if order < 2 * q:
        raise ValueError("the theorem range requires order >= 2q")

    edge_count = len(complete_edges(order))
    if edge_count > max_ground_edges:
        raise ValueError(f"K_{order} has {edge_count} edges; limit is {max_ground_edges}")

    direct = DirectPackingOracle(q, order)
    sparse = SparsityOracle(q, order)
    total_graphs = 1 << edge_count
    admissible = bytearray(total_graphs)

    for graph_mask in range(total_graphs):
        direct_value = not direct.contains_q_packing(graph_mask)
        sparse_value = sparse.is_sparse(graph_mask)
        if direct_value != sparse_value:
            raise AssertionError(
                "direct packing and sparsity predicates disagree for "
                f"q={q}, order={order}, mask={graph_mask}"
            )
        admissible[graph_mask] = direct_value

    maximal_graphs = 0
    maximal_edge_counts: set[int] = set()
    ground_mask = total_graphs - 1
    for graph_mask, is_admissible in enumerate(admissible):
        if not is_admissible:
            continue
        missing = ground_mask ^ graph_mask
        while missing:
            edge_bit = missing & -missing
            if admissible[graph_mask | edge_bit]:
                break
            missing ^= edge_bit
        else:
            maximal_graphs += 1
            maximal_edge_counts.add(graph_mask.bit_count())

    return CheckResult(
        q=q,
        order=order,
        total_graphs=total_graphs,
        admissible_graphs=sum(admissible),
        maximal_graphs=maximal_graphs,
        maximal_edge_counts=tuple(sorted(maximal_edge_counts)),
    )


def tight_construction(q: int, order: int) -> tuple[Edge, ...]:
    """Construct K_{2q}-e, then add q-valent vertices."""
    _validate_parameters(q, order)
    if order < 2 * q:
        raise ValueError("tight construction requires order >= 2q")

    chosen = [edge for edge in complete_edges(2 * q) if edge != (0, 1)]
    for vertex in range(2 * q, order):
        chosen.extend((old_vertex, vertex) for old_vertex in range(q))
    return tuple(chosen)
