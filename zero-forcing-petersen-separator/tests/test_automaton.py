from zero_forcing_petersen_separator.automaton import (
    COLUMNS,
    automaton_digest,
    build_automaton,
    transfer_certificate,
)


def test_automaton_shape_and_digests() -> None:
    automaton = build_automaton()
    assert len(COLUMNS) == 7
    assert len(automaton.states) == 247
    assert len(automaton.transitions) == 1_233
    assert automaton_digest(automaton) == (
        "c0d865280febdcad27e27b87e57517654d5a863b6235a1ff0baf23dbf1e1bb8a"
    )


def test_exact_transfer_range() -> None:
    result = transfer_certificate()
    expected = {
        7: 5,
        8: 5,
        9: 5,
        10: 6,
        11: 6,
        12: 6,
        13: 7,
        14: 7,
        15: 7,
        16: 7,
    }
    assert {order: result.minimum_at(order) for order in expected} == expected
    assert all(result.minimum_at(order) is None for order in range(17, 99))
    assert result.accepting_state_digest_sha256 == (
        "a297c0de728646d4968ccc9773a26d45b5a76413368928a62083855f4d0021be"
    )
