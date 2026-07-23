import pytest

from latin_transversals.explicit import (
    common_entries,
    h_phase_one_transversal,
    h_phase_zero_transversal,
    h_witnesses,
    verify_h_transversal,
)


@pytest.mark.parametrize("k", [9, 11, 13, 15, 17, 19, 21, 25, 31, 33, 101, 999])
def test_phase_zero_formulas(k: int) -> None:
    for omitted in (0, 1, 2):
        assert verify_h_transversal(k, h_phase_zero_transversal(k, omitted), omitted)


@pytest.mark.parametrize("k", [9, 11, 13, 15, 17, 19, 21, 101, 999])
def test_phase_one_formula(k: int) -> None:
    assert verify_h_transversal(k, h_phase_one_transversal(k), 0)


@pytest.mark.parametrize("k", [9, 11, 13, 15, 17, 19, 21, 101, 999])
def test_four_witnesses_have_empty_intersection(k: int) -> None:
    assert not common_entries(k, h_witnesses(k))


def test_all_odd_k_through_999() -> None:
    for k in range(9, 1_000, 2):
        witnesses = h_witnesses(k)
        assert all(verify_h_transversal(k, witnesses[omitted], omitted) for omitted in (0, 1, 2))
        assert verify_h_transversal(k, witnesses[3], 0)
        assert not common_entries(k, witnesses)
