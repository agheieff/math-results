from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .separator import Color, Column, compatible

State = tuple[int, int, int]

COLUMNS: tuple[Column, ...] = tuple(
    (outer, inner) for outer in Color for inner in Color if compatible(outer, inner)
)


@dataclass(frozen=True)
class Transition:
    source: int
    target: int
    separator_weight: int
    balance_delta: int


@dataclass(frozen=True)
class Automaton:
    states: tuple[State, ...]
    transitions: tuple[Transition, ...]


@dataclass(frozen=True)
class TransferResult:
    max_order: int
    max_separator: int
    exact_separator_sizes: tuple[tuple[int, tuple[int, ...]], ...]
    accepting_state_digest_sha256: str

    def minimum_at(self, order: int) -> int | None:
        exact = dict(self.exact_separator_sizes).get(order, ())
        return min(exact) if exact else None


def build_automaton() -> Automaton:
    states = tuple(
        (first, second, third)
        for first in range(len(COLUMNS))
        for second in range(len(COLUMNS))
        for third in range(len(COLUMNS))
        if compatible(COLUMNS[first][0], COLUMNS[second][0])
        and compatible(COLUMNS[second][0], COLUMNS[third][0])
    )
    state_index = {state: index for index, state in enumerate(states)}
    transitions = []
    for source, (first, second, third) in enumerate(states):
        for new_index, new_column in enumerate(COLUMNS):
            if not compatible(COLUMNS[third][0], new_column[0]):
                continue
            if not compatible(COLUMNS[first][1], new_column[1]):
                continue
            target = state_index[(second, third, new_index)]
            transitions.append(
                Transition(
                    source,
                    target,
                    new_column.count(Color.B),
                    new_column.count(Color.Y) - 1,
                )
            )
    return Automaton(states, tuple(transitions))


def automaton_digest(automaton: Automaton) -> str:
    digest = hashlib.sha256()
    for column in COLUMNS:
        digest.update(bytes(column))
    for state in automaton.states:
        digest.update(bytes(state))
    for transition in automaton.transitions:
        digest.update(transition.source.to_bytes(2, "little"))
        digest.update(transition.target.to_bytes(2, "little"))
        digest.update(bytes((transition.separator_weight, transition.balance_delta + 1)))
    return digest.hexdigest()


def transfer_certificate(
    max_order: int = 98,
    max_separator: int = 7,
    automaton: Automaton | None = None,
) -> TransferResult:
    if max_order < 1 or max_separator < 0:
        raise ValueError("invalid transfer bounds")
    machine = automaton or build_automaton()
    state_count = len(machine.states)
    block_width = 2 * max_order + 3
    zero_offset = max_order + 1
    exact_sizes = []
    digest = hashlib.sha256()

    paths = [[0] * (max_separator + 1) for _ in range(state_count)]
    for state in range(state_count):
        paths[state][0] = 1 << (state * block_width + zero_offset)

    accepting_width = (state_count + 7) // 8
    for order in range(1, max_order + 1):
        next_paths = [[0] * (max_separator + 1) for _ in range(state_count)]
        for transition in machine.transitions:
            source = paths[transition.source]
            target = next_paths[transition.target]
            upper = max_separator + 1 - transition.separator_weight
            for separator in range(upper):
                marked_starts = source[separator]
                if transition.balance_delta == 1:
                    marked_starts <<= 1
                elif transition.balance_delta == -1:
                    marked_starts >>= 1
                target[separator + transition.separator_weight] |= marked_starts
        paths = next_paths

        present = []
        for separator in range(max_separator + 1):
            accepting_states = 0
            for state in range(state_count):
                marker = 1 << (state * block_width + zero_offset)
                if paths[state][separator] & marker:
                    accepting_states |= 1 << state
            if accepting_states:
                present.append(separator)
            digest.update(order.to_bytes(2, "little"))
            digest.update(bytes((separator,)))
            digest.update(accepting_states.to_bytes(accepting_width, "little"))
        exact_sizes.append((order, tuple(present)))

    return TransferResult(
        max_order,
        max_separator,
        tuple(exact_sizes),
        digest.hexdigest(),
    )
