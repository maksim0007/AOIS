from __future__ import annotations

from typing import Callable, Dict

from src.dataset import DEFAULT_RECORDS
from src.hash_table import DuplicateKeyError, HashTable, HashTableError


class Application:
    def __init__(self) -> None:
        self.table = HashTable(size=20, base_address=0)

    def load_default_records(self) -> None:
        for record in DEFAULT_RECORDS:
            if not self.table.contains(record.key):
                self.table.insert(record.key, record.data)

    def show_table(self) -> str:
        return self.table.pretty_table()

    def show_metadata(self) -> str:
        return self.table.pretty_metadata()

    def show_load_factor(self) -> str:
        return f"Коэффициент заполнения: {self.table.load_factor():.2f}"

    def search(self, key: str) -> str:
        result = self.table.find(key)
        if result is None:
            return f"Запись с ключом '{key}' не найдена."
        return f"Найдена запись: {result.key} -> {result.data}"

    def insert(self, key: str, data: str) -> str:
        index = self.table.insert(key, data)
        return f"Запись добавлена в строку {index}."

    def remove(self, key: str) -> str:
        removed = self.table.remove(key)
        if not removed:
            return f"Запись с ключом '{key}' не найдена."
        return f"Запись '{key}' удалена."


MENU = """
1. Загрузить демонстрационные записи (вариант 6: Литература)
2. Показать хеш-таблицу
3. Показать V(K), h(V) и строки размещения
4. Найти запись по ключу
5. Добавить запись
6. Удалить запись
7. Показать коэффициент заполнения
0. Выход
""".strip()


def run_console(input_func: Callable[[str], str] = input, output_func: Callable[[str], None] = print) -> None:
    app = Application()
    def load_defaults() -> None:
        app.load_default_records()
        output_func("Демонстрационные данные загружены.")

    actions: Dict[str, Callable[[], None]] = {
        "1": load_defaults,
        "2": lambda: output_func(app.show_table()),
        "3": lambda: output_func(app.show_metadata()),
        "4": lambda: output_func(app.search(input_func("Введите ключ: "))),
        "5": lambda: output_func(app.insert(input_func("Введите ключ: "), input_func("Введите данные: "))),
        "6": lambda: output_func(app.remove(input_func("Введите ключ: "))),
        "7": lambda: output_func(app.show_load_factor()),
    }

    while True:
        output_func(MENU)
        command = input_func("Выберите пункт меню: ").strip()
        if command == "0":
            output_func("Работа завершена.")
            break
        action = actions.get(command)
        if action is None:
            output_func("Неизвестная команда.")
            continue
        try:
            action()
        except (HashTableError, ValueError) as error:
            output_func(f"Ошибка: {error}")


if __name__ == "__main__":
    run_console()
