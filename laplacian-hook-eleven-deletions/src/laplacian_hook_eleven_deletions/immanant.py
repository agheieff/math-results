"""Subset cycle-cover immanant recurrence."""

from collections.abc import Sequence

from laplacian_hook_eleven_deletions.model import Polynomial


def _hamilton_counts(adjacency: Sequence[Sequence[int]]) -> tuple[int, ...]:
    order = len(adjacency)
    full = 1 << order
    cycles = [0] * full
    for root in range(order - 1):
        allowed = (full - 1) ^ ((1 << (root + 1)) - 1)
        paths = [[0] * order for _ in range(full)]
        for subset in range(1, full):
            if subset & ~allowed:
                continue
            endpoints = subset
            while endpoints:
                bit = endpoints & -endpoints
                endpoint = bit.bit_length() - 1
                previous = subset ^ bit
                if not previous:
                    value = adjacency[root][endpoint]
                else:
                    value = 0
                    predecessors = previous
                    while predecessors:
                        predecessor_bit = predecessors & -predecessors
                        predecessor = predecessor_bit.bit_length() - 1
                        value += paths[previous][predecessor] * adjacency[predecessor][endpoint]
                        predecessors ^= predecessor_bit
                paths[subset][endpoint] = value
                endpoints ^= bit
            cycles[(1 << root) | subset] = sum(
                paths[subset][endpoint] * adjacency[endpoint][root]
                for endpoint in range(order)
                if subset & (1 << endpoint)
            )
    return tuple(cycles)


def hook_immanantal_polynomial(adjacency: Sequence[Sequence[int]], rank: int) -> Polynomial:
    order = len(adjacency)
    width = order + 1
    cycles = _hamilton_counts(adjacency)
    covers: list[list[int]] = [[] for _ in range(1 << order)]
    covers[0] = [1] + [0] * ((rank + 1) * width - 1)
    for mask in range(1, 1 << order):
        vertex_bit = mask & -mask
        vertex = vertex_bit.bit_length() - 1
        rest = mask ^ vertex_bit
        output = [0] * ((rank + 1) * width)
        degree = sum(adjacency[vertex])
        for t_degree in range(rank + 1):
            offset = t_degree * width
            for x_degree in range(width - 1):
                value = covers[rest][offset + x_degree]
                if value:
                    output[offset + x_degree] -= degree * value
                    output[offset + x_degree + 1] += value
                    if t_degree < rank:
                        output[offset + width + x_degree] -= degree * value
                        output[offset + width + x_degree + 1] += value
        subset = rest
        while subset:
            cycle_mask = vertex_bit | subset
            count = cycles[cycle_mask]
            if count:
                length = cycle_mask.bit_count()
                base = covers[rest ^ subset]
                for t_degree in range(rank + 1):
                    for x_degree in range(width):
                        value = base[t_degree * width + x_degree]
                        if value:
                            output[t_degree * width + x_degree] += count * value
                            if t_degree + length <= rank:
                                output[(t_degree + length) * width + x_degree] += (
                                    (-1) ** (length + 1) * count * value
                                )
            subset = (subset - 1) & rest
        covers[mask] = output
    numerator = covers[-1]
    previous = [0] * width
    for t_degree in range(rank + 1):
        previous = [
            numerator[t_degree * width + x_degree] - previous[x_degree] for x_degree in range(width)
        ]
    return tuple(reversed(previous))
