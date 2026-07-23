from __future__ import annotations

from itertools import combinations

import pytest
from pysat.solvers import Solver  # type: ignore[import-untyped]

from union_closed_tight.encoding import Instance, build_cnf, family_variable
from union_closed_tight.semantics import is_canonical_clean_tight


@pytest.mark.parametrize("member_count", range(2, 9))
def test_encoding_matches_exhaustive_semantics(member_count: int) -> None:
    order = 3
    subset_count = 1 << order
    cnf = build_cnf(Instance(order, member_count))
    with Solver(name="cadical195", bootstrap_with=cnf) as solver:
        for chosen in combinations(range(subset_count), member_count):
            members = set(chosen)
            assumptions = [
                family_variable(mask) if mask in members else -family_variable(mask)
                for mask in range(subset_count)
            ]
            assert solver.solve(assumptions=assumptions) == is_canonical_clean_tight(
                order,
                member_count,
                members,
            )


def test_full_power_set_is_admitted() -> None:
    instance = Instance(order=3, member_count=8)
    with Solver(name="cadical195", bootstrap_with=build_cnf(instance)) as solver:
        assert solver.solve()


@pytest.mark.parametrize("order,member_count", [(0, 2), (3, 1), (3, 9)])
def test_invalid_instance(order: int, member_count: int) -> None:
    with pytest.raises(ValueError):
        build_cnf(Instance(order, member_count))
