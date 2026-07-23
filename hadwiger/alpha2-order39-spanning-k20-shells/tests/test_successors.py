from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SUCCESSOR_NEW_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.successor_search import (
    EXPECTED_CENTER_COUNTS,
    enumerate_successors,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import support_system_valid


def test_five_successor_shells_are_complete() -> None:
    checkpoint = enumerate_successors()
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in checkpoint.shells
    )

    assert counts == EXPECTED_CENTER_COUNTS
    assert len(checkpoint.hall_union) == 13
    assert checkpoint.new_states == SUCCESSOR_NEW_SUPPORTS


def test_new_successor_supports_pass_exact_support_conditions() -> None:
    assert all(support_system_valid(state) for state in SUCCESSOR_NEW_SUPPORTS)
