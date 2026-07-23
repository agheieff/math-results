from zero_forcing_petersen_all_orders.finite import (
    certify_seven_sets,
    eight_outer_vertices_force,
    replay_symbolic_upper_bound,
)


def test_exact_n13_lower_bound() -> None:
    certificate = certify_seven_sets(13)
    assert certificate.tested == 657_800
    assert certificate.forcing_sets == 0
    assert (
        certificate.replay_digest_sha256
        == "2659be2817727d701afa76d0d049bd4b21f5285b38b186962ab26613235bfd97"
    )


def test_uniform_upper_witness_on_large_replay_range() -> None:
    assert all(eight_outer_vertices_force(n) for n in range(13, 501))
    assert all(replay_symbolic_upper_bound(n) for n in range(13, 1_001))
