from __future__ import annotations

from .boolean_function import BooleanFunction


def coefficients(function: BooleanFunction) -> list[int]:
    coeffs = function.truth_vector()[:]
    n = len(function.variables)
    for bit in range(n):
        step = 1 << bit
        for mask in range(1 << n):
            if mask & step:
                coeffs[mask] ^= coeffs[mask ^ step]
    return coeffs


def monomial(function: BooleanFunction, mask: int) -> str:
    if mask == 0:
        return "1"
    factors = [var for pos, var in enumerate(function.variables) if mask & (1 << pos)]
    return "*".join(factors)


def polynomial(function: BooleanFunction) -> str:
    terms = [monomial(function, mask) for mask, coeff in enumerate(coefficients(function)) if coeff == 1]
    return " ⊕ ".join(terms) if terms else "0"
