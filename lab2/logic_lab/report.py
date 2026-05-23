from __future__ import annotations

from itertools import combinations

from .boolean_function import BooleanFunction
from .derivatives import derivative_vector, fictitious_variables
from .kmap import minimize_by_kmap
from .minimization import Implicant, minimize
from .normal_forms import build_sdnf, build_sknf, numeric_sdnf, numeric_sknf
from .post_classes import post_classes
from .table_format import ascii_table
from .zhegalkin import polynomial


def truth_table_text(function: BooleanFunction) -> str:
    headers = function.variables + ["F"]
    rows = [[*row.bits, row.result] for row in function.truth_table()]
    return ascii_table(headers, rows)


def post_classes_text(function: BooleanFunction) -> str:
    return ", ".join(f"{name}={'да' if value else 'нет'}" for name, value in post_classes(function).items())


def derivatives_text(function: BooleanFunction) -> str:
    lines: list[str] = []
    for size in range(1, min(4, len(function.variables)) + 1):
        for group in combinations(function.variables, size):
            lines.append(f"dF/d({','.join(group)}) = {derivative_vector(function, group)}")
    return "\n".join(lines) if lines else "-"


def minimization_stages_text(function: BooleanFunction, mode: str) -> str:
    data = minimize(function, mode)
    lines = [f"Исходные номера: {data['indices']}"]
    for index, stage in enumerate(data["stage_strings"], start=1):
        lines.append(f"Этап склеивания {index}: {stage}")
    lines.append(f"Результат: {data['result']}")
    return "\n".join(lines)


def _implicant_text(implicant: Implicant, variables: list[str], mode: str) -> str:
    return implicant.dnf(variables) if mode == "dnf" else implicant.cnf(variables)


def calculation_table_text(function: BooleanFunction, mode: str) -> str:
    data = minimize(function, mode)
    indices = data["indices"]
    selected = data["selected"]
    coverage = data["coverage_table"]
    headers = ["Импликанта"] + [str(item) for item in indices]
    rows: list[list[str]] = []
    for implicant in selected:
        row = [_implicant_text(implicant, function.variables, mode)]
        row.extend("X" if covered else "" for covered in coverage[implicant])
        rows.append(row)
    return ascii_table(headers, rows) + f"\nРезультат: {data['result']}"


def generate_report(expression: str) -> str:
    function = BooleanFunction(expression)
    dnf_map = minimize_by_kmap(function, "dnf")
    cnf_map = minimize_by_kmap(function, "cnf")
    fake = fictitious_variables(function)
    blocks = [
        f"Выражение: {expression}",
        f"Переменные: {', '.join(function.variables) or '-'}",
        "Таблица истинности:\n" + truth_table_text(function),
        "СДНФ: " + build_sdnf(function),
        "СКНФ: " + build_sknf(function),
        "Числовая форма СДНФ: " + numeric_sdnf(function),
        "Числовая форма СКНФ: " + numeric_sknf(function),
        f"Индексная форма: {function.index_form()}",
        "Классы Поста: " + post_classes_text(function),
        "Полином Жегалкина: " + polynomial(function),
        "Фиктивные переменные: " + (", ".join(fake) if fake else "нет"),
        "Булевы производные:\n" + derivatives_text(function),
        "Расчетный метод, ДНФ:\n" + minimization_stages_text(function, "dnf"),
        "Расчетный метод, КНФ:\n" + minimization_stages_text(function, "cnf"),
        "Расчетно-табличный метод, ДНФ:\n" + minimization_stages_text(function, "dnf") + "\n" + calculation_table_text(function, "dnf"),
        "Расчетно-табличный метод, КНФ:\n" + minimization_stages_text(function, "cnf") + "\n" + calculation_table_text(function, "cnf"),
        "Табличный метод — карта Карно для ДНФ:\n" + dnf_map["table"],
        "Табличный метод — карта Карно для КНФ:\n" + cnf_map["table"],
    ]
    return "\n\n".join(blocks)
