from __future__ import annotations

SUPPORT_HEX = (
    "015",
    "015",
    "023",
    "036",
    "038",
    "049",
    "04a",
    "052",
    "064",
    "0a8",
    "0b0",
    "0d0",
    "10e",
    "121",
    "141",
    "160",
    "186",
    "18a",
    "18c",
    "203",
    "209",
    "218",
    "224",
    "244",
    "281",
    "2c0",
    "310",
    "382",
)
SUPPORTS = tuple(int(text, 16) for text in SUPPORT_HEX)

ONE_DEFECT_HEX = (
    "00d",
    "015",
    "023",
    "029",
    "032",
    "04a",
    "052",
    "058",
    "064",
    "091",
    "0a8",
    "0d0",
    "10e",
    "121",
    "141",
    "160",
    "186",
    "18a",
    "18c",
    "203",
    "218",
    "230",
    "244",
    "244",
    "281",
    "2a4",
    "310",
    "382",
)
ONE_DEFECT = tuple(int(text, 16) for text in ONE_DEFECT_HEX)

# Each entry replaces the first pair by the second pair. Every replacement
# preserves both support sizes and all ten coordinate degrees.
SWITCH_PATH = (
    ((0x18C, 0x382), (0x186, 0x388)),
    ((0x032, 0x2A4), (0x0B0, 0x226)),
    ((0x091, 0x244), (0x015, 0x2C0)),
    ((0x00D, 0x388), (0x18C, 0x209)),
    ((0x226, 0x230), (0x224, 0x232)),
    ((0x186, 0x232), (0x036, 0x382)),
    ((0x029, 0x058), (0x038, 0x049)),
)

GRAPH6 = (
    "fsaCCA?_C?I_T?W_Eo?[?QOGhE@I??e??IeA@gB?JA?FA?BOc@aOSKK?Yo?"
    "@`_o?IL_O?WpA?B?ObpIOPEp_KH@BoCaBaQ?aQ`cOGDEwc??Z{@_?@ERW??CFrG???"
)

K20_MODEL = (
    (0,),
    (1, 22),
    (2, 29),
    (3, 18),
    (4, 35),
    (5, 26),
    (6, 17),
    (7, 21),
    (8, 15),
    (9, 13),
    (10, 24),
    (11, 30),
    (12, 23),
    (14, 34),
    (16, 32),
    (19, 25),
    (20, 33),
    (27, 37),
    (28, 38),
    (31, 36),
)
