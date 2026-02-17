class BitArrayUtils:
    """Утилиты для работы с 32-битными массивами (Принцип DRY)"""

    @staticmethod
    def create_empty() -> list[int]:
        return [0] * 32

    @staticmethod
    def add_binary_arrays(a: list[int], b: list[int]) -> list[int]:
        result = BitArrayUtils.create_empty()
        carry = 0
        for i in range(31, -1, -1):
            s = a[i] + b[i] + carry
            result[i] = s % 2
            carry = s // 2
        return result

    @staticmethod
    def invert_array(a: list[int]) -> list[int]:
        return [1 if bit == 0 else 0 for bit in a]

    @staticmethod
    def shift_left(a: list[int], positions: int) -> list[int]:
        if positions == 0: return a[:]
        return a[positions:] + [0] * positions


class Converter:
    """Перевод десятичных чисел в 32-битные массивы и обратно"""

    @staticmethod
    def dec_to_direct_code(dec_str: str) -> list[int]:
        is_negative = dec_str.startswith('-')
        val = int(dec_str[1:]) if is_negative else int(dec_str)

        arr = BitArrayUtils.create_empty()
        arr[0] = 1 if is_negative else 0

        idx = 31
        while val > 0 and idx > 0:
            arr[idx] = val % 2
            val //= 2
            idx -= 1
        return arr

    @staticmethod
    def dec_to_inverse_code(dec_str: str) -> list[int]:
        direct = Converter.dec_to_direct_code(dec_str)
        if direct[0] == 0:
            return direct
        inv = BitArrayUtils.invert_array(direct)
        inv[0] = 1
        return inv

    @staticmethod
    def dec_to_twos_complement(dec_str: str) -> list[int]:
        direct = Converter.dec_to_direct_code(dec_str)
        if direct[0] == 0:
            return direct
        inv = Converter.dec_to_inverse_code(dec_str)
        one = BitArrayUtils.create_empty()
        one[31] = 1
        return BitArrayUtils.add_binary_arrays(inv, one)

    @staticmethod
    def twos_complement_to_dec(arr: list[int]) -> str:
        if arr[0] == 0:
            return str(Converter._bin_to_abs_dec(arr))

        # Исправленный блок: инвертируем и прибавляем 1 для получения модуля
        inv = BitArrayUtils.invert_array(arr)
        one = BitArrayUtils.create_empty()
        one[31] = 1
        direct_abs = BitArrayUtils.add_binary_arrays(inv, one)

        return "-" + str(Converter._bin_to_abs_dec(direct_abs))

    @staticmethod
    def direct_code_to_dec(arr: list[int]) -> str:
        val = str(Converter._bin_to_abs_dec(arr))
        return "-" + val if arr[0] == 1 and val != "0" else val

    @staticmethod
    def _bin_to_abs_dec(arr: list[int]) -> int:
        val = 0
        multiplier = 1
        for i in range(31, 0, -1):
            val += arr[i] * multiplier
            multiplier *= 2
        return val


