import sys

import pytest

from logic_lab import cli
from logic_lab.__main__ import main as package_main
from logic_lab.boolean_function import BooleanFunction
from logic_lab.minimization import Implicant, gluing, minimize
from logic_lab.parser import Lexer, Parser, ParseError
from logic_lab.post_classes import is_linear


def test_print_menu_and_console_exit(monkeypatch, capsys):
    answers = iter(["a|b", "2", "3", "4", "a&b", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    cli.console_menu()
    out = capsys.readouterr().out
    assert "Карта Карно" in out
    assert "Выход" in out


def test_main_with_argument(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["python -m logic_lab", "a&b"])
    package_main()
    assert "Выражение: a&b" in capsys.readouterr().out


def test_main_without_argument(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["python -m logic_lab"])
    answers = iter(["a", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    package_main()
    assert "Выход" in capsys.readouterr().out


def test_console_invalid_choice_and_expression(monkeypatch, capsys):
    answers = iter(["a|", "1", "bad", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    cli.console_menu()
    out = capsys.readouterr().out
    assert "Ошибка" in out
    assert "Неверный пункт меню" in out


def test_lexer_bad_arrow_and_parser_extra_token():
    with pytest.raises(ParseError):
        Lexer("a-b").tokenize()
    parser = Parser("a")
    parser.tokens.insert(1, parser.tokens[0])
    with pytest.raises(ParseError):
        parser.parse()


def test_more_minimization_edges():
    tautology = BooleanFunction("a|!a")
    contradiction = BooleanFunction("a&!a")
    assert minimize(tautology, "cnf")["result"] == "1"
    assert minimize(contradiction, "dnf")["result"] == "0"
    full = Implicant((None, None), frozenset({0, 1, 2, 3}))
    assert full.dnf(["a", "b"]) == "1"
    assert full.cnf(["a", "b"]) == "0"
    stages, primes = gluing([], 2)
    assert stages == [[]]
    assert primes == []


def test_post_linear_false_path():
    assert is_linear(BooleanFunction("a|b")) is False
