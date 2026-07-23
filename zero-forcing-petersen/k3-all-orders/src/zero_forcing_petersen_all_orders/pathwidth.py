"""Exact reachable-prefix certificates for vertex separation at width seven."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Iterator
from dataclasses import dataclass

from .graph import boundary_size


def fixed_weight_masks(vertex_count: int, weight: int) -> Iterator[int]:
    """Yield fixed-weight masks in increasing numerical order."""
    if not 0 <= weight <= vertex_count:
        raise ValueError("weight must lie between zero and the vertex count")
    if weight == 0:
        yield 0
        return
    mask = (1 << weight) - 1
    limit = 1 << vertex_count
    while mask < limit:
        yield mask
        lowest = mask & -mask
        ripple = mask + lowest
        mask = ripple | (((ripple ^ mask) >> 2) // lowest)


@dataclass(frozen=True)
class PrefixCertificate:
    n: int
    width_limit: int
    layer_counts: tuple[int, ...]
    first_empty_size: int | None
    replay_digest_sha256: str

    @property
    def excludes_layout(self) -> bool:
        return self.first_empty_size is not None

    def as_dict(self) -> dict[str, object]:
        return {
            "graph": f"P({self.n},3)",
            "width_limit": self.width_limit,
            "layer_counts": list(self.layer_counts),
            "first_empty_size": self.first_empty_size,
            "excludes_vertex_separation_at_most_seven": self.excludes_layout,
            "replay_digest_sha256": self.replay_digest_sha256,
        }


def _record_layer(
    digest: hashlib._Hash,
    size: int,
    states: set[int],
    byte_width: int,
) -> None:
    layer_digest = hashlib.sha256()
    for state in sorted(states):
        layer_digest.update(state.to_bytes(byte_width, "little"))
    digest.update(size.to_bytes(2, "little"))
    digest.update(len(states).to_bytes(8, "little"))
    digest.update(layer_digest.digest())


def certify_no_narrow_layout(n: int, width_limit: int = 7) -> PrefixCertificate:
    """Enumerate exactly the prefixes reachable in a layout of the given width."""
    if n < 7:
        raise ValueError("P(n,3) requires n at least seven")
    vertex_count = 2 * n
    if not 0 <= width_limit < vertex_count:
        raise ValueError("invalid width limit")
    counts = [math.comb(vertex_count, size) for size in range(width_limit + 1)]
    digest = hashlib.sha256(f"P({n},3)|limit={width_limit}".encode())
    for size, count in enumerate(counts):
        digest.update(f"|formula:{size}:{count}".encode())

    size = width_limit + 1
    states = {
        mask
        for mask in fixed_weight_masks(vertex_count, size)
        if boundary_size(n, mask) <= width_limit
    }
    byte_width = (vertex_count + 7) // 8
    _record_layer(digest, size, states, byte_width)
    counts.append(len(states))

    full_mask = (1 << vertex_count) - 1
    while states and size < vertex_count:
        size += 1
        next_states: set[int] = set()
        for state in states:
            remaining = full_mask ^ state
            while remaining:
                vertex_bit = remaining & -remaining
                remaining -= vertex_bit
                candidate = state | vertex_bit
                if boundary_size(n, candidate) <= width_limit:
                    next_states.add(candidate)
        states = next_states
        _record_layer(digest, size, states, byte_width)
        counts.append(len(states))

    first_empty = size if not states else None
    return PrefixCertificate(
        n=n,
        width_limit=width_limit,
        layer_counts=tuple(counts),
        first_empty_size=first_empty,
        replay_digest_sha256=digest.hexdigest(),
    )
