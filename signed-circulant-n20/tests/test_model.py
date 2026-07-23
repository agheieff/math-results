from signed_circulant.model import (
    CLASS_BITS,
    CLASS_COUNT,
    EDGES,
    TARGET_MASKS,
    N,
    hamilton_holonomy,
    is_alternating,
    mask_from_normalized_signing,
    normalize_signing,
    signing_from_mask,
    switch_signing,
    triangle_fluxes,
)


def test_graph_and_class_count() -> None:
    assert len(EDGES) == 40
    assert len(set(frozenset(edge) for edge in EDGES)) == 40
    assert CLASS_BITS == 21
    assert CLASS_COUNT == 2_097_152


def test_gauge_is_unique_and_switch_invariant() -> None:
    mask = 0x12345
    signing = signing_from_mask(mask)
    switches = tuple(-1 if (i * i + 3 * i + 1) % 5 < 2 else 1 for i in range(N))
    switched = switch_signing(signing, switches)
    assert mask_from_normalized_signing(normalize_signing(switched)) == mask


def test_twisted_classes() -> None:
    assert TARGET_MASKS == (873_813, 1_223_339)
    for mask in TARGET_MASKS:
        assert hamilton_holonomy(mask) == -1
        assert is_alternating(triangle_fluxes(mask))
