from collections.abc import Iterator


def integer_partitions(total: int, ceiling: int | None = None) -> Iterator[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    bound = total if ceiling is None else min(total, ceiling)
    for first in range(bound, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first, *rest)
