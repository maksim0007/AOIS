import pytest

from logic_lab.boolean_function import BooleanFunction
from logic_lab.kmap import bits_to_text, format_karnaugh_map, gray_code, karnaugh_grid, minimize_by_kmap
from logic_lab.minimization import Implicant, gluing, minimize


def normalize(text: str) -> str:
    return text.replace(" ", "")


def test_implicant_helpers():
    first = Implicant((1, 0, 1), frozenset({5}))
    second = Implicant((1, 1, 1), frozenset({7}))
    assert first.can_merge(second)
    merged = first.merge(second)
    assert merged.pattern == (1, None, 1)
    assert merged.contains(5, 3)
    assert merged.contains(7, 3)
    assert merged.dnf(["a", "b", "c"]) == "(a & c)"
    assert merged.cnf(["a", "b", "c"]) == "(!a | !c)"


def test_gluing_and_minimization_example():
    function = BooleanFunction("a|(b&c)")
    dnf = minimize(function, "dnf")
    cnf = minimize(function, "cnf")
    assert normalize(dnf["result"]) in {"(a)∨(b&c)", "(b&c)∨(a)"}
    assert normalize(cnf["result"]) in {"(a|b)∧(a|c)", "(a|c)∧(a|b)"}
    stages, primes = gluing(function.minterms(), len(function.variables))
    assert stages
    assert primes


def test_kmap_table_is_ascii_table():
    function = BooleanFunction("a|(b&c)")
    text = format_karnaugh_map(function, "dnf")
    assert "+" in text
    assert "a\\bc" in text
    assert "00" in text and "01" in text and "11" in text and "10" in text
    assert "Минимизированная ДНФ" in text
    assert minimize_by_kmap(function, "cnf")["table"].startswith("Карта Карно")


def test_gray_and_grid():
    assert gray_code(2) == [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert bits_to_text(tuple()) == "-"
    rows, cols, grid = karnaugh_grid(BooleanFunction("a|b"))
    assert rows == ["0", "1"]
    assert cols == ["0", "1"]
    assert grid == [[0, 1], [1, 1]]


def test_invalid_minimization_mode():
    with pytest.raises(ValueError):
        minimize(BooleanFunction("a"), "bad")
    with pytest.raises(ValueError):
        format_karnaugh_map(BooleanFunction("a"), "bad")
