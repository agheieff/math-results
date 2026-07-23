"""Direct transversal verification and a Shor-move search."""

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from random import Random

from latin_transversals.squares import Entry, Square

Transversal = tuple[int, ...]


def entries(table: Square, columns: Sequence[int]) -> tuple[Entry, ...]:
    return tuple(Entry(row, column, table[row][column]) for row, column in enumerate(columns))


def is_transversal(table: Square, columns: Sequence[int]) -> bool:
    n = len(table)
    return (
        len(columns) == n
        and set(columns) == set(range(n))
        and len({table[row][column] for row, column in enumerate(columns)}) == n
    )


@dataclass(frozen=True)
class SearchConstraints:
    required: frozenset[Entry] = frozenset()
    forbidden: frozenset[Entry] = frozenset()
    allowed_columns: tuple[frozenset[int], ...] | None = None


def _is_allowed(
    table: Square,
    constraints: SearchConstraints,
    row: int,
    column: int,
) -> bool:
    entry = Entry(row, column, table[row][column])
    if entry in constraints.forbidden:
        return False
    allowed = constraints.allowed_columns
    return allowed is None or column in allowed[row]


def _random_diagonal(
    table: Square,
    constraints: SearchConstraints,
    random: Random,
) -> list[int] | None:
    n = len(table)
    fixed = {entry.row: entry.column for entry in constraints.required}
    if len(fixed) != len(constraints.required):
        return None
    if len(set(fixed.values())) != len(fixed):
        return None
    if any(
        table[row][column] != entry.symbol
        for entry in constraints.required
        for row, column in [(entry.row, entry.column)]
    ):
        return None
    columns = [-1] * n
    for row, column in fixed.items():
        columns[row] = column
    free_columns = [column for column in range(n) if column not in fixed.values()]
    free_rows = [row for row in range(n) if row not in fixed]

    # A randomized bipartite matching gives a valid constrained diagonal.
    random.shuffle(free_rows)
    matches: dict[int, int] = {}

    def augment(row: int, seen: set[int]) -> bool:
        candidates = free_columns.copy()
        random.shuffle(candidates)
        for column in candidates:
            if column in seen or not _is_allowed(table, constraints, row, column):
                continue
            seen.add(column)
            owner = matches.get(column)
            if owner is None or augment(owner, seen):
                matches[column] = row
                return True
        return False

    if not all(augment(row, set()) for row in free_rows):
        return None
    for column, row in matches.items():
        columns[row] = column
    return columns


def _weight(table: Square, columns: Sequence[int]) -> int:
    return len({table[row][column] for row, column in enumerate(columns)})


def find_transversal(
    table: Square,
    constraints: SearchConstraints | None = None,
    *,
    seed: int = 0,
    restarts: int = 1_000,
    climb_steps: int = 100_000,
) -> Transversal | None:
    """Implement Procedure 2 of Ghafari-Wanless with bounded restarts."""
    constraints = constraints or SearchConstraints()
    random = Random(seed)
    n = len(table)
    required_rows = {entry.row for entry in constraints.required}

    def try_swap(columns: list[int], row_a: int, row_b: int) -> bool:
        if row_a in required_rows or row_b in required_rows:
            return False
        column_a, column_b = columns[row_a], columns[row_b]
        if not _is_allowed(table, constraints, row_a, column_b):
            return False
        if not _is_allowed(table, constraints, row_b, column_a):
            return False
        columns[row_a], columns[row_b] = column_b, column_a
        return True

    for _ in range(restarts):
        columns = _random_diagonal(table, constraints, random)
        if columns is None:
            return None
        for _ in range(climb_steps):
            symbols = [table[row][column] for row, column in enumerate(columns)]
            counts = Counter(symbols)
            weight = len(counts)
            if weight == n:
                return tuple(columns)
            excess = [row for row, symbol in enumerate(symbols) if counts[symbol] > 1]
            unused = list(set(range(n)) - counts.keys())

            if weight < n - 2:
                row = random.choice(excess)
                target_symbol = random.choice(unused)
                target_column = table[row].index(target_symbol)
                other_row = columns.index(target_column)
                before = weight
                if try_swap(columns, row, other_row) and _weight(table, columns) < before:
                    try_swap(columns, row, other_row)
                continue

            if weight == n - 1:
                row = random.choice(excess)
                other_row = random.randrange(n - 1)
                if other_row >= row:
                    other_row += 1
                try_swap(columns, row, other_row)
                continue

            pairs = [(a, b) for index, a in enumerate(excess) for b in excess[index + 1 :]]
            random.shuffle(pairs)
            moved = False
            for row_a, row_b in pairs:
                if not try_swap(columns, row_a, row_b):
                    continue
                if _weight(table, columns) == n:
                    return tuple(columns)
                try_swap(columns, row_a, row_b)
            safe_pairs = [
                (a, b)
                for a, b in pairs
                if not (symbols[a] == symbols[b] and counts[symbols[a]] == 2)
            ]
            if safe_pairs:
                for row_a, row_b in safe_pairs:
                    before = _weight(table, columns)
                    if try_swap(columns, row_a, row_b):
                        if _weight(table, columns) >= before:
                            moved = True
                            break
                        try_swap(columns, row_a, row_b)
            if not moved:
                break
    return None
