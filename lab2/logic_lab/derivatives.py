from __future__ import annotations

from itertools import product
from typing import Iterable

from .boolean_function import BooleanFunction


def derivative_value(function: BooleanFunction, base_bits: tuple[int, ...], variables: Iterable[str]) -> int:
    names = list(variables)
    if not 1 <= len(names) <= 4:
        raise ValueError("Производная задается по 1-4 переменным")
    for name in names:
        if name not in function.variables:
            raise ValueError(f"Переменная {name} отсутствует в функции")

    indices = [function.variables.index(name) for name in names]
    total = 0
    for toggles in product((0, 1), repeat=len(indices)):
        bits = list(base_bits)
        for index, toggle in zip(indices, toggles):
            if toggle:
                bits[index] = 1 - bits[index]
        total ^= function.value_for_bits(tuple(bits))
    return total


def derivative_vector(function: BooleanFunction, variables: Iterable[str]) -> list[int]:
    names = list(variables)
    return [derivative_value(function, bits, names) for bits in function.iter_bit_tuples()]


def fictitious_variables(function: BooleanFunction) -> list[str]:
    return [name for name in function.variables if all(value == 0 for value in derivative_vector(function, [name]))]
