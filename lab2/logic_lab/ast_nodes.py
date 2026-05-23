from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set


class Node:
    def evaluate(self, values: Dict[str, int]) -> int:
        raise NotImplementedError

    def variables(self) -> Set[str]:
        raise NotImplementedError


@dataclass(frozen=True)
class Const(Node):
    value: int

    def evaluate(self, values: Dict[str, int]) -> int:
        return self.value

    def variables(self) -> Set[str]:
        return set()


@dataclass(frozen=True)
class Var(Node):
    name: str

    def evaluate(self, values: Dict[str, int]) -> int:
        return int(values[self.name])

    def variables(self) -> Set[str]:
        return {self.name}


@dataclass(frozen=True)
class Not(Node):
    expr: Node

    def evaluate(self, values: Dict[str, int]) -> int:
        return 1 - self.expr.evaluate(values)

    def variables(self) -> Set[str]:
        return self.expr.variables()


@dataclass(frozen=True)
class Binary(Node):
    left: Node
    right: Node

    def variables(self) -> Set[str]:
        return self.left.variables() | self.right.variables()


@dataclass(frozen=True)
class And(Binary):
    def evaluate(self, values: Dict[str, int]) -> int:
        return self.left.evaluate(values) & self.right.evaluate(values)


@dataclass(frozen=True)
class Or(Binary):
    def evaluate(self, values: Dict[str, int]) -> int:
        return self.left.evaluate(values) | self.right.evaluate(values)


@dataclass(frozen=True)
class Implication(Binary):
    def evaluate(self, values: Dict[str, int]) -> int:
        return int((1 - self.left.evaluate(values)) | self.right.evaluate(values))


@dataclass(frozen=True)
class Equivalence(Binary):
    def evaluate(self, values: Dict[str, int]) -> int:
        return int(self.left.evaluate(values) == self.right.evaluate(values))
