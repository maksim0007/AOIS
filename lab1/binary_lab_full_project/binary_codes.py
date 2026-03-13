BITS = 32

def decimal_to_binary(n, bits=BITS):
    sign = 0
    if n < 0:
        sign = 1
        n = -n

    result = [0] * bits
    i = bits - 1

    while n > 0 and i >= 1:
        result[i] = n % 2
        n //= 2
        i -= 1

    result[0] = sign
    return result


def ones_complement(n):
    b = decimal_to_binary(n)
    if b[0] == 1:
        for i in range(1, len(b)):
            b[i] = 1 - b[i]
    return b


def twos_complement(n):
    b = ones_complement(n)

    if b[0] == 1:
        carry = 1
        for i in range(len(b) - 1, 0, -1):
            s = b[i] + carry
            b[i] = s % 2
            carry = s // 2

    return b


def binary_to_decimal(bits):
    sign = bits[0]
    value = 0
    power = 1

    for i in range(len(bits)-1, 0, -1):
        value += bits[i] * power
        power *= 2

    return -value if sign == 1 else value
