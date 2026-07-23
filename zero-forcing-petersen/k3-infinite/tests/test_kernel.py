from fractions import Fraction

from zero_forcing_petersen_infinite.kernel import (
    BASIS,
    adjacency_residual,
    null_vector_for,
    solution_value,
)
from zero_forcing_petersen_infinite.model import inner, outer


def test_eight_dimensional_symbolic_kernel() -> None:
    for basis in BASIS:
        for index in range(-40, 41):
            assert adjacency_residual(basis, outer(index)) == 0
            assert adjacency_residual(basis, inner(index)) == 0


def test_exact_witness_for_arbitrary_seven_constraints() -> None:
    vertices = (outer(-11), inner(-7), outer(-2), inner(0), outer(6), inner(13), outer(29))
    witness = null_vector_for(vertices)
    assert witness != (Fraction(0),) * 8
    assert all(solution_value(witness, vertex) == 0 for vertex in vertices)
