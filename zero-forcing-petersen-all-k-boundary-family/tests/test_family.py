import pytest

from zero_forcing_petersen_all_k_boundary_family.family import block, replay, word


def test_symbolic_blocks_and_replays() -> None:
    for k in range(3, 21):
        columns = block(k)
        assert len(columns) == k
        assert sum(column.count("Y") for column in columns) == k
        assert sum(column.count("B") for column in columns) == 2
        for multiplier in range(3, 9):
            result = replay(k, multiplier)
            assert len(word(k, multiplier)) == result.selected_size == k * multiplier
            assert result.boundary_size == 2 * multiplier


def test_square_family_refutes_uniform_threshold() -> None:
    for k in range(6, 41):
        result = replay(k, k)
        assert result.n >= 6 * k - 1
        assert result.boundary_size == 2 * k < 2 * k + 2


def test_domain_checks() -> None:
    with pytest.raises(ValueError):
        block(2)
    with pytest.raises(ValueError):
        word(3, 2)
