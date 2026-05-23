import pytest

from logic_lab.ast_nodes import Const
from logic_lab.boolean_function import BooleanFunction
from logic_lab.parser import ParseError, parse_expression


def test_parser_supports_unicode_and_ascii():
    left = parse_expression("!(!a->!b)|c")
    right = parse_expression("¬(¬a→¬b)∨c")
    values = {"a": 0, "b": 1, "c": 0}
    assert left.evaluate(values) == right.evaluate(values)


def test_equivalence_and_constants():
    function = BooleanFunction("a~b")
    assert function.truth_vector() == [1, 0, 0, 1]
    assert Const(1).evaluate({}) == 1
    assert Const(0).variables() == set()


def test_truth_table_numbers():
    function = BooleanFunction("a|b")
    assert function.variables == ["a", "b"]
    assert function.truth_vector() == [0, 1, 1, 1]
    assert function.minterms() == [1, 2, 3]
    assert function.maxterms() == [0]
    assert function.index_form() == 7


def test_parser_errors():
    for text in ["", "a+x", "(a&b", "x&y", "a->"]:
        with pytest.raises(ParseError):
            parse_expression(text)
