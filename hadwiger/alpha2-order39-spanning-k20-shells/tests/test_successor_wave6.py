from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SIXTH_SUCCESSOR_NEW_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.successor_wave6 import (
    EXPECTED_CENTER_COUNTS,
    enumerate_sixth_successors,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import support_system_valid


def test_sixth_successor_shells_are_complete() -> None:
    shells, hall_union, new_states = enumerate_sixth_successors()
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )

    assert counts == EXPECTED_CENTER_COUNTS
    assert len(hall_union) == 8
    assert new_states == SIXTH_SUCCESSOR_NEW_SUPPORTS


def test_sixth_successors_pass_exact_support_conditions() -> None:
    assert all(support_system_valid(state) for state in SIXTH_SUCCESSOR_NEW_SUPPORTS)
