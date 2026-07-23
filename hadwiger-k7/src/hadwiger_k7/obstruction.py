from hadwiger_k7.graph import Graph

# Vertices are the cells of a 3 x 3 board, numbered 3r + c. Two cells are
# adjacent exactly when they share a row or a column: this is L(K_{3,3}).
ROOK_EDGES = frozenset(
    {
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 6),
        (1, 2),
        (1, 4),
        (1, 7),
        (2, 5),
        (2, 8),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 5),
        (4, 7),
        (5, 8),
        (6, 7),
        (6, 8),
        (7, 8),
    }
)

EXPECTED_ROOK_SHA256 = "18c6d8aae8f72705038b0ebd16e17e0ae423c9eda2e66e475c5c8c5e7ed469bd"


def rook_graph() -> Graph:
    return Graph(order=9, edges=ROOK_EDGES)
