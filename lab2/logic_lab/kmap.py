from __future__ import annotations

from .boolean_function import BooleanFunction
from .minimization import minimize
from .table_format import ascii_table


def gray_code(bits: int) -> list[tuple[int, ...]]:
    if bits == 0:
        return [tuple()]
    previous = gray_code(bits - 1)
    return [(0,) + item for item in previous] + [(1,) + item for item in reversed(previous)]


def bits_to_text(bits: tuple[int, ...]) -> str:
    return "".join(map(str, bits)) if bits else "-"


def split_variables(function: BooleanFunction) -> tuple[list[str], list[str]]:
    row_count = len(function.variables) // 2
    return function.variables[:row_count], function.variables[row_count:]


def karnaugh_grid(function: BooleanFunction, invert: bool = False) -> tuple[list[str], list[str], list[list[int]]]:
    row_vars, col_vars = split_variables(function)
    row_codes = gray_code(len(row_vars))
    col_codes = gray_code(len(col_vars))
    rows: list[list[int]] = []
    for row_code in row_codes:
        current: list[int] = []
        for col_code in col_codes:
            assignment = dict(zip(function.variables, row_code + col_code))
            value = function.evaluate(assignment)
            current.append(1 - value if invert else value)
        rows.append(current)
    return [bits_to_text(code) for code in row_codes], [bits_to_text(code) for code in col_codes], rows


def format_karnaugh_map(function: BooleanFunction, mode: str = "dnf") -> str:
    if mode not in {"dnf", "cnf"}:
        raise ValueError("mode должен быть dnf или cnf")
    row_vars, col_vars = split_variables(function)
    row_label = "".join(row_vars) or "-"
    col_label = "".join(col_vars) or "-"
    row_headers, col_headers, values = karnaugh_grid(function, invert=(mode == "cnf"))
    table_rows = [[row_header] + row for row_header, row in zip(row_headers, values)]
    title = f"{row_label}\\{col_label}"
    table = ascii_table([title] + col_headers, table_rows)
    result = minimize(function, mode)["result"]
    kind = "КНФ" if mode == "cnf" else "ДНФ"
    value_name = "нули функции" if mode == "cnf" else "единицы функции"
    return f"Карта Карно ({kind}), в таблице отмечены {value_name}:\n{table}\nМинимизированная {kind}: {result}"


def minimize_by_kmap(function: BooleanFunction, mode: str = "dnf") -> dict[str, object]:
    row_headers, col_headers, grid = karnaugh_grid(function, invert=(mode == "cnf"))
    return {
        "row_headers": row_headers,
        "col_headers": col_headers,
        "grid": grid,
        "table": format_karnaugh_map(function, mode),
        "result": minimize(function, mode)["result"],
    }
