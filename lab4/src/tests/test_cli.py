from __future__ import annotations

import unittest

from src.cli import Application, run_console
from src.hash_table import DuplicateKeyError


class ApplicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Application()

    def test_load_default_records(self) -> None:
        self.app.load_default_records()
        self.assertTrue(self.app.table.contains("Поэма"))
        self.assertEqual(len(self.app.table.metadata_rows()), 12)

    def test_search_returns_not_found_message(self) -> None:
        self.app.load_default_records()
        self.assertIn("не найдена", self.app.search("Баллада"))

    def test_insert_and_remove_messages(self) -> None:
        self.app.load_default_records()
        insert_message = self.app.insert("Баллада", "Жанр")
        self.assertIn("добавлена", insert_message)
        remove_message = self.app.remove("Баллада")
        self.assertIn("удалена", remove_message)

    def test_show_load_factor_format(self) -> None:
        self.app.load_default_records()
        self.assertTrue(self.app.show_load_factor().startswith("Коэффициент заполнения"))


class ConsoleTests(unittest.TestCase):
    def test_console_flow(self) -> None:
        inputs = iter([
            "1",
            "4", "Поэма",
            "5", "Баллада", "Лиро-эпическое произведение",
            "6", "Баллада",
            "7",
            "0",
        ])
        outputs = []

        run_console(input_func=lambda _: next(inputs), output_func=outputs.append)

        joined = "\n".join(outputs)
        self.assertIn("Демонстрационные данные загружены.", joined)
        self.assertIn("Найдена запись", joined)
        self.assertIn("добавлена", joined)
        self.assertIn("удалена", joined)
        self.assertIn("Коэффициент заполнения", joined)
        self.assertIn("Работа завершена.", joined)

    def test_console_handles_invalid_command(self) -> None:
        inputs = iter(["9", "0"])
        outputs = []

        run_console(input_func=lambda _: next(inputs), output_func=outputs.append)

        self.assertIn("Неизвестная команда.", outputs)

    def test_console_handles_duplicate_error(self) -> None:
        inputs = iter(["1", "5", "Поэма", "Повтор", "0"])
        outputs = []

        run_console(input_func=lambda _: next(inputs), output_func=outputs.append)

        joined = "\n".join(outputs)
        self.assertIn("Ошибка", joined)
        self.assertNotIn(DuplicateKeyError.__name__, joined)


if __name__ == "__main__":
    unittest.main()
