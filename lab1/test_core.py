import unittest
from core import BitArrayUtils, Converter, IntegerMath, BCD8421


class TestBitArrayUtils(unittest.TestCase):
    def test_create_empty(self):
        arr = BitArrayUtils.create_empty()
        self.assertEqual(len(arr), 32)
        self.assertTrue(all(bit == 0 for bit in arr))

    def test_invert_array(self):
        arr = [0] * 31 + [1]
        inv = BitArrayUtils.invert_array(arr)
        self.assertEqual(inv[31], 0)
        self.assertEqual(inv[0], 1)

    def test_shift_left(self):
        arr = [0] * 31 + [1]
        shifted = BitArrayUtils.shift_left(arr, 2)
        self.assertEqual(shifted[29], 1)
        self.assertEqual(shifted[30], 0)
        self.assertEqual(shifted[31], 0)


class TestConverter(unittest.TestCase):
    def test_dec_to_direct_code_positive(self):
        arr = Converter.dec_to_direct_code("5")
        self.assertEqual(arr[-3:], [1, 0, 1])
        self.assertEqual(arr[0], 0)

    def test_dec_to_direct_code_negative(self):
        arr = Converter.dec_to_direct_code("-5")
        self.assertEqual(arr[-3:], [1, 0, 1])
        self.assertEqual(arr[0], 1)

    def test_dec_to_twos_complement_positive(self):
        arr = Converter.dec_to_twos_complement("5")
        self.assertEqual(arr[-3:], [1, 0, 1])
        self.assertEqual(arr[0], 0)

    def test_twos_complement_to_dec(self):
        dec_str = "-15"
        arr = Converter.dec_to_twos_complement(dec_str)
        self.assertEqual(Converter.twos_complement_to_dec(arr), dec_str)

        dec_pos = "15"
        arr_pos = Converter.dec_to_twos_complement(dec_pos)
        self.assertEqual(Converter.twos_complement_to_dec(arr_pos), dec_pos)

    def test_direct_code_to_dec(self):
        arr1 = Converter.dec_to_direct_code("42")
        self.assertEqual(Converter.direct_code_to_dec(arr1), "42")

        arr2 = Converter.dec_to_direct_code("-42")
        self.assertEqual(Converter.direct_code_to_dec(arr2), "-42")


class TestIntegerMath(unittest.TestCase):
    def test_add_twos_complement(self):
        _, dec_res = IntegerMath.add_twos_complement("10", "-3")
        self.assertEqual(dec_res, "7")

        _, dec_res2 = IntegerMath.add_twos_complement("-20", "-15")
        self.assertEqual(dec_res2, "-35")

    def test_subtract_twos_complement(self):
        _, dec_res = IntegerMath.subtract_twos_complement("10", "15")
        self.assertEqual(dec_res, "-5")

        _, dec_res2 = IntegerMath.subtract_twos_complement("-10", "-15")
        self.assertEqual(dec_res2, "5")

    def test_multiply_direct(self):
        _, dec_res = IntegerMath.multiply_direct("5", "6")
        self.assertEqual(dec_res, "30")

        _, dec_res2 = IntegerMath.multiply_direct("5", "-6")
        self.assertEqual(dec_res2, "-30")

    def test_divide_direct(self):
        _, dec_res = IntegerMath.divide_direct("10", "3")
        self.assertEqual(dec_res, "3.33333")

        _, dec_res2 = IntegerMath.divide_direct("-10", "4")
        self.assertEqual(dec_res2, "-2.50000")

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            IntegerMath.divide_direct("10", "0")


class TestBCD8421(unittest.TestCase):
    def test_add_no_correction(self):
        _, dec_res = BCD8421.add("12", "13")
        self.assertEqual(dec_res, "25")

    def test_add_with_correction(self):
        # 18 + 25 = 43 (вызовет перенос и коррекцию тетрады)
        _, dec_res = BCD8421.add("18", "25")
        self.assertEqual(dec_res, "43")


if __name__ == '__main__':
    unittest.main()