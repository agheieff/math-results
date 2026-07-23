from decimal import Decimal, localcontext

PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
    "208998628034825342117067982148086513282306647093844609550582231725359408128"
)


def height_with_offset(base: Decimal, offset: Decimal, precision: int = 100) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        return +(base + offset)


def theta_over_pi(height: Decimal, precision: int = 90) -> Decimal:
    """Evaluate the Riemann--Siegel theta asymptotic divided by pi."""
    with localcontext() as context:
        context.prec = precision
        two = Decimal(2)
        theta = (
            height / two * (height / (two * PI)).ln()
            - height / two
            - PI / 8
            + 1 / (48 * height)
            + 7 / (5760 * height**3)
            + 31 / (80640 * height**5)
            + 127 / (430080 * height**7)
        )
        return +(theta / PI)


def distance_to_integer(value: Decimal) -> Decimal:
    floor = value // 1
    fraction = value - floor
    return min(fraction, 1 - fraction)
