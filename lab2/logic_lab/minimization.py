from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Optional

from .boolean_function import BooleanFunction


@dataclass(frozen=True)
class Implicant:
    pattern: tuple[Optional[int], ...]
    covers: frozenset[int]

    def can_merge(self, other: "Implicant") -> bool:
        differences = 0
        for left, right in zip(self.pattern, other.pattern):
            if left == right:
                continue
            if left is None or right is None:
                return False
            differences += 1
        return differences == 1

    def merge(self, other: "Implicant") -> "Implicant":
        pattern = tuple(left if left == right else None for left, right in zip(self.pattern, other.pattern))
        return Implicant(pattern, self.covers | other.covers)

    def literal_count(self) -> int:
        return sum(bit is not None for bit in self.pattern)

    def contains(self, index: int, width: int) -> bool:
        bits = tuple(int(ch) for ch in f"{index:0{width}b}")
        return all(mask is None or mask == bit for mask, bit in zip(self.pattern, bits))

    def dnf(self, variables: list[str]) -> str:
        parts: list[str] = []
        for var, bit in zip(variables, self.pattern):
            if bit is None:
                continue
            parts.append(var if bit == 1 else f"!{var}")
        return "1" if not parts else "(" + " & ".join(parts) + ")"

    def cnf(self, variables: list[str]) -> str:
        parts: list[str] = []
        for var, bit in zip(variables, self.pattern):
            if bit is None:
                continue
            parts.append(f"!{var}" if bit == 1 else var)
        return "0" if not parts else "(" + " | ".join(parts) + ")"


def _pattern_key(pattern: tuple[Optional[int], ...]) -> tuple[int, ...]:
    return tuple(2 if bit is None else bit for bit in pattern)


def _unique(implicants: Iterable[Implicant]) -> list[Implicant]:
    found: dict[tuple[Optional[int], ...], Implicant] = {}
    for item in implicants:
        old = found.get(item.pattern)
        if old is None or len(item.covers) > len(old.covers):
            found[item.pattern] = item
    return sorted(found.values(), key=lambda item: (_pattern_key(item.pattern), sorted(item.covers)))


def _initial(indices: list[int], width: int) -> list[Implicant]:
    return [Implicant(tuple(int(ch) for ch in f"{idx:0{width}b}"), frozenset({idx})) for idx in indices]


def gluing(indices: list[int], width: int) -> tuple[list[list[Implicant]], list[Implicant]]:
    current = _initial(sorted(indices), width)
    stages = [current]
    primes: list[Implicant] = []
    while current:
        next_stage: list[Implicant] = []
        used: set[Implicant] = set()
        for left, right in combinations(current, 2):
            if left.can_merge(right):
                used.add(left)
                used.add(right)
                next_stage.append(left.merge(right))
        primes.extend(item for item in current if item not in used)
        next_stage = _unique(next_stage)
        if not next_stage:
            break
        stages.append(next_stage)
        current = next_stage
    return stages, _unique(primes)


def _select_cover(indices: list[int], primes: list[Implicant], width: int) -> list[Implicant]:
    if not indices:
        return []
    chart = {idx: [prime for prime in primes if prime.contains(idx, width)] for idx in indices}
    selected: set[Implicant] = set()
    covered: set[int] = set()
    for idx, owners in chart.items():
        if len(owners) == 1:
            selected.add(owners[0])
    for item in selected:
        for idx in indices:
            if item.contains(idx, width):
                covered.add(idx)
    remaining = [idx for idx in indices if idx not in covered]
    if not remaining:
        return sorted(selected, key=lambda item: (item.literal_count(), _pattern_key(item.pattern)))

    candidates = [prime for prime in primes if prime not in selected]
    best: tuple[int, int, tuple[tuple[int, ...], ...], tuple[Implicant, ...]] | None = None
    for count in range(1, len(candidates) + 1):
        for combo in combinations(candidates, count):
            candidate_set = set(combo) | selected
            if all(any(item.contains(idx, width) for item in candidate_set) for idx in indices):
                ordered = tuple(sorted(candidate_set, key=lambda item: (item.literal_count(), _pattern_key(item.pattern))))
                score = (len(ordered), sum(item.literal_count() for item in ordered), tuple(_pattern_key(item.pattern) for item in ordered), ordered)
                if best is None or score < best:
                    best = score
        if best is not None:
            break
    return list(best[-1]) if best else sorted(selected, key=lambda item: (item.literal_count(), _pattern_key(item.pattern)))


def _format_stage(stage: list[Implicant], variables: list[str], mode: str) -> str:
    if not stage:
        return "-"
    if mode == "dnf":
        return " ∨ ".join(item.dnf(variables) for item in stage)
    return " ∧ ".join(item.cnf(variables) for item in stage)


def _format_result(selected: list[Implicant], variables: list[str], mode: str) -> str:
    if not selected:
        return "0" if mode == "dnf" else "1"
    if mode == "dnf":
        return " ∨ ".join(item.dnf(variables) for item in selected)
    return " ∧ ".join(item.cnf(variables) for item in selected)


def minimize(function: BooleanFunction, mode: str) -> dict[str, object]:
    if mode not in {"dnf", "cnf"}:
        raise ValueError("mode должен быть dnf или cnf")
    width = len(function.variables)
    indices = function.minterms() if mode == "dnf" else function.maxterms()
    stages, primes = gluing(indices, width)
    selected = _select_cover(indices, primes, width)
    table = {item: [item.contains(idx, width) for idx in indices] for item in selected}
    return {
        "indices": indices,
        "stages": stages,
        "stage_strings": [_format_stage(stage, function.variables, mode) for stage in stages],
        "prime_implicants": primes,
        "selected": selected,
        "coverage_table": table,
        "result": _format_result(selected, function.variables, mode),
    }
