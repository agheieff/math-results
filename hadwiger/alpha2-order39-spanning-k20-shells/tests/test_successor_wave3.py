from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    THIRD_SUCCESSOR_NEW_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.successor_wave3 import (
    EXPECTED_CENTER_COUNTS,
    enumerate_third_successors,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import support_system_valid


def test_third_successor_shells_are_complete() -> None:
    shells, hall_union, new_states = enumerate_third_successors()
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )

    assert counts == EXPECTED_CENTER_COUNTS
    assert len(hall_union) == 13
    assert new_states == THIRD_SUCCESSOR_NEW_SUPPORTS


def test_third_successors_pass_exact_support_conditions() -> None:
    assert all(support_system_valid(state) for state in THIRD_SUCCESSOR_NEW_SUPPORTS)
