from binary_codes import decimal_to_binary

def multiply_direct(x, y):
    sign = 1 if (x < 0) ^ (y < 0) else 0

    x = abs(x)
    y = abs(y)

    a = decimal_to_binary(x)
    b = decimal_to_binary(y)

    a = a[1:]
    b = b[1:]

    result = [0] * len(a)

    for i in range(len(b)-1, -1, -1):
        if b[i] == 1:
            shift = len(b)-1-i
            for j in range(len(a)):
                k = j-shift
                if 0 <= k < len(result):
                    result[k] ^= a[j]

    return [sign] + result
