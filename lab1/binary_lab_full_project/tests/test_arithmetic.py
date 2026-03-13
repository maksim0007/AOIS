from arithmetic import add_twos_complement, subtract_twos_complement

def test_add():
    r = add_twos_complement(5,3)
    assert len(r) == 32

def test_sub():
    r = subtract_twos_complement(7,3)
    assert len(r) == 32
