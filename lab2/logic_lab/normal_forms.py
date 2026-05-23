from __future__ import annotations

from .boolean_function import BooleanFunction, TruthRow


def _minterm(variables: list[str], row: TruthRow) -> str:
    literals = [var if bit == 1 else f"!{var}" for var, bit in zip(variables, row.bits)]
    return "(" + " & ".join(literals) + ")"


def _maxterm(variables: list[str], row: TruthRow) -> str:
    literals = [f"!{var}" if bit == 1 else var for var, bit in zip(variables, row.bits)]
    return "(" + " | ".join(literals) + ")"


def build_sdnf(function: BooleanFunction) -> str:
    terms = [_minterm(function.variables, row) for row in function.truth_table() if row.result == 1]
    return " | ".join(terms) if terms else "0"


def build_sknf(function: BooleanFunction) -> str:
    terms = [_maxterm(function.variables, row) for row in function.truth_table() if row.result == 0]
    return " & ".join(terms) if terms else "1"


def numeric_sdnf(function: BooleanFunction) -> str:
    return "Σ(" + ", ".join(map(str, function.minterms())) + ")"


def numeric_sknf(function: BooleanFunction) -> str:
    return "Π(" + ", ".join(map(str, function.maxterms())) + ")"
