from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from ortools.sat.python import cp_model


@dataclass(frozen=True)
class Outcome:
    vertices: int
    edges: int
    independence: int

    @property
    def ratio(self) -> Fraction:
        return Fraction(self.independence, self.vertices)

    def as_dict(self) -> dict[str, int | str]:
        return {
            "vertices": self.vertices,
            "edges": self.edges,
            "independence": self.independence,
            "ratio": str(self.ratio),
        }


def independence_number(
    vertex_count: int,
    edges: tuple[tuple[int, int, int], ...],
    *,
    workers: int = 8,
) -> int:
    model = cp_model.CpModel()
    selected = [model.new_bool_var(f"x_{index}") for index in range(vertex_count)]
    for edge in edges:
        model.add(sum(selected[index] for index in edge) <= 2)
    model.maximize(sum(selected))

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    status = solver.solve(model)
    if status != cp_model.OPTIMAL:
        raise RuntimeError(f"independence optimization ended with {solver.status_name(status)}")
    return int(round(solver.objective_value))
