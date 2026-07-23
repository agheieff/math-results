from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    FOURTH_SUCCESSOR_NEW_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.successor_wave4 import (
    EXPECTED_CENTER_COUNTS,
    enumerate_fourth_successors,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import support_system_valid


def test_fourth_successor_shells_are_complete() -> None:
    shells, hall_union, new_states = enumerate_fourth_successors()
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )

    assert counts == EXPECTED_CENTER_COUNTS
    assert len(hall_union) == 11
    assert new_states == FOURTH_SUCCESSOR_NEW_SUPPORTS


def test_fourth_successors_pass_exact_support_conditions() -> None:
    assert all(support_system_valid(state) for state in FOURTH_SUCCESSOR_NEW_SUPPORTS)
