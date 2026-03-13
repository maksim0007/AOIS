def digit_to_bcd(d):
    bits = [0,0,0,0]
    i = 3
    while d > 0:
        bits[i] = d % 2
        d //= 2
        i -= 1
    return bits


def bcd_add_8421(a, b):
    a_digits = list(map(int,str(a)))
    b_digits = list(map(int,str(b)))

    a_digits.reverse()
    b_digits.reverse()

    carry = 0
    result = []

    for i in range(max(len(a_digits),len(b_digits))):

        da = a_digits[i] if i < len(a_digits) else 0
        db = b_digits[i] if i < len(b_digits) else 0

        s = da + db + carry

        if s > 9:
            s -= 10
            carry = 1
        else:
            carry = 0

        result.append(digit_to_bcd(s))

    return result
