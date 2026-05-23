from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, List, Tuple

from .ast_nodes import Node
from .parser import parse_expression


@dataclass(frozen=True)
class TruthRow:
    bits: Tuple[int, ...]
    values: Dict[str, int]
    result: int


class BooleanFunction:
    def __init__(self, expression: str):
        self.expression = expression
        self.ast: Node = parse_expression(expression)
        self.variables: List[str] = sorted(self.ast.variables())

    def evaluate(self, values: Dict[str, int]) -> int:
        return self.ast.evaluate(values)

    def iter_bit_tuples(self) -> Iterable[Tuple[int, ...]]:
        return product((0, 1), repeat=len(self.variables))

    def assignment_from_bits(self, bits: Tuple[int, ...]) -> Dict[str, int]:
        return dict(zip(self.variables, bits))

    def value_for_bits(self, bits: Tuple[int, ...]) -> int:
        return self.evaluate(self.assignment_from_bits(bits))

    def truth_table(self) -> List[TruthRow]:
        rows: List[TruthRow] = []
        for bits in self.iter_bit_tuples():
            assignment = self.assignment_from_bits(bits)
            rows.append(TruthRow(bits=bits, values=assignment, result=self.evaluate(assignment)))
        return rows

    def truth_vector(self) -> List[int]:
        return [row.result for row in self.truth_table()]

    def minterms(self) -> List[int]:
        return [idx for idx, value in enumerate(self.truth_vector()) if value == 1]

    def maxterms(self) -> List[int]:
        return [idx for idx, value in enumerate(self.truth_vector()) if value == 0]

    def index_form(self) -> int:
        bits = "".join(str(bit) for bit in self.truth_vector())
        return int(bits, 2) if bits else 0
