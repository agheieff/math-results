from hadwiger_alpha2_order39_spanning_k20_search.labeled_catchup import (
    EXPECTED_CENTER_COUNTS,
    NEW_STATES_SHA256,
    _support_hash,
    enumerate_labeled_catchup,
)


def test_labeled_catchup_shells_are_complete() -> None:
    centers, shells, hall_union, new_states = enumerate_labeled_catchup()
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )

    assert len(centers) == 23
    assert counts == EXPECTED_CENTER_COUNTS
    assert len(hall_union) == 99
    assert len(new_states) == 74
    assert _support_hash(new_states) == NEW_STATES_SHA256
