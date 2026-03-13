from multiply import multiply_direct
from divide import divide_direct
from bcd import bcd_add_8421

def test_multiply():
    r = multiply_direct(5,3)
    assert isinstance(r,list)

def test_divide():
    integer, frac = divide_direct(13,3)
    assert integer == 4
    assert len(frac) == 5

def test_bcd():
    r = bcd_add_8421(45,27)
    assert len(r) > 0
