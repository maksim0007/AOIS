from logic_lab.boolean_function import BooleanFunction
from logic_lab.normal_forms import build_sdnf, build_sknf, numeric_sdnf, numeric_sknf
from logic_lab.post_classes import is_linear, is_monotone, is_self_dual, post_classes
from logic_lab.zhegalkin import coefficients, monomial, polynomial


def test_normal_forms_for_xor():
    function = BooleanFunction("(a&!b)|(!a&b)")
    assert build_sdnf(function) == "(!a & b) | (a & !b)"
    assert build_sknf(function) == "(a | b) & (!a | !b)"
    assert numeric_sdnf(function) == "Σ(1, 2)"
    assert numeric_sknf(function) == "Π(0, 3)"


def test_normal_forms_edge_cases():
    assert build_sknf(BooleanFunction("a|!a")) == "1"
    assert build_sdnf(BooleanFunction("a&!a")) == "0"


def test_zhegalkin_for_xor():
    function = BooleanFunction("(a&!b)|(!a&b)")
    assert coefficients(function) == [0, 1, 1, 0]
    assert monomial(function, 0) == "1"
    assert monomial(function, 3) == "a*b"
    assert polynomial(function) == "a ⊕ b"


def test_post_classes():
    and_function = BooleanFunction("a&b")
    classes = post_classes(and_function)
    assert classes == {"T0": True, "T1": True, "S": False, "M": True, "L": False}
    assert is_monotone(and_function) is True
    assert is_linear(and_function) is False
    assert is_self_dual(BooleanFunction("!a")) is True
