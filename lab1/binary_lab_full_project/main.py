from binary_codes import decimal_to_binary, twos_complement, binary_to_decimal
from arithmetic import add_twos_complement, subtract_twos_complement
from multiply import multiply_direct
from divide import divide_direct
from bcd import bcd_add_8421

print("=== Binary Lab Demo ===")

print("13 -> binary:", decimal_to_binary(13))
print("-5 two's complement:", twos_complement(-5))

print("5 + 3:", add_twos_complement(5,3))
print("7 - 3:", subtract_twos_complement(7,3))

print("Multiply 5*3:", multiply_direct(5,3))

print("Divide 13/3:", divide_direct(13,3))

print("BCD 45 + 27:", bcd_add_8421(45,27))
