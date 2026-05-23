from __future__ import annotations

from .boolean_function import BooleanFunction
from .kmap import minimize_by_kmap
from .report import generate_report


def process_expression(expression: str) -> str:
    return generate_report(expression)


def print_menu() -> None:
    print("\n===== Лабораторная работа 2 =====")
    print("1. Полный отчет")
    print("2. Только карта Карно для ДНФ")
    print("3. Только карта Карно для КНФ")
    print("4. Ввести новую функцию")
    print("0. Выход")


def ask_expression() -> str:
    return input("Введите логическую функцию: ").strip()


def console_menu() -> None:
    expression = ask_expression()
    while True:
        print_menu()
        choice = input("Выбор: ").strip()
        if choice == "4":
            expression = ask_expression()
            continue
        if choice == "0":
            print("Выход...")
            break
        if choice not in {"1", "2", "3"}:
            print("Неверный пункт меню")
            continue

        try:
            function = BooleanFunction(expression)
            if choice == "1":
                print("\n" + generate_report(expression))
            elif choice == "2":
                print("\n" + minimize_by_kmap(function, "dnf")["table"])
            elif choice == "3":
                print("\n" + minimize_by_kmap(function, "cnf")["table"])
        except Exception as error:
            print(f"Ошибка: {error}")
