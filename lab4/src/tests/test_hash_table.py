from __future__ import annotations

import unittest

from src.dataset import DEFAULT_RECORDS
from src.hash_table import (
    DuplicateKeyError,
    HashTable,
    InvalidKeyError,
    TableOverflowError,
)


class HashTableTests(unittest.TestCase):
    def setUp(self) -> None:
        self.table = HashTable(size=20, base_address=0)
        for record in DEFAULT_RECORDS:
            self.table.insert(record.key, record.data)

    def test_numeric_value_uses_first_two_russian_letters(self) -> None:
        self.assertEqual(self.table.numeric_value("Поэма"), 543)
        self.assertEqual(self.table.numeric_value("  П оэма  ".replace(" ", "")), 543)

    def test_hash_address_is_modulo_table_size(self) -> None:
        self.assertEqual(self.table.hash_address("Поэма"), 3)
        self.assertEqual(self.table.hash_address("Роман"), 16)

    def test_collisions_create_chain_of_at_least_three(self) -> None:
        chain = self.table._chain_indexes(3)
        self.assertGreaterEqual(len(chain), 4)
        self.assertEqual(chain[0], 3)
        self.assertTrue(self.table.cells[3].collision)
        self.assertTrue(self.table.cells[chain[-1]].terminal)

    def test_find_returns_expected_record(self) -> None:
        record = self.table.find("Сюжет")
        self.assertIsNotNone(record)
        self.assertEqual(record.data, "Система событий художественного произведения.")

    def test_contains_returns_false_for_absent_key(self) -> None:
        self.assertFalse(self.table.contains("Баллада"))

    def test_insert_duplicate_raises_error(self) -> None:
        with self.assertRaises(DuplicateKeyError):
            self.table.insert("Поэма", "Дубликат")

    def test_insert_new_record_updates_table_and_metadata(self) -> None:
        self.table.insert("Баллада", "Лиро-эпическое стихотворное произведение.")
        self.assertTrue(self.table.contains("Баллада"))
        metadata = {row["key"]: row for row in self.table.metadata_rows()}
        self.assertIn("БАЛЛАДА", metadata)

    def test_remove_single_record(self) -> None:
        self.assertTrue(self.table.remove("Пьеса"))
        self.assertIsNone(self.table.find("Пьеса"))

    def test_remove_middle_record_from_chain_preserves_others(self) -> None:
        self.assertTrue(self.table.remove("Поэзия"))
        self.assertIsNone(self.table.find("Поэзия"))
        self.assertIsNotNone(self.table.find("Поэма"))
        self.assertIsNotNone(self.table.find("Поэт"))
        self.assertIsNotNone(self.table.find("Повесть"))
        chain = self.table._chain_indexes(3)
        self.assertEqual(len(chain), 3)
        self.assertTrue(self.table.cells[chain[-1]].terminal)

    def test_remove_first_record_from_chain_preserves_others(self) -> None:
        self.assertTrue(self.table.remove("Поэма"))
        self.assertIsNone(self.table.find("Поэма"))
        self.assertIsNotNone(self.table.find("Поэзия"))
        self.assertTrue(self.table.cells[3].occupied)

    def test_remove_unknown_key_returns_false(self) -> None:
        self.assertFalse(self.table.remove("Баллада"))

    def test_load_factor_matches_number_of_occupied_rows(self) -> None:
        self.assertAlmostEqual(self.table.load_factor(), len(DEFAULT_RECORDS) / 20)

    def test_display_rows_has_full_table_size(self) -> None:
        rows = self.table.display_rows()
        self.assertEqual(len(rows), 20)
        self.assertEqual(rows[3]["U"], 1)

    def test_pretty_table_contains_header(self) -> None:
        rendered = self.table.pretty_table()
        self.assertIn("№ | ID", rendered)
        self.assertIn("ПОЭМА", rendered)

    def test_pretty_metadata_contains_values(self) -> None:
        rendered = self.table.pretty_metadata()
        self.assertIn("Ключевое слово", rendered)
        self.assertIn("ПОЭМА", rendered)

    def test_invalid_short_key_raises_error(self) -> None:
        with self.assertRaises(InvalidKeyError):
            self.table.insert("Я", "Недопустимо")

    def test_invalid_non_russian_key_raises_error(self) -> None:
        with self.assertRaises(InvalidKeyError):
            self.table.numeric_value("A1")

    def test_table_overflow_raises_error(self) -> None:
        small_table = HashTable(size=2)
        small_table.insert("Поэма", "1")
        small_table.insert("Роман", "2")
        with self.assertRaises(TableOverflowError):
            small_table.insert("Сюжет", "3")

    def test_metadata_rows_are_sorted_by_row(self) -> None:
        rows = self.table.metadata_rows()
        row_numbers = [row["row"] for row in rows]
        self.assertEqual(row_numbers, sorted(row_numbers))

    def test_remove_last_record_from_chain_preserves_head(self) -> None:
        self.assertTrue(self.table.remove("Повесть"))
        self.assertIsNone(self.table.find("Повесть"))
        self.assertTrue(self.table.cells[3].occupied)
        self.assertTrue(self.table.contains("Поэма"))


if __name__ == "__main__":
    unittest.main()
