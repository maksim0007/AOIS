from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_INDEX = {letter: index for index, letter in enumerate(RUSSIAN_ALPHABET)}


@dataclass(frozen=True)
class Record:
    key: str
    data: str


@dataclass
class Cell:
    key: str = ""
    collision: bool = False
    occupied: bool = False
    terminal: bool = False
    link: bool = False
    deleted: bool = False
    overflow_pointer: Optional[int] = None
    data_pointer: str = ""
    home_index: Optional[int] = None

    def clear(self) -> None:
        self.key = ""
        self.collision = False
        self.occupied = False
        self.terminal = False
        self.link = False
        self.deleted = False
        self.overflow_pointer = None
        self.data_pointer = ""
        self.home_index = None


class HashTableError(Exception):
    pass


class DuplicateKeyError(HashTableError):
    pass


class TableOverflowError(HashTableError):
    pass


class InvalidKeyError(HashTableError):
    pass


class HashTable:
    def __init__(self, size: int = 20, base_address: int = 0) -> None:
        if size < 1:
            raise ValueError("Размер таблицы должен быть положительным")
        self.size = size
        self.base_address = base_address
        self.cells: List[Cell] = [Cell() for _ in range(size)]
        self.records_metadata: Dict[str, Tuple[int, int]] = {}

    @staticmethod
    def normalize_key(key: str) -> str:
        normalized = " ".join(key.strip().upper().split())
        if len(normalized) < 2:
            raise InvalidKeyError("Ключевое слово должно содержать минимум 2 буквы")
        return normalized

    @staticmethod
    def _first_two_letters(key: str) -> str:
        letters = []
        for character in HashTable.normalize_key(key):
            if character in ALPHABET_INDEX:
                letters.append(character)
            if len(letters) == 2:
                break
        if len(letters) < 2:
            raise InvalidKeyError("В ключевом слове должны быть как минимум две русские буквы")
        return "".join(letters)

    def numeric_value(self, key: str) -> int:
        letters = self._first_two_letters(key)
        return ALPHABET_INDEX[letters[0]] * len(RUSSIAN_ALPHABET) + ALPHABET_INDEX[letters[1]]

    def hash_address(self, key: str) -> int:
        return self.base_address + (self.numeric_value(key) % self.size)

    def _physical_index(self, address: int) -> int:
        return (address - self.base_address) % self.size

    def _home_index(self, key: str) -> int:
        return self._physical_index(self.hash_address(key))

    def _find_free_index(self, start_index: int) -> int:
        for step in range(self.size):
            index = (start_index + step) % self.size
            if not self.cells[index].occupied:
                return index
        raise TableOverflowError("Хеш-таблица переполнена")

    def _find_predecessor_index(self, home_index: int, target_index: int) -> Optional[int]:
        chain = self._chain_indexes(home_index)
        for index in chain:
            if self.cells[index].terminal:
                continue
            if self.cells[index].overflow_pointer == target_index:
                return index
        return None

    def _chain_indexes(self, home_index: int) -> List[int]:
        first = self.cells[home_index]
        if not first.occupied or first.home_index != home_index:
            return []
        indexes = [home_index]
        current_index = home_index
        while not self.cells[current_index].terminal:
            next_index = self.cells[current_index].overflow_pointer
            if next_index is None:
                break
            indexes.append(next_index)
            current_index = next_index
        return indexes

    def _rebuild_chain_flags(self, home_index: int) -> None:
        indexes = self._chain_indexes(home_index)
        if not indexes:
            return
        for position, index in enumerate(indexes):
            cell = self.cells[index]
            cell.home_index = home_index
            cell.deleted = False
            cell.link = False
            if len(indexes) == 1:
                cell.collision = False
                cell.terminal = True
                cell.overflow_pointer = home_index
            else:
                cell.collision = position == 0
                cell.terminal = position == len(indexes) - 1
                if cell.terminal:
                    cell.overflow_pointer = home_index
                else:
                    cell.overflow_pointer = indexes[position + 1]

    def contains(self, key: str) -> bool:
        return self.find(key) is not None

    def find(self, key: str) -> Optional[Record]:
        normalized = self.normalize_key(key)
        home_index = self._home_index(normalized)
        chain = self._chain_indexes(home_index)
        for index in chain:
            cell = self.cells[index]
            if cell.key == normalized and cell.occupied and not cell.deleted:
                return Record(cell.key, cell.data_pointer)
        return None

    def insert(self, key: str, data: str) -> int:
        normalized = self.normalize_key(key)
        if self.contains(normalized):
            raise DuplicateKeyError(f"Ключ '{normalized}' уже существует")

        value = self.numeric_value(normalized)
        address = self.hash_address(normalized)
        home_index = self._physical_index(address)
        home_cell = self.cells[home_index]

        if not home_cell.occupied:
            home_cell.key = normalized
            home_cell.data_pointer = data
            home_cell.occupied = True
            home_cell.deleted = False
            home_cell.home_index = home_index
            self._rebuild_chain_flags(home_index)
        else:
            if home_cell.home_index != home_index:
                foreign_home_index = home_cell.home_index
                if foreign_home_index is None:
                    raise HashTableError("Обнаружена поврежденная строка таблицы")
                free_index = self._find_free_index(home_index)
                moved_cell = self.cells[free_index]
                moved_cell.key = home_cell.key
                moved_cell.collision = home_cell.collision
                moved_cell.occupied = home_cell.occupied
                moved_cell.terminal = home_cell.terminal
                moved_cell.link = home_cell.link
                moved_cell.deleted = home_cell.deleted
                moved_cell.overflow_pointer = home_cell.overflow_pointer
                moved_cell.data_pointer = home_cell.data_pointer
                moved_cell.home_index = home_cell.home_index

                predecessor_index = self._find_predecessor_index(foreign_home_index, home_index)
                if predecessor_index is None:
                    raise HashTableError("Не удалось восстановить цепочку коллизий")
                self.cells[predecessor_index].overflow_pointer = free_index
                home_cell.clear()
                self._rebuild_chain_flags(foreign_home_index)

            if not home_cell.occupied:
                home_cell.key = normalized
                home_cell.data_pointer = data
                home_cell.occupied = True
                home_cell.deleted = False
                home_cell.home_index = home_index
                self._rebuild_chain_flags(home_index)
            else:
                free_index = self._find_free_index(home_index)
                new_cell = self.cells[free_index]
                new_cell.key = normalized
                new_cell.data_pointer = data
                new_cell.occupied = True
                new_cell.deleted = False
                new_cell.home_index = home_index

                chain = self._chain_indexes(home_index)
                tail_index = chain[-1]
                tail_cell = self.cells[tail_index]
                tail_cell.terminal = False
                tail_cell.overflow_pointer = free_index
                self._rebuild_chain_flags(home_index)

        self.records_metadata[normalized] = (value, address)
        return home_index if not home_cell.occupied else self._find_index_by_key(normalized)

    def _find_index_by_key(self, normalized_key: str) -> int:
        home_index = self._home_index(normalized_key)
        for index in self._chain_indexes(home_index):
            if self.cells[index].key == normalized_key:
                return index
        raise KeyError(normalized_key)

    def remove(self, key: str) -> bool:
        normalized = self.normalize_key(key)
        home_index = self._home_index(normalized)
        chain = self._chain_indexes(home_index)
        if not chain:
            return False

        records_to_keep: List[Record] = []
        found = False
        indexes_to_clear: List[int] = []
        for index in chain:
            cell = self.cells[index]
            indexes_to_clear.append(index)
            if cell.key == normalized and cell.occupied and not cell.deleted:
                found = True
                continue
            records_to_keep.append(Record(cell.key, cell.data_pointer))

        if not found:
            return False

        for index in indexes_to_clear:
            self.cells[index].clear()
        self.records_metadata.pop(normalized, None)
        for record in records_to_keep:
            self.insert(record.key, record.data)
        return True

    def load_factor(self) -> float:
        occupied_count = sum(1 for cell in self.cells if cell.occupied)
        return occupied_count / self.size

    def display_rows(self) -> List[Dict[str, object]]:
        rows: List[Dict[str, object]] = []
        for index, cell in enumerate(self.cells):
            rows.append(
                {
                    "row": index,
                    "ID": cell.key,
                    "C": int(cell.collision),
                    "U": int(cell.occupied),
                    "T": int(cell.terminal),
                    "L": int(cell.link),
                    "D": int(cell.deleted),
                    "Po": "" if cell.overflow_pointer is None else cell.overflow_pointer,
                    "Pi": cell.data_pointer,
                    "home_index": "" if cell.home_index is None else cell.home_index,
                }
            )
        return rows

    def metadata_rows(self) -> List[Dict[str, object]]:
        result: List[Dict[str, object]] = []
        for index, cell in enumerate(self.cells):
            if not cell.occupied:
                continue
            value, address = self.records_metadata[cell.key]
            result.append(
                {
                    "key": cell.key,
                    "V": value,
                    "h": address,
                    "row": index,
                    "data": cell.data_pointer,
                }
            )
        return sorted(result, key=lambda item: int(item["row"]))

    def pretty_table(self) -> str:
        header = (
            "№ | ID               | C | U | T | L | D | Po | Дом | Данные\n"
            "-" * 74
        )
        lines = [header]
        for row in self.display_rows():
            lines.append(
                f"{row['row']:>2} | "
                f"{str(row['ID'])[:16]:<16} | "
                f"{row['C']:>1} | {row['U']:>1} | {row['T']:>1} | {row['L']:>1} | {row['D']:>1} | "
                f"{str(row['Po']):>2} | {str(row['home_index']):>3} | {row['Pi']}"
            )
        return "\n".join(lines)

    def pretty_metadata(self) -> str:
        header = "Ключевое слово | V | h | № строки | Данные\n" + "-" * 74
        lines = [header]
        for row in self.metadata_rows():
            lines.append(
                f"{row['key'][:20]:<20} | {row['V']:<3} | {row['h']:<3} | {row['row']:<8} | {row['data']}"
            )
        return "\n".join(lines)
