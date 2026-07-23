from zero_forcing_petersen_infinite.model import inner, neighbors, outer


def test_strip_is_simple_cubic_and_symmetric() -> None:
    for index in range(-20, 21):
        for vertex in (outer(index), inner(index)):
            adjacent = neighbors(vertex)
            assert len(set(adjacent)) == 3
            assert all(vertex in neighbors(item) for item in adjacent)
