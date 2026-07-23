from __future__ import annotations

import unittest

from strong_seymour.tournament import maximum_matching
from strong_seymour.verify import has_complete_matching_exhaustive, verify_counterexample


class ExhaustiveMatchingTests(unittest.TestCase):
    def test_all_three_by_three_bipartite_graphs(self) -> None:
        left = (0, 1, 2)
        right = (3, 4, 5)
        for edge_mask in range(1 << 9):
            adjacency = [[0] * 6 for _ in range(6)]
            for source in left:
                for offset, target in enumerate(right):
                    bit = 3 * source + offset
                    adjacency[source][target] = (edge_mask >> bit) & 1
            exhaustive = has_complete_matching_exhaustive(adjacency, left, right)
            augmenting = len(maximum_matching(adjacency, left, right)) == 3
            self.assertEqual(exhaustive, augmenting, f"edge mask {edge_mask}")

    def test_rejects_cyclic_regular_tournament(self) -> None:
        order = 13
        adjacency = [
            [int(source != target and (target - source) % order <= 6) for target in range(order)]
            for source in range(order)
        ]
        certificate = {
            "format": "strong-seymour-tournament-v1",
            "order": order,
            "adjacency": adjacency,
        }
        with self.assertRaisesRegex(ValueError, "strong Seymour"):
            verify_counterexample(certificate)


if __name__ == "__main__":
    unittest.main()
