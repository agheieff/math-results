from __future__ import annotations

import hashlib
from itertools import combinations
from pathlib import Path

import pytest
from pysat.solvers import Solver  # type: ignore[import-untyped]

from union_closed_tight_m20.encoding import (
    TARGET,
    Parameters,
    build_cnf,
    family_variable,
)
from union_closed_tight_m20.semantics import (
    element_frequencies,
    is_canonical_clean_tight,
)


def test_public_target_is_exactly_order_eight_m20() -> None:
    assert Parameters(order=8, member_count=20) == TARGET


def test_target_cnf_fingerprint(tmp_path: Path) -> None:
    formula = build_cnf()
    path = tmp_path / "target.cnf"
    formula.to_file(path)
    assert (formula.nv, len(formula.clauses)) == (17_792, 231_118)
    assert (
        hashlib.sha256(path.read_bytes()).hexdigest()
        == "bf3bf0267d86d737cb40b45ad6d0b5bb2bd68e3c18f3c1c46e3f451e9767c300"
    )


@pytest.mark.parametrize("member_count", range(2, 9))
def test_cnf_matches_direct_predicate_on_every_order_three_family(
    member_count: int,
) -> None:
    parameters = Parameters(order=3, member_count=member_count)
    formula = build_cnf(parameters)
    with Solver(name="cadical195", bootstrap_with=formula) as solver:
        for chosen in combinations(range(parameters.subset_count), member_count):
            family = set(chosen)
            assumptions = [
                family_variable(mask) if mask in family else -family_variable(mask)
                for mask in range(parameters.subset_count)
            ]
            assert solver.solve(assumptions=assumptions) is is_canonical_clean_tight(
                parameters.order,
                parameters.member_count,
                family,
            )


def test_order_four_power_set_hits_the_m16_boundary() -> None:
    parameters = Parameters(order=4, member_count=16)
    family = set(range(16))
    assert is_canonical_clean_tight(parameters.order, parameters.member_count, family)
    with Solver(name="cadical195", bootstrap_with=build_cnf(parameters)) as solver:
        assert solver.solve()


def test_direct_frequency_counts() -> None:
    assert element_frequencies(3, {0b000, 0b011, 0b101, 0b111}) == (3, 2, 2)


def test_direct_predicate_rejects_equal_incidence_columns() -> None:
    family = {0b000, 0b011, 0b100, 0b111}
    assert not is_canonical_clean_tight(3, 4, family)


@pytest.mark.parametrize("order,member_count", [(0, 2), (3, 1), (3, 9)])
def test_invalid_parameters_fail_fast(order: int, member_count: int) -> None:
    with pytest.raises(ValueError):
        build_cnf(Parameters(order, member_count))
