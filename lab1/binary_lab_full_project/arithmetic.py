from binary_codes import twos_complement, BITS

def add_binary(a, b):
    result = [0] * BITS
    carry = 0

    for i in range(BITS - 1, -1, -1):
        s = a[i] + b[i] + carry
        result[i] = s % 2
        carry = s // 2

    return result


def negate_twos(bits):
    inv = bits[:]

    for i in range(1, len(inv)):
        inv[i] = 1 - inv[i]

    carry = 1
    for i in range(len(inv) - 1, 0, -1):
        s = inv[i] + carry
        inv[i] = s % 2
        carry = s // 2

    return inv


def add_twos_complement(x, y):
    a = twos_complement(x)
    b = twos_complement(y)
    return add_binary(a, b)


def subtract_twos_complement(x, y):
    a = twos_complement(x)
    b = twos_complement(y)
    neg_b = negate_twos(b)
    return add_binary(a, neg_b)
