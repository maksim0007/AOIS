from __future__ import annotations

from itertools import product

from .boolean_function import BooleanFunction
from .zhegalkin import coefficients


def preserves_zero(function: BooleanFunction) -> bool:
    return function.truth_vector()[0] == 0


def preserves_one(function: BooleanFunction) -> bool:
    return function.truth_vector()[-1] == 1


def is_self_dual(function: BooleanFunction) -> bool:
    vector = function.truth_vector()
    for idx, value in enumerate(vector):
        if value == vector[len(vector) - 1 - idx]:
            return False
    return True


def is_monotone(function: BooleanFunction) -> bool:
    points = list(product((0, 1), repeat=len(function.variables)))
    for left in points:
        for right in points:
            if all(a <= b for a, b in zip(left, right)):
                if function.value_for_bits(left) > function.value_for_bits(right):
                    return False
    return True


def is_linear(function: BooleanFunction) -> bool:
    for mask, coeff in enumerate(coefficients(function)):
        if coeff == 1 and bin(mask).count("1") > 1:
            return False
    return True


def post_classes(function: BooleanFunction) -> dict[str, bool]:
    return {
        "T0": preserves_zero(function),
        "T1": preserves_one(function),
        "S": is_self_dual(function),
        "M": is_monotone(function),
        "L": is_linear(function),
    }
