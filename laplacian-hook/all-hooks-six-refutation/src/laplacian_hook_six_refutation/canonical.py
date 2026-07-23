"""Canonical component keys proving the witnesses are nonisomorphic."""

from itertools import permutations

from laplacian_hook_six_refutation.model import EdgeSet

ComponentKey = tuple[int, int]
GraphKey = tuple[ComponentKey, ...]


def _component_key(vertices: frozenset[int], edges: EdgeSet) -> ComponentKey:
    ordered = tuple(sorted(vertices))
    best = -1
    for order in permutations(ordered):
        code = 0
        bit = 0
        for left in range(len(order)):
            for right in range(left + 1, len(order)):
                first = order[left]
                second = order[right]
                edge = (first, second) if first < second else (second, first)
                if edge in edges:
                    code |= 1 << bit
                bit += 1
        best = max(best, code)
    return len(vertices), best


def graph_key(edges: EdgeSet) -> GraphKey:
    active = {vertex for edge in edges for vertex in edge}
    adjacency = {vertex: set[int]() for vertex in active}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    components: list[ComponentKey] = []
    unseen = set(active)
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        stack = [root]
        vertices: set[int] = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        components.append(_component_key(frozenset(vertices), edges))
    return tuple(sorted(components))


def format_graph_key(key: GraphKey) -> str:
    return "-".join(f"v{order}e{code:x}" for order, code in key)
