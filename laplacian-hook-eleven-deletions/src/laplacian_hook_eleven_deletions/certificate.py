"""Build the complete eleven-deletion exceptional-hook certificate."""

from hashlib import sha256

from laplacian_hook_eleven_deletions.audit import boundary_audit, stable_audit
from laplacian_hook_eleven_deletions.census import (
    augmentation_census,
    burnside_census,
    format_graph_key,
)
from laplacian_hook_eleven_deletions.character import (
    character_ratios,
    expected_character_ratios,
)

EXPECTED_STABLE_COUNTS = (1, 1, 2, 5, 11, 26, 68, 177, 497, 1476, 4613, 15216)
EXPECTED_STABLE_HISTOGRAM = (
    116415929,
    119623258,
    7417312,
    530662,
    50841,
    1251,
    23,
    2,
)
EXPECTED_BOUNDARY_COUNTS = {
    9: (1, 1, 2, 5, 11, 25, 63, 148, 345, 771, 1637, 3252),
    11: (1, 1, 2, 5, 11, 26, 67, 172, 467, 1305, 3664, 10250),
    13: (1, 1, 2, 5, 11, 26, 68, 176, 492, 1446, 4435, 14140),
    15: (1, 1, 2, 5, 11, 26, 68, 177, 496, 1471, 4583, 15036),
    17: (1, 1, 2, 5, 11, 26, 68, 177, 497, 1475, 4608, 15186),
    19: (1, 1, 2, 5, 11, 26, 68, 177, 497, 1476, 4612, 15211),
    21: (1, 1, 2, 5, 11, 26, 68, 177, 497, 1476, 4613, 15215),
}
EXPECTED_BOUNDARY_HISTOGRAMS = {
    9: (12602366, 6322656, 603367, 62421, 5417, 672, 31, 0),
    11: (67314715, 55443564, 4370566, 364290, 34511, 773, 15, 1),
    13: (105393288, 103410165, 7002602, 515355, 49344, 1218, 27, 4),
    15: (114535653, 116779545, 7393430, 529942, 50781, 1250, 23, 2),
    17: (116101787, 119143380, 7416320, 530942, 50890, 1220, 55, 2),
    19: (116364069, 119542586, 7417308, 530661, 50642, 1450, 23, 2),
    21: (116409052, 119608043, 7417312, 530662, 50841, 1251, 23, 2),
}


def _character_certificate() -> dict[str, object]:
    lines: list[str] = []
    checked_orders = list(range(9, 64, 2))
    for order in checked_orders:
        actual = character_ratios(order)
        if actual != expected_character_ratios(order):
            raise AssertionError(f"character ratio failed at n={order}")
        lines.append(f"{order}|" + "|".join(f"{key}:{value}" for key, value in actual.items()))
    return {
        "checked_odd_orders": checked_orders,
        "q6_ratios": {
            "four_chi(3,3)/D": "(n^2-12n+59)/[4(n-4)(n-2)]",
            "two_chi(4,2)/D": "-(n-7)/[(n-4)(n-2)]",
            "chi(6)/D": "0",
            "chi(2,2,2)/D": "0",
        },
        "q7_ratios": {
            "two_chi(7)/D": "(n-13)(n-11)(n-9)/[32(n-6)(n-4)(n-2)]",
            "two_chi(3,2,2)/D": "-(n-13)/[2(n-4)(n-2)]",
            "two_chi(4,3)/D": "0",
            "two_chi(5,2)/D": "0",
        },
        "q8_ratios": {
            "chi(8)/D": "0",
            "chi(6,2)/D": "-3(n-9)(n-11)/[16(n-6)(n-4)(n-2)]",
            "chi(5,3)/D": "(n-9)(n^2-16n+135)/[64(n-6)(n-4)(n-2)]",
            "chi(4,4)/D": "-(n^2-16n+75)/[4(n-6)(n-4)(n-2)]",
            "chi(4,2,2)/D": "0",
            "chi(3,3,2)/D": "0",
            "chi(2,2,2,2)/D": "3/[(n-4)(n-2)]",
        },
        "sample_sha256": sha256("\n".join(lines).encode()).hexdigest(),
    }


def build_certificate() -> dict[str, object]:
    census = augmentation_census()
    counts = tuple(len(level) for level in census)
    if counts != EXPECTED_STABLE_COUNTS or burnside_census() != EXPECTED_STABLE_COUNTS:
        raise AssertionError("stable censuses disagree")

    stable = stable_audit()
    if (
        stable.histogram != EXPECTED_STABLE_HISTOGRAM
        or stable.identity_group_count != 854
        or len(stable.q6_pairs) != 1251
        or len(stable.q7_pairs) != 23
        or len(stable.q8_pairs) != 2
        or len(stable.specializations) != 311
    ):
        raise AssertionError("unexpected stable audit")

    orders = (9, 11, 13, 15, 17, 19, 21)
    boundaries = [boundary_audit(order) for order in orders]
    for boundary in boundaries:
        if (
            boundary.counts != EXPECTED_BOUNDARY_COUNTS[boundary.order]
            or boundary.histogram != EXPECTED_BOUNDARY_HISTOGRAMS[boundary.order]
        ):
            raise AssertionError(f"unexpected boundary audit at n={boundary.order}")
        for index in (7, 8):
            count = sum(pair.first_index == index for pair in boundary.deep_pairs)
            if count != EXPECTED_BOUNDARY_HISTOGRAMS[boundary.order][index - 1]:
                raise AssertionError(f"unexpected q{index} residual pattern at n={boundary.order}")

    return {
        "theorem": (
            "For every odd n>=9, the exceptional self-conjugate hook polynomial "
            "determines every K_n-H with at most eleven deleted edges."
        ),
        "stable_reference_order": 23,
        "stable_deletion_class_counts": list(counts),
        "stable_class_count": sum(counts),
        "max_active_support": 22,
        "canonicalization": "pynauty component canonical labels",
        "complement_keys_by_deletion_count": [
            [format_graph_key(key) for key in sorted(level)] for level in census
        ],
        "character_certificate": _character_certificate(),
        "stable_symbolic_audit": stable.as_json(),
        "boundary_audits": [boundary.as_json() for boundary in boundaries],
    }
