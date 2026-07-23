"""Exact characteristic-polynomial, target-algebra, and Sturm checks."""

from fractions import Fraction

from signed_circulant_n22.model import Matrix

Polynomial = tuple[int, ...]  # Descending coefficients.
RationalPolynomial = tuple[Fraction, ...]

U_MINIMAL_POLYNOMIAL: Polynomial = (1, -1, -4, 3, 3, -1)
TARGET_SQUARE_POLYNOMIAL: Polynomial = (1, -20, 149, -519, 851, -529)
TARGET_POLYNOMIAL: Polynomial = (1, 0, -20, 0, 149, 0, -519, 0, 851, 0, -529)
SEPARATOR_NUMERATOR = 3801
SEPARATOR_DENOMINATOR = 500


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


def polyadd(left: Polynomial, right: Polynomial) -> Polynomial:
    size = max(len(left), len(right))
    padded_left = (0,) * (size - len(left)) + left
    padded_right = (0,) * (size - len(right)) + right
    result = tuple(a + b for a, b in zip(padded_left, padded_right, strict=True))
    first = next((i for i, value in enumerate(result) if value), len(result) - 1)
    return result[first:]


def compose(outer: Polynomial, inner: Polynomial) -> Polynomial:
    result: Polynomial = (0,)
    for coefficient in outer:
        result = polyadd(polymul(result, inner), (coefficient,))
    return result


def expected_extremal_polynomial() -> Polynomial:
    return polymul((1, 0, -4), polymul(TARGET_POLYNOMIAL, TARGET_POLYNOMIAL))


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


def verify_target_algebra() -> None:
    """Verify the cyclotomic elimination and exact separator."""
    # For u=2*cos(pi/11), S_11(u)+2=(u+2)*m(u)^2=0.
    twice_cos_eleven_plus_two: Polynomial = (
        1,
        0,
        -11,
        0,
        44,
        0,
        -77,
        0,
        55,
        0,
        -11,
        2,
    )
    if (
        polymul((1, 2), polymul(U_MINIMAL_POLYNOMIAL, U_MINIMAL_POLYNOMIAL))
        != twice_cos_eleven_plus_two
    ):
        raise AssertionError("twice-cosine polynomial identity failed")

    # alpha=u^2+u+2 and p(alpha)=m(u)*(u^5+6u^4+10u^3+u^2-6u-1).
    elimination_quotient: Polynomial = (1, 6, 10, 1, -6, -1)
    if compose(TARGET_SQUARE_POLYNOMIAL, (1, 1, 2)) != polymul(
        U_MINIMAL_POLYNOMIAL, elimination_quotient
    ):
        raise AssertionError("target elimination identity failed")

    # pi/11<pi/8 gives u>sqrt(2+sqrt(2))>9/5, hence alpha>176/25>7.
    if not (
        Fraction(31, 25) ** 2 < 2
        and 2 + Fraction(31, 25) == Fraction(9, 5) ** 2
        and Fraction(9, 5) ** 2 + Fraction(9, 5) + 2 == Fraction(176, 25)
        and Fraction(176, 25) > 7
    ):
        raise AssertionError("rational target lower bound failed")

    intervals = (
        (Fraction(9, 5), Fraction(19, 10)),
        (Fraction(23, 10), Fraction(12, 5)),
        (Fraction(31, 10), Fraction(16, 5)),
        (Fraction(5), Fraction(51, 10)),
        (Fraction(38, 5), Fraction(SEPARATOR_NUMERATOR, SEPARATOR_DENOMINATOR)),
    )
    if any(roots_between(left, right) != 1 for left, right in intervals):
        raise AssertionError("target square polynomial root isolation failed")
