import pytest

from logic_lab.boolean_function import BooleanFunction
from logic_lab.derivatives import derivative_value, derivative_vector, fictitious_variables


def test_partial_derivative_for_xor():
    function = BooleanFunction("(a&!b)|(!a&b)")
    assert derivative_vector(function, ["a"]) == [1, 1, 1, 1]
    assert derivative_value(function, (0, 0), ["a"]) == 1


def test_mixed_derivative_and_fictitious():
    function = BooleanFunction("a|b")
    assert derivative_vector(function, ["a", "b"]) == [1, 1, 1, 1]
    assert fictitious_variables(BooleanFunction("a|!a")) == ["a"]


def test_derivative_validation():
    function = BooleanFunction("a&b")
    with pytest.raises(ValueError):
        derivative_vector(function, [])
    with pytest.raises(ValueError):
        derivative_vector(function, ["a", "b", "c", "d", "e"])
    with pytest.raises(ValueError):
        derivative_vector(function, ["c"])
