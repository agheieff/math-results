from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SEVENTH_SUCCESSOR_NEW_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.successor_wave7 import (
    EXPECTED_CENTER_COUNTS,
    enumerate_seventh_successors,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import support_system_valid


def test_seventh_successor_shells_are_complete() -> None:
    shells, hall_union, new_states = enumerate_seventh_successors()
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )

    assert counts == EXPECTED_CENTER_COUNTS
    assert len(hall_union) == 15
    assert new_states == SEVENTH_SUCCESSOR_NEW_SUPPORTS


def test_seventh_successors_pass_exact_support_conditions() -> None:
    assert all(support_system_valid(state) for state in SEVENTH_SUCCESSOR_NEW_SUPPORTS)
