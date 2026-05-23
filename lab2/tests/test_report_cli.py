from logic_lab.cli import process_expression
from logic_lab.report import calculation_table_text, derivatives_text, generate_report, truth_table_text
from logic_lab.boolean_function import BooleanFunction
from logic_lab.table_format import ascii_table


def test_report_contains_all_required_sections():
    report = generate_report("!(!a->!b)|c")
    required = [
        "Таблица истинности",
        "СДНФ",
        "СКНФ",
        "Числовая форма СДНФ",
        "Индексная форма",
        "Классы Поста",
        "Полином Жегалкина",
        "Фиктивные переменные",
        "Булевы производные",
        "Расчетный метод",
        "Расчетно-табличный метод",
        "карта Карно",
    ]
    for item in required:
        assert item in report


def test_process_expression_and_helpers():
    function = BooleanFunction("a&b")
    assert "Выражение: a&b" in process_expression("a&b")
    assert "|" in truth_table_text(function)
    assert "dF/d" in derivatives_text(function)
    assert "Импликанта" in calculation_table_text(function, "dnf")
    assert ascii_table(["A"], [[1]]) == "+---+\n| A |\n+---+\n| 1 |\n+---+"
