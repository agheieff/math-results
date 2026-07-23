from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical195

from strong_seymour.tournament import hall_neighbours, out_neighbours


@dataclass(frozen=True)
class Encoding:
    cnf: CNF
    pool: IDPool
    edges: dict[tuple[int, int], int]
    witnesses: dict[tuple[int, int], int]


def arc(edges: dict[tuple[int, int], int], source: int, target: int) -> int:
    if source == target:
        raise ValueError("loops have no literals")
    if source < target:
        return edges[source, target]
    return -edges[target, source]


def add_cardinality(cnf: CNF, encoded: CNF) -> None:
    cnf.extend(encoded.clauses)


def build_encoding(order: int, *, fix_first_row: bool = True) -> Encoding:
    if order < 13:
        raise ValueError("the paper already proves all orders below 13")
    pool = IDPool()
    cnf = CNF()
    edges = {
        (source, target): pool.id(f"e_{source}_{target}")
        for source in range(order)
        for target in range(source + 1, order)
    }
    witnesses = {
        (vertex, source): pool.id(f"w_{vertex}_{source}")
        for vertex in range(order)
        for source in range(order)
        if source != vertex
    }
    neighbours = {
        (vertex, target): pool.id(f"q_{vertex}_{target}")
        for vertex in range(order)
        for target in range(order)
        if target != vertex
    }

    for vertex in range(order):
        outgoing = [arc(edges, vertex, target) for target in range(order) if target != vertex]
        degree_encoding = CardEnc.equals if order == 13 else CardEnc.atleast
        add_cardinality(
            cnf,
            degree_encoding(outgoing, bound=6, vpool=pool, encoding=EncType.seqcounter),
        )

        witness_literals = [
            witnesses[vertex, source] for source in range(order) if source != vertex
        ]
        neighbour_literals = [
            neighbours[vertex, target] for target in range(order) if target != vertex
        ]
        if order == 13 or vertex == 0:
            add_cardinality(
                cnf,
                CardEnc.atleast(
                    witness_literals,
                    bound=3,
                    vpool=pool,
                    encoding=EncType.seqcounter,
                ),
            )
        # Choose an inclusion-minimal Hall witness. It has |Q| = |W| - 1.
        add_cardinality(
            cnf,
            CardEnc.atmost(
                neighbour_literals + [-literal for literal in witness_literals],
                bound=order - 2,
                vpool=pool,
                encoding=EncType.seqcounter,
            ),
        )
        add_cardinality(
            cnf,
            CardEnc.atmost(
                witness_literals + [-literal for literal in neighbour_literals],
                bound=order,
                vpool=pool,
                encoding=EncType.seqcounter,
            ),
        )

        for source in range(order):
            if source == vertex:
                continue
            cnf.append([-witnesses[vertex, source], arc(edges, vertex, source)])

        for target in range(order):
            if target == vertex:
                continue
            q_literal = neighbours[vertex, target]
            incoming_literal = arc(edges, target, vertex)
            cnf.append([-q_literal, incoming_literal])
            hits: list[int] = []
            for source in range(order):
                if source in (vertex, target):
                    continue
                witness_literal = witnesses[vertex, source]
                edge_literal = arc(edges, source, target)
                hit = pool.id(f"h_{vertex}_{source}_{target}")
                hits.append(hit)
                cnf.append([-hit, witness_literal])
                cnf.append([-hit, incoming_literal])
                cnf.append([-hit, edge_literal])
                cnf.append([-witness_literal, -incoming_literal, -edge_literal, hit])
                cnf.append([-hit, q_literal])
            cnf.append([-q_literal, *hits])

    if fix_first_row:
        if order > 14:
            raise ValueError("first-row symmetry break is justified only for orders 13 and 14")
        for target in range(1, order):
            cnf.append([arc(edges, 0, target) if target <= 6 else -arc(edges, 0, target)])

    return Encoding(cnf=cnf, pool=pool, edges=edges, witnesses=witnesses)


def extract_certificate(order: int, model: list[int], encoding: Encoding) -> dict[str, Any]:
    true_literals = {literal for literal in model if literal > 0}
    adjacency = [
        [
            int(
                source != target
                and (
                    arc(encoding.edges, source, target) in true_literals
                    if arc(encoding.edges, source, target) > 0
                    else -arc(encoding.edges, source, target) not in true_literals
                )
            )
            for target in range(order)
        ]
        for source in range(order)
    ]
    hall_witnesses = {
        str(vertex): [
            source
            for source in range(order)
            if source != vertex and encoding.witnesses[vertex, source] in true_literals
        ]
        for vertex in range(order)
    }
    return {
        "format": "strong-seymour-tournament-v1",
        "order": order,
        "adjacency": adjacency,
        "outdegrees": [len(out_neighbours(adjacency, vertex)) for vertex in range(order)],
        "hall_witnesses": hall_witnesses,
        "hall_neighbours": {
            str(vertex): list(hall_neighbours(adjacency, vertex, hall_witnesses[str(vertex)]))
            for vertex in range(order)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=13)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cnf", type=Path)
    args = parser.parse_args()

    encoding = build_encoding(args.order)
    if args.cnf is not None:
        encoding.cnf.to_file(args.cnf)
    print(
        f"c order={args.order} variables={encoding.pool.top} clauses={len(encoding.cnf.clauses)}",
        flush=True,
    )
    with Cadical195(bootstrap_with=encoding.cnf.clauses) as solver:
        satisfiable = solver.solve()
        print("s SATISFIABLE" if satisfiable else "s UNSATISFIABLE", flush=True)
        if not satisfiable:
            return
        certificate = extract_certificate(args.order, solver.get_model(), encoding)

    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(encoded, end="")
    else:
        args.output.write_text(encoded)


if __name__ == "__main__":
    main()
