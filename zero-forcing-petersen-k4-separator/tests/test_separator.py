from zero_forcing_petersen_k4_separator.automaton import build_automaton
from zero_forcing_petersen_k4_separator.certificate import N22_WORD, N23_WORD
from zero_forcing_petersen_k4_separator.model import (
    Color,
    is_balanced,
    parse_coloring,
    pump_down,
    separator_size,
)


def test_automaton_dimensions() -> None:
    automaton = build_automaton()
    assert len(automaton.states) == 1_481
    assert len(automaton.transitions) == 7_383


def test_threshold_witnesses() -> None:
    n22 = parse_coloring(N22_WORD)
    n23 = parse_coloring(N23_WORD)
    assert is_balanced(n22)
    assert separator_size(n22) == 9
    assert is_balanced(n23)
    assert separator_size(n23) == 10


def test_paired_clean_run_deletion() -> None:
    coloring = (
        ((Color.B, Color.B),)
        + ((Color.A, Color.B),) * 3
        + ((Color.A, Color.A),) * 32
        + ((Color.A, Color.B),) * 3
        + ((Color.B, Color.B),)
        + ((Color.Y, Color.Y),) * 40
    )
    assert is_balanced(coloring)
    reduced = pump_down(coloring)
    assert len(reduced) == 78
    assert is_balanced(reduced)
    assert separator_size(reduced) == 10
