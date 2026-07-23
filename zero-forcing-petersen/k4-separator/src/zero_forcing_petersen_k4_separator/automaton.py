from __future__ import annotations

import hashlib
from dataclasses import dataclass
from itertools import product
from typing import cast

from .model import COLUMNS, Color, compatible

State = tuple[int, int, int, int]


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
    exact_separator_sizes: tuple[tuple[int, tuple[int, ...]], ...]
    accepting_state_digest_sha256: str

    def minimum_at(self, order: int) -> int | None:
        sizes = dict(self.exact_separator_sizes).get(order, ())
        return min(sizes) if sizes else None


def build_automaton() -> Automaton:
    states = tuple(
        cast(State, state)
        for state in product(range(len(COLUMNS)), repeat=4)
        if all(
            compatible(COLUMNS[state[index]][0], COLUMNS[state[index + 1]][0]) for index in range(3)
        )
    )
    state_index = {state: index for index, state in enumerate(states)}
    transitions: list[Transition] = []
    for source, state in enumerate(states):
        for column_index, column in enumerate(COLUMNS):
            if not compatible(COLUMNS[state[-1]][0], column[0]):
                continue
            if not compatible(COLUMNS[state[0]][1], column[1]):
                continue
            target_state: State = (state[1], state[2], state[3], column_index)
            transitions.append(
                Transition(
                    source,
                    state_index[target_state],
                    column.count(Color.B),
                    column.count(Color.Y) - 1,
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
    max_order: int = 162,
    max_separator: int = 9,
    automaton: Automaton | None = None,
) -> TransferResult:
    if max_order < 1 or max_separator < 0:
        raise ValueError("invalid transfer bounds")
    machine = automaton or build_automaton()
    state_count = len(machine.states)
    block_width = 2 * max_order + 3
    zero_offset = max_order + 1
    paths = [[0] * (max_separator + 1) for _ in range(state_count)]
    for state in range(state_count):
        paths[state][0] = 1 << (state * block_width + zero_offset)

    digest = hashlib.sha256()
    exact_sizes: list[tuple[int, tuple[int, ...]]] = []
    accepting_width = (state_count + 7) // 8
    for order in range(1, max_order + 1):
        next_paths = [[0] * (max_separator + 1) for _ in range(state_count)]
        for transition in machine.transitions:
            source = paths[transition.source]
            target = next_paths[transition.target]
            for separator in range(max_separator + 1 - transition.separator_weight):
                marked = source[separator]
                if transition.balance_delta == 1:
                    marked <<= 1
                elif transition.balance_delta == -1:
                    marked >>= 1
                target[separator + transition.separator_weight] |= marked
        paths = next_paths

        present: list[int] = []
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
    return TransferResult(tuple(exact_sizes), digest.hexdigest())
