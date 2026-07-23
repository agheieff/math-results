"""The path-tree switching gauge for C_24(1,2)."""

from collections.abc import Iterable, Sequence

N = 24
TREE_EDGES = tuple((i, i + 1) for i in range(N - 1))
COTREE_EDGES = ((N - 1, 0), *((i, (i + 2) % N) for i in range(N)))
EDGES = (*TREE_EDGES, *COTREE_EDGES)
CLASS_BITS = len(COTREE_EDGES)
CLASS_COUNT = 1 << CLASS_BITS

Matrix = tuple[tuple[int, ...], ...]
Signing = tuple[int, ...]


def signing_from_mask(mask: int) -> Signing:
    """Return the unique tree-positive signing represented by ``mask``."""
    if not 0 <= mask < CLASS_COUNT:
        raise ValueError(f"mask must be in [0, {CLASS_COUNT})")
    return (1,) * len(TREE_EDGES) + tuple(
        -1 if (mask >> bit) & 1 else 1 for bit in range(CLASS_BITS)
    )


def mask_from_normalized_signing(signing: Sequence[int]) -> int:
    """Encode a tree-positive signing."""
    if len(signing) != len(EDGES):
        raise ValueError(f"expected {len(EDGES)} signs")
    if any(sign not in (-1, 1) for sign in signing):
        raise ValueError("signs must be -1 or 1")
    if any(sign != 1 for sign in signing[: len(TREE_EDGES)]):
        raise ValueError("tree edges are not gauge-normalized")
    mask = 0
    for bit, sign in enumerate(signing[len(TREE_EDGES) :]):
        mask |= (sign == -1) << bit
    return mask


def switch_signing(signing: Sequence[int], switches: Sequence[int]) -> Signing:
    """Apply vertex switching to every edge."""
    if len(signing) != len(EDGES) or len(switches) != N:
        raise ValueError("wrong signing or switching length")
    if any(value not in (-1, 1) for value in (*signing, *switches)):
        raise ValueError("all values must be -1 or 1")
    return tuple(
        sign * switches[u] * switches[v] for sign, (u, v) in zip(signing, EDGES, strict=True)
    )


def normalize_signing(signing: Sequence[int]) -> Signing:
    """Switch uniquely to positive path-tree signs, fixing switch[0] = 1."""
    if len(signing) != len(EDGES):
        raise ValueError(f"expected {len(EDGES)} signs")
    switches = [1]
    for edge_sign in signing[: len(TREE_EDGES)]:
        switches.append(switches[-1] * edge_sign)
    return switch_signing(signing, switches)


def matrix_from_signing(signing: Sequence[int]) -> Matrix:
    """Build the symmetric signed adjacency matrix."""
    rows = [[0] * N for _ in range(N)]
    for sign, (u, v) in zip(signing, EDGES, strict=True):
        rows[u][v] = sign
        rows[v][u] = sign
    return tuple(tuple(row) for row in rows)


def matrix_from_mask(mask: int) -> Matrix:
    return matrix_from_signing(signing_from_mask(mask))


def triangle_fluxes(mask: int) -> tuple[int, ...]:
    """Return the signs of triangles (i,i+1,i+2)."""
    signing = signing_from_mask(mask)
    signs = {frozenset(edge): sign for edge, sign in zip(EDGES, signing, strict=True)}
    return tuple(
        signs[frozenset((i, (i + 1) % N))]
        * signs[frozenset(((i + 1) % N, (i + 2) % N))]
        * signs[frozenset((i, (i + 2) % N))]
        for i in range(N)
    )


def hamilton_holonomy(mask: int) -> int:
    """Return the sign product around the step-1 Hamilton cycle."""
    return -1 if mask & 1 else 1


def twisted_masks() -> tuple[int, int]:
    """Construct the two alternating-flux, anti-periodic gauge classes."""
    masks: list[int] = []
    for tau0 in (-1, 1):
        edge_signs = [1] * len(EDGES)
        edge_signs[len(TREE_EDGES)] = -1
        step1 = [1] * (N - 1) + [-1]
        for i in range(N):
            tau = tau0 if i % 2 == 0 else -tau0
            step2 = tau * step1[i] * step1[(i + 1) % N]
            edge_signs[len(TREE_EDGES) + 1 + i] = step2
        masks.append(mask_from_normalized_signing(edge_signs))
    masks.sort()
    return masks[0], masks[1]


TARGET_MASKS = twisted_masks()


def is_alternating(values: Iterable[int]) -> bool:
    sequence = tuple(values)
    return len(sequence) == N and all(sequence[(i + 1) % N] == -sequence[i] for i in range(N))
