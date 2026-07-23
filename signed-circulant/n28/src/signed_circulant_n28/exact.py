"""Exact characteristic-polynomial, target-algebra, and Sturm checks."""

from fractions import Fraction

from signed_circulant_n28.model import Matrix

Polynomial = tuple[int, ...]  # Descending coefficients.
RationalPolynomial = tuple[Fraction, ...]

U_MINIMAL_POLYNOMIAL: Polynomial = (1, 0, -7, 0, 14, 0, -7)
TARGET_SQUARE_POLYNOMIAL: Polynomial = (1, -26, 270, -1434, 4111, -6030, 3529)
TARGET_POLYNOMIAL: Polynomial = (
    1,
    0,
    -26,
    0,
    270,
    0,
    -1434,
    0,
    4111,
    0,
    -6030,
    0,
    3529,
)
SEPARATOR_NUMERATOR = 969
SEPARATOR_DENOMINATOR = 125


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
    return polymul((1, 0, -4, 0, 4), polymul(TARGET_POLYNOMIAL, TARGET_POLYNOMIAL))


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
    # For u=2*cos(pi/14), S_14(u)+2=u^2*m(u)^2=0.
    twice_cos_fourteen_plus_two: Polynomial = (
        1,
        0,
        -14,
        0,
        77,
        0,
        -210,
        0,
        294,
        0,
        -196,
        0,
        49,
        0,
        0,
    )
    if (
        polymul((1, 0, 0), polymul(U_MINIMAL_POLYNOMIAL, U_MINIMAL_POLYNOMIAL))
        != twice_cos_fourteen_plus_two
    ):
        raise AssertionError("twice-cosine polynomial identity failed")
    if (
        any(coefficient % 7 for coefficient in U_MINIMAL_POLYNOMIAL[1:])
        or U_MINIMAL_POLYNOMIAL[-1] % 49 == 0
    ):
        raise AssertionError("twice-cosine Eisenstein check failed")

    # alpha=u^2+u+2 and p(alpha)=m(u)*(u^6+6u^5+8u^4-8u^3-13u^2+6u+1).
    elimination_quotient: Polynomial = (1, 6, 8, -8, -13, 6, 1)
    if compose(TARGET_SQUARE_POLYNOMIAL, (1, 1, 2)) != polymul(
        U_MINIMAL_POLYNOMIAL, elimination_quotient
    ):
        raise AssertionError("target elimination identity failed")

    shifted_target: Polynomial = (1, -14, 70, -154, 147, -42, -7)
    if compose(TARGET_SQUARE_POLYNOMIAL, (1, 2)) != shifted_target:
        raise AssertionError("shifted target identity failed")
    if any(coefficient % 7 for coefficient in shifted_target[1:]) or shifted_target[-1] % 49 == 0:
        raise AssertionError("target Eisenstein check failed")

    # pi/14<pi/8 gives u>sqrt(2+sqrt(2))>9/5, hence alpha>176/25>7.
    if not (
        Fraction(31, 25) ** 2 < 2
        and 2 + Fraction(31, 25) == Fraction(9, 5) ** 2
        and Fraction(9, 5) ** 2 + Fraction(9, 5) + 2 == Fraction(176, 25)
        and Fraction(176, 25) > 7
    ):
        raise AssertionError("rational target lower bound failed")

    intervals = (
        (Fraction(9, 5), Fraction(19, 10)),
        (Fraction(14, 5), Fraction(29, 10)),
        (Fraction(18, 5), Fraction(37, 10)),
        (Fraction(19, 5), Fraction(39, 10)),
        (Fraction(6), Fraction(61, 10)),
        (Fraction(7), Fraction(SEPARATOR_NUMERATOR, SEPARATOR_DENOMINATOR)),
    )
    if any(roots_between(left, right) != 1 for left, right in intervals):
        raise AssertionError("target square polynomial root isolation failed")