class IntegerMath:
    """Арифметика целых чисел"""

    @staticmethod
    def add_twos_complement(a_dec: str, b_dec: str) -> tuple[list[int], str]:
        a = Converter.dec_to_twos_complement(a_dec)
        b = Converter.dec_to_twos_complement(b_dec)
        result = BitArrayUtils.add_binary_arrays(a, b)
        return result, Converter.twos_complement_to_dec(result)

    @staticmethod
    def subtract_twos_complement(a_dec: str, b_dec: str) -> tuple[list[int], str]:
        b_neg_dec = b_dec[1:] if b_dec.startswith('-') else '-' + b_dec
        return IntegerMath.add_twos_complement(a_dec, b_neg_dec)

    @staticmethod
    def multiply_direct(a_dec: str, b_dec: str) -> tuple[list[int], str]:
        a = Converter.dec_to_direct_code(a_dec)
        b = Converter.dec_to_direct_code(b_dec)

        result = BitArrayUtils.create_empty()
        result[0] = a[0] ^ b[0]  # Знак: XOR знаковых битов

        # Умножение сдвигом
        for i in range(31, 0, -1):
            if b[i] == 1:
                shift_amount = 31 - i
                shifted_a = BitArrayUtils.shift_left(a, shift_amount)
                shifted_a[0] = 0  # Убираем знак при сложении модулей
                result = BitArrayUtils.add_binary_arrays(result, shifted_a)

        result[0] = a[0] ^ b[0]  # Восстанавливаем знак
        return result, Converter.direct_code_to_dec(result)

    @staticmethod
    def divide_direct(a_dec: str, b_dec: str) -> tuple[str, str]:
        """Деление с точностью до 5 знаков (возвращает строки для дробных частей)"""
        num_a = int(a_dec)
        num_b = int(b_dec)

        if num_b == 0:
            raise ValueError("Division by zero")

        sign = "-" if (num_a < 0) ^ (num_b < 0) else ""
        abs_a, abs_b = abs(num_a), abs(num_b)

        integer_part = abs_a // abs_b
        remainder = abs_a % abs_b

        fractional_part = ""
        for _ in range(5):  # Точность 5 знаков
            remainder *= 10
            fractional_part += str(remainder // abs_b)
            remainder %= abs_b

        dec_res = f"{sign}{integer_part}.{fractional_part}"
        bin_res = f"Sign: {1 if sign == '-' else 0}, Int_Bin: {bin(integer_part)[2:]}, Frac: .{fractional_part}"
        return bin_res, dec_res


class BCD8421:
    """Арифметика в Двоично-десятичном коде 8421"""

    @staticmethod
    def add(a_dec: str, b_dec: str) -> tuple[list[int], str]:
        a_arr = BCD8421._dec_to_bcd(a_dec)
        b_arr = BCD8421._dec_to_bcd(b_dec)

        result = BitArrayUtils.create_empty()
        carry = 0

        for i in range(7, -1, -1):
            start = i * 4
            val_a = sum(a_arr[start + j] * (2 ** (3 - j)) for j in range(4))
            val_b = sum(b_arr[start + j] * (2 ** (3 - j)) for j in range(4))
            s = val_a + val_b + carry

            if s > 9:
                s += 6  # Коррекция 8421 BCD
                carry = 1
            else:
                carry = 0

            for j in range(3, -1, -1):
                result[start + j] = s % 2
                s //= 2

        return result, BCD8421._bcd_to_dec(result)

    @staticmethod
    def _dec_to_bcd(dec_str: str) -> list[int]:
        arr = BitArrayUtils.create_empty()
        dec_str = dec_str.lstrip('-').zfill(8)
        for i, digit in enumerate(dec_str[-8:]):
            val = int(digit)
            start = i * 4
            for j in range(3, -1, -1):
                arr[start + j] = val % 2
                val //= 2
        return arr

    @staticmethod
    def _bcd_to_dec(arr: list[int]) -> str:
        res = ""
        for i in range(8):
            start = i * 4
            val = sum(arr[start + j] * (2 ** (3 - j)) for j in range(4))
            res += str(val)
        return res.lstrip('0') or '0'


# ==========================================
# Тестирование работы алгоритмов
# ==========================================
if __name__ == "__main__":
    def print_res(name, bin_arr, dec_val):
        bin_str = "".join(map(str, bin_arr)) if isinstance(bin_arr, list) else bin_arr
        print(f"{name}:\nBin: {bin_str}\nDec: {dec_val}\n")


    print("--- 1. Дополнительный код: Сложение ---")
    bin_res, dec_res = IntegerMath.add_twos_complement("-15", "10")
    print_res("-15 + 10", bin_res, dec_res)

    print("--- 2. Дополнительный код: Вычитание ---")
    bin_res, dec_res = IntegerMath.subtract_twos_complement("10", "25")
    print_res("10 - 25", bin_res, dec_res)

    print("--- 3. Прямой код: Умножение ---")
    bin_res, dec_res = IntegerMath.multiply_direct("5", "-6")
    print_res("5 * (-6)", bin_res, dec_res)

    print("--- 4. Прямой код: Деление ---")
    bin_res, dec_res = IntegerMath.divide_direct("10", "3")
    print_res("10 / 3 (5 decimal places)", bin_res, dec_res)

    print("--- 5. BCD 8421: Сложение ---")
    bin_res, dec_res = BCD8421.add("18", "25")
    print_res("18 + 25 in BCD", bin_res, dec_res)