from zero_forcing_petersen_all_orders.pathwidth import certify_no_narrow_layout


def test_target_pathwidth_lower_certificates() -> None:
    expected = {
        14: (17, "6923b68acc1945de1444a3193b18c3bc3c19920306a2e57699a696c766b1d2e4"),
        15: (17, "6477e534dd9c8ff0e32173613982ff781218441242e4f9d5e25efc97daf7548f"),
        16: (17, "cf9bae363b5e42f47ad4e867c42571d126c87500c08d0161d32939b2ab160013"),
    }
    for n, (first_empty, digest) in expected.items():
        certificate = certify_no_narrow_layout(n)
        assert certificate.first_empty_size == first_empty
        assert certificate.replay_digest_sha256 == digest
