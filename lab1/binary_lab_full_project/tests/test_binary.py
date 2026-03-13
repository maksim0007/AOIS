from binary_codes import decimal_to_binary, twos_complement, binary_to_decimal

def test_decimal_to_binary():
    b = decimal_to_binary(6)
    assert b[-1] == 0
    assert b[-2] == 1
    assert b[-3] == 1

def test_twos_complement():
    b = twos_complement(-3)
    assert b[0] == 1

def test_binary_to_decimal():
    b = decimal_to_binary(9)
    assert binary_to_decimal(b) == 9
