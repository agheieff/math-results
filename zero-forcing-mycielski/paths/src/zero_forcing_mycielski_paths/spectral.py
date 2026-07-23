from math import cos, pi, sin


def path_eigenvalue(order: int, index: int) -> float:
    return 2.0 * cos(index * pi / (order + 1))


def spectral_parameters(order: int) -> tuple[float, float, float, float]:
    if order < 4 or order == 5:
        raise ValueError("generic certificate requires n>=4 and n!=5")
    r = path_eigenvalue(order, 2)
    s = path_eigenvalue(order, 4)
    return r, s, -r * s, r + s


def even_mode_sum(order: int, index: int) -> float:
    return sum(sin(index * (vertex + 1) * pi / (order + 1)) for vertex in range(order))


def verify_spectral_parameters(order: int) -> None:
    r, s, a, b = spectral_parameters(order)
    if abs(b) < 1e-10:
        raise AssertionError("path-edge coefficient vanished")
    eigenvalues = [path_eigenvalue(order, index) for index in range(1, order + 1)]
    roots = [value for value in eigenvalues if abs(a + b * value - value * value) < 1e-9]
    if len(roots) != 2 or abs(roots[0] - r) > 1e-9 or abs(roots[1] - s) > 1e-9:
        raise AssertionError("wrong singular modes")
    if abs(even_mode_sum(order, 2)) > 1e-9 or abs(even_mode_sum(order, 4)) > 1e-9:
        raise AssertionError("selected modes are not apex-orthogonal")
