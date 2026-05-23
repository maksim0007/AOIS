from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .ast_nodes import And, Const, Equivalence, Implication, Node, Not, Or, Var

ALLOWED_VARIABLES = {"a", "b", "c", "d", "e"}
REPLACEMENTS = {
    "¬": "!",
    "∧": "&",
    "∨": "|",
    "→": "->",
    "↔": "~",
}


class ParseError(ValueError):
    pass


@dataclass(frozen=True)
class Token:
    kind: str
    value: str


class Lexer:
    def __init__(self, text: str):
        normalized = "".join(text.split())
        for source, target in REPLACEMENTS.items():
            normalized = normalized.replace(source, target)
        self.text = normalized
        self.pos = 0

    def tokenize(self) -> List[Token]:
        result: List[Token] = []
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if self.text.startswith("->", self.pos):
                result.append(Token("OP", "->"))
                self.pos += 2
            elif ch in "()!&|~":
                result.append(Token(ch, ch))
                self.pos += 1
            elif ch in "01":
                result.append(Token("CONST", ch))
                self.pos += 1
            elif ch.isalpha():
                name = ch.lower()
                if name not in ALLOWED_VARIABLES:
                    raise ParseError("Допустимы только переменные a, b, c, d, e")
                result.append(Token("VAR", name))
                self.pos += 1
            else:
                raise ParseError(f"Недопустимый символ: {ch}")
        result.append(Token("EOF", ""))
        return result


class Parser:
    def __init__(self, text: str):
        self.tokens = Lexer(text).tokenize()
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def eat(self, kind: str, value: str | None = None) -> Token:
        token = self.current()
        if token.kind != kind:
            raise ParseError(f"Ожидался токен {kind}, получен {token.kind}")
        if value is not None and token.value != value:
            raise ParseError(f"Ожидался токен {value}, получен {token.value}")
        self.pos += 1
        return token

    def parse(self) -> Node:
        if self.current().kind == "EOF":
            raise ParseError("Пустое выражение")
        expression = self.parse_equivalence()
        self.eat("EOF")
        if len(expression.variables()) > 5:
            raise ParseError("Допускается не более 5 переменных")
        return expression

    def parse_equivalence(self) -> Node:
        node = self.parse_implication()
        while self.current().kind == "~":
            self.eat("~")
            node = Equivalence(node, self.parse_implication())
        return node

    def parse_implication(self) -> Node:
        node = self.parse_or()
        while self.current().kind == "OP" and self.current().value == "->":
            self.eat("OP", "->")
            node = Implication(node, self.parse_or())
        return node

    def parse_or(self) -> Node:
        node = self.parse_and()
        while self.current().kind == "|":
            self.eat("|")
            node = Or(node, self.parse_and())
        return node

    def parse_and(self) -> Node:
        node = self.parse_unary()
        while self.current().kind == "&":
            self.eat("&")
            node = And(node, self.parse_unary())
        return node

    def parse_unary(self) -> Node:
        token = self.current()
        if token.kind == "!":
            self.eat("!")
            return Not(self.parse_unary())
        if token.kind == "(":
            self.eat("(")
            expression = self.parse_equivalence()
            self.eat(")")
            return expression
        if token.kind == "VAR":
            return Var(self.eat("VAR").value)
        if token.kind == "CONST":
            return Const(int(self.eat("CONST").value))
        raise ParseError(f"Неожиданный токен: {token.value or token.kind}")


def parse_expression(text: str) -> Node:
    return Parser(text).parse()
