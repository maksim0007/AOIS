def divide_direct(x, y, precision=5):
    if y == 0:
        raise ZeroDivisionError("division by zero")

    sign = -1 if (x < 0) ^ (y < 0) else 1

    x = abs(x)
    y = abs(y)

    integer = x // y
    remainder = x % y

    frac = []

    for _ in range(precision):
        remainder *= 10
        digit = remainder // y
        frac.append(digit)
        remainder %= y

    return sign * integer, frac
