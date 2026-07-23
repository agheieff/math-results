"""Exact characteristic-polynomial and polynomial arithmetic."""

from laplacian_hook_six_refutation.model import Matrix, Polynomial


def matmul(left: Matrix, right: Matrix) -> Matrix:
    order = len(left)
    return tuple(
        tuple(
            sum(left[row][index] * right[index][column] for index in range(order))
            for column in range(order)
        )
        for row in range(order)
    )


def identity(order: int) -> Matrix:
    return tuple(tuple(int(row == column) for column in range(order)) for row in range(order))


def characteristic_polynomial(matrix: Matrix) -> Polynomial:
    """Compute det(xI-M) from traces and Newton identities."""
    order = len(matrix)
    if any(len(row) != order for row in matrix):
        raise ValueError("matrix must be square")
    power = identity(order)
    traces = [0]
    for _ in range(order):
        power = matmul(power, matrix)
        traces.append(sum(power[index][index] for index in range(order)))

    coefficients = [1]
    for degree in range(1, order + 1):
        numerator = -sum(
            coefficients[degree - power_index] * traces[power_index]
            for power_index in range(1, degree + 1)
        )
        quotient, remainder = divmod(numerator, degree)
        if remainder:
            raise ArithmeticError("Newton coefficient was not integral")
        coefficients.append(quotient)
    return tuple(coefficients)


def polynomial_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)


def polynomial_power(polynomial: Polynomial, exponent: int) -> Polynomial:
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    result: Polynomial = (1,)
    for _ in range(exponent):
        result = polynomial_multiply(result, polynomial)
    return result


def polynomial_product(factors: tuple[Polynomial, ...]) -> Polynomial:
    result: Polynomial = (1,)
    for factor in factors:
        result = polynomial_multiply(result, factor)
    return result


def pad_sparse_polynomial(nonzero_factor: Polynomial, order: int) -> Polynomial:
    degree = len(nonzero_factor) - 1
    if order < degree:
        raise ValueError("order is below the nonzero factor degree")
    return (*nonzero_factor, *(0 for _ in range(order - degree)))


def complement_nonzero_factor(nonzero_factor: Polynomial, order: int) -> Polynomial:
    """Return prod_mu (x-order+mu) from prod_mu(t-mu)."""
    degree = len(nonzero_factor) - 1
    result = [0] * (degree + 1)
    sign = (-1) ** degree
    base: Polynomial = (-1, order)  # order - x
    for index, coefficient in enumerate(nonzero_factor):
        power = degree - index
        term = polynomial_power(base, power)
        offset = degree - power
        for term_index, value in enumerate(term):
            result[offset + term_index] += sign * coefficient * value
    return tuple(result)


def complement_polynomial_from_sparse(nonzero_factor: Polynomial, order: int) -> Polynomial:
    """Use L(complement)=nI-J-L to transform a five-root sparse factor."""
    if len(nonzero_factor) != 6 or order < 6:
        raise ValueError("expected a degree-five nonzero sparse factor and order at least six")
    return polynomial_product(
        (
            (1, 0),
            polynomial_power((1, -order), order - 6),
            complement_nonzero_factor(nonzero_factor, order),
        )
    )
