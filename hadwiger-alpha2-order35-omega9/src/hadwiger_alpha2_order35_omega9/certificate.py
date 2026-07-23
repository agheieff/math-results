from __future__ import annotations

SUPPORT_TEXT = (
    "027",
    "014",
    "278",
    "357",
    "158",
    "156",
    "0367",
    "068",
    "0345",
    "1268",
    "025",
    "157",
    "178",
    "245",
    "134",
    "458",
    "368",
    "347",
    "013",
    "038",
    "248",
    "467",
    "127",
    "046",
    "256",
    "236",
)

SUPPORTS = tuple(sum(1 << int(point) for point in text) for text in SUPPORT_TEXT)

GRAPH6 = (
    "b??????gUOCLDQPKGqceA_ga[CBDCLG?@D?GOW@PW?ojA`GBKC?Cm?YBGLWE_G?"
    "ScGGI?gao_OUAA?rA?WEQIF?o@Ha?DM@cQ@c??"
)

K18_MODEL = (
    (0,),
    (1, 22),
    (2, 23),
    (3, 29),
    (4, 27),
    (5, 26),
    (6, 10),
    (7, 14),
    (8, 33),
    (9, 31),
    (11, 15),
    (12, 25),
    (13, 17),
    (16, 30),
    (18, 21),
    (19, 20),
    (24, 32),
    (28, 34),
)

ALTERNATE_K18_MODEL = (
    (32,),
    (0, 2),
    (1, 16),
    (3, 19),
    (4, 34),
    (5, 7),
    (6, 27),
    (8, 33),
    (9, 18),
    (10, 28),
    (11, 29),
    (12, 24),
    (13, 14),
    (15, 31),
    (17, 25),
    (20, 26),
    (21, 23),
    (22, 30),
)


def complement_adjacency() -> tuple[int, ...]:
    """Build the triangle-free complement F from the support certificate."""
    order = 35
    adjacency = [0] * order
    for vertex, support in enumerate(SUPPORTS, 9):
        for point in range(9):
            if support >> point & 1:
                adjacency[point] |= 1 << vertex
                adjacency[vertex] |= 1 << point

    for left, support_left in enumerate(SUPPORTS, 9):
        for right, support_right in enumerate(SUPPORTS, 9):
            if left < right and not support_left & support_right:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return tuple(adjacency)
