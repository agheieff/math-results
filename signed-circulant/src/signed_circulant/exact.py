"""Independent integer characteristic-polynomial and Sturm checks."""

from fractions import Fraction

from signed_circulant.model import Matrix

Polynomial = tuple[int, ...]  # Descending coefficients.
RationalPolynomial = tuple[Fraction, ...]

TARGET_SQUARE_POLYNOMIAL: Polynomial = (1, -18, 114, -302, 281)
TARGET_POLYNOMIAL: Polynomial = (1, 0, -18, 0, 114, 0, -302, 0, 281)


def matmul(left: Matrix, right: Matrix) -> Matrix:
    n = len(left)
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)) for i in range(n)
    )


def identity(n: int) -> Matrix:
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def characteristic_polynomial(matrix: Matrix) -> Polynomial:
    """Compute det(xI-A) from exact power traces and Newton identities."""
    n = len(matrix)
    power = identity(n)
    traces = [0]
    for _ in range(n):
        power = matmul(power, matrix)
        traces.append(sum(power[i][i] for i in range(n)))

    coefficients = [1]
    for k in range(1, n + 1):
        numerator = -sum(coefficients[k - i] * traces[i] for i in range(1, k + 1))
        quotient, remainder = divmod(numerator, k)
        if remainder:
            raise ArithmeticError("Newton coefficient was not integral")
        coefficients.append(quotient)
    return tuple(coefficients)


def polymul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return tuple(result)


def expected_extremal_polynomial() -> Polynomial:
    square_minus_two = (1, 0, -2)
    return polymul(
        polymul(square_minus_two, square_minus_two),
        polymul(TARGET_POLYNOMIAL, TARGET_POLYNOMIAL),
    )


def derivative(polynomial: RationalPolynomial) -> RationalPolynomial:
    degree = len(polynomial) - 1
    return tuple(coefficient * (degree - i) for i, coefficient in enumerate(polynomial[:-1]))


def polynomial_remainder(
    dividend: RationalPolynomial, divisor: RationalPolynomial
) -> RationalPolynomial:
    current = list(dividend)
    while len(current) >= len(divisor):
        factor = current[0] / divisor[0]
        for i, coefficient in enumerate(divisor):
            current[i] -= factor * coefficient
        while current and current[0] == 0:
            current.pop(0)
    return tuple(current)


def sturm_sequence(polynomial: RationalPolynomial) -> tuple[RationalPolynomial, ...]:
    sequence = [polynomial, derivative(polynomial)]
    while len(sequence[-1]) > 1:
        remainder = polynomial_remainder(sequence[-2], sequence[-1])
        if not remainder:
            raise ArithmeticError("target polynomial is not square-free")
        sequence.append(tuple(-coefficient for coefficient in remainder))
    return tuple(sequence)


STURM_SEQUENCE = sturm_sequence(
    tuple(Fraction(coefficient) for coefficient in TARGET_SQUARE_POLYNOMIAL)
)


def evaluate(coefficients: RationalPolynomial, value: Fraction) -> Fraction:
    result = Fraction()
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def variations(value: Fraction) -> int:
    signs = [
        1 if result > 0 else -1 for poly in STURM_SEQUENCE if (result := evaluate(poly, value))
    ]
    return sum(left != right for left, right in zip(signs, signs[1:], strict=False))


def roots_between(left: Fraction, right: Fraction) -> int:
    return variations(left) - variations(right)


def verify_target_isolation() -> None:
    """Verify the four squared roots and the rational separator 38/5."""
    intervals = ((2, 3), (3, 4), (4, 5), (7, 8))
    if any(roots_between(Fraction(a), Fraction(b)) != 1 for a, b in intervals):
        raise AssertionError("target square polynomial root isolation failed")
    if roots_between(Fraction(5), Fraction(7)) != 0:
        raise AssertionError("unexpected root between 5 and 7")

    # For alpha=(9+sqrt(5)+sqrt(10+2sqrt(5)))/2, eliminating sqrt(5)
    # gives [((2x-9)^2-5)^2 - 5(4x-16)^2] = 16*p(x).
    two_x_minus_nine = (4, -36, 76)  # (2x-9)^2 - 5
    four_x_minus_sixteen = (4, -16)
    eliminated = tuple(
        left - right
        for left, right in zip(
            polymul(two_x_minus_nine, two_x_minus_nine),
            (
                0,
                0,
                *tuple(5 * value for value in polymul(four_x_minus_sixteen, four_x_minus_sixteen)),
            ),
            strict=True,
        )
    )
    if eliminated != tuple(16 * coefficient for coefficient in TARGET_SQUARE_POLYNOMIAL):
        raise AssertionError("radical elimination identity failed")

    # 2<sqrt(5)<9/4 and 3<sqrt(10+2sqrt(5))<77/20, so
    # 7<alpha<151/20<38/5.
    if not (
        Fraction(2) ** 2 < 5 < Fraction(9, 4) ** 2
        and Fraction(3) ** 2 < 10 + 2 * Fraction(2)
        and 10 + 2 * Fraction(9, 4) < Fraction(77, 20) ** 2
        and Fraction(151, 20) < Fraction(38, 5)
    ):
        raise AssertionError("rational separator ordering failed")
