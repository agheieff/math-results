import hashlib
import math
from collections.abc import Iterator

from zero_forcing_petersen_k4.census import run_census
from zero_forcing_petersen_k4.graph import GeneralizedPetersen, closure

EXPECTED = {
    17: (
        3_085_368,
        48_100,
        17_045_749_760,
        "33263f8e1a983f57f05f9662b7a5bed6241469a01d1a46cc5e407a65614bfc21",
    ),
    18: (
        5_230_208,
        0,
        0,
        "2808d8f325a9ff5c71e176124b299a76bae128a15c6a2b6680c392229c984249",
    ),
    19: (
        8_579_560,
        0,
        0,
        "ba8ed889b61dc25b0215e1a5452bd5d9ed14f6fea7b955f8a5a0be72a95fc8b3",
    ),
    20: (
        13_671_944,
        0,
        0,
        "daa728023f3b4ef3755b89beb9375db55a03e1d6c5984404e244d6c95b004aa8",
    ),
    21: (
        21_232_978,
        0,
        0,
        "4749b3e860792ece995bb830d3e8be055b282dca12240ded4c3e55d97fb8c37a",
    ),
    22: (
        32_224_114,
        0,
        0,
        "77a397cbf1b05b17ab4285429449ab010d70146097a1d6cef88d4cf5608ea646",
    ),
}


def _rotation_orbit_count(n: int, size: int) -> int:
    fixed_total = 0
    for shift in range(n):
        cycles_per_layer = math.gcd(n, shift)
        cycle_length = n // cycles_per_layer
        if size % cycle_length == 0:
            fixed_total += math.comb(2 * cycles_per_layer, size // cycle_length)
    count, remainder = divmod(fixed_total, n)
    assert remainder == 0
    return count


def _reference_necklaces(n: int, size: int) -> Iterator[int]:
    symbol_weight = (0, 1, 1, 2)
    word = [0] * (n + 1)

    def generate(position: int, period: int, weight: int) -> Iterator[int]:
        if weight > size or weight + 2 * (n - position + 1) < size:
            return
        if position > n:
            if n % period == 0 and weight == size:
                mask = 0
                for index, symbol in enumerate(word[1:]):
                    if symbol & 1:
                        mask |= 1 << index
                    if symbol & 2:
                        mask |= 1 << (n + index)
                yield mask
            return

        copied = word[position - period]
        word[position] = copied
        yield from generate(position + 1, period, weight + symbol_weight[copied])
        for symbol in range(copied + 1, 4):
            word[position] = symbol
            yield from generate(position + 1, position, weight + symbol_weight[symbol])

    yield from generate(1, 1, 0)


def _reference_n9() -> tuple[int, int, int, str]:
    n = 9
    graph = GeneralizedPetersen(n)
    digest = hashlib.sha256(bytes((ord("P"), ord("4"), ord("Z"), ord("9"), n, 0, 9, 0)))
    tested = 0
    forcing = 0
    first_witness = 0
    for mask in _reference_necklaces(n, 9):
        closed = closure(graph, mask)
        digest.update(mask.to_bytes(8, "little"))
        digest.update(closed.to_bytes(8, "little"))
        tested += 1
        if closed == graph.full_mask:
            forcing += 1
            if first_witness == 0:
                first_witness = mask
    return tested, forcing, first_witness, digest.hexdigest()


def test_exact_cyclic_orbit_census() -> None:
    n9, *results = run_census((9, *EXPECTED))
    assert (
        n9.necklaces,
        n9.forcing_necklaces,
        n9.first_witness,
        n9.replay_digest_sha256,
    ) == _reference_n9()

    for result in results:
        assert (
            result.necklaces,
            result.forcing_necklaces,
            result.first_witness,
            result.replay_digest_sha256,
        ) == EXPECTED[result.n]
        assert result.necklaces == _rotation_orbit_count(result.n, 9)

    control = results[0]
    assert closure(GeneralizedPetersen(17), control.first_witness) == (1 << 34) - 1
