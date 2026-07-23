from laplacian_hook_eleven_deletions.audit import boundary_audit, stable_audit


def test_stable_and_boundary_separation() -> None:
    stable = stable_audit()
    assert stable.histogram == (
        116415929,
        119623258,
        7417312,
        530662,
        50841,
        1251,
        23,
        2,
    )
    assert stable.identity_group_count == 854
    assert len(stable.q6_pairs) == 1251
    assert len(stable.q7_pairs) == 23
    assert len(stable.q8_pairs) == 2
    assert len(stable.specializations) == 311
    assert stable.signature_sha256 == (
        "11994fe61d39d0ecc9c1b3b5656342a8f1ad79ac3851cd994e8747f4e1aa8469"
    )
    assert {pair.polynomial for pair in stable.q8_pairs} == {
        (-96, -2432, -21216, -63040),
        (-72, -1936, -17400, -52016),
    }
    assert {item.order for item in stable.specializations} == {23, 29, 41, 77}
    assert all(
        item.first_index == 4 and item.separating_index == 5 and item.separating_difference
        for item in stable.specializations
    )

    expected_histograms = {
        9: (12602366, 6322656, 603367, 62421, 5417, 672, 31, 0),
        11: (67314715, 55443564, 4370566, 364290, 34511, 773, 15, 1),
        13: (105393288, 103410165, 7002602, 515355, 49344, 1218, 27, 4),
        15: (114535653, 116779545, 7393430, 529942, 50781, 1250, 23, 2),
        17: (116101787, 119143380, 7416320, 530942, 50890, 1220, 55, 2),
        19: (116364069, 119542586, 7417308, 530661, 50642, 1450, 23, 2),
        21: (116409052, 119608043, 7417312, 530662, 50841, 1251, 23, 2),
    }
    expected_digests = {
        9: "ebad800b3213dfcfc370e0a69979ee059c5ae79d985a71b17358450cb20b9bc9",
        11: "be731cc2e90249f716ee7806d0e42165d7062b58cfc9d180384e1fcf8e8b18d5",
        13: "92ac2c4e3109c19ef0f4662cf9fcc922b3a9df594e601d53fe2d486623732e0a",
        15: "f5f425732f0e0fffdcf550bd8080672ba6201f6fe7e146aa4d0a3644047ce1be",
        17: "7840211f5c2ca0ba0020768d00a4b08e64362964e9b5dc35ab105683582be87b",
        19: "ede3654e13db7abc44b8146f38946618df5a7492ec2a7afa7e6ceeba82da5d03",
        21: "f83b4bd6d4127d5137ca8e2f0d171e3a0e5fb6089cfbf575d6d5fa674f3a04bd",
    }
    boundaries = {order: boundary_audit(order) for order in expected_histograms}
    assert {
        order: boundary.histogram for order, boundary in boundaries.items()
    } == expected_histograms
    assert {
        order: boundary.signature_sha256 for order, boundary in boundaries.items()
    } == expected_digests
    assert all(pair.difference for boundary in boundaries.values() for pair in boundary.deep_pairs)
