def get_sign_bit(decimal):
    if decimal < 0:
        return '1'
    else:
        return '0'

def get_exponent_bits(binary):
    if '.' in binary:
        integer_bits, fractional_bits = binary.split('.')
        if integer_bits != '0':
            exponent = len(integer_bits) - 1
        else:
            exponent = -len(fractional_bits.split('1')[0]) - 1
    else:
        exponent = len(binary) - 1

    exponent += 127

    exponent_bits = ''
    for i in range(8):
        if exponent >= 2**(7-i):
            exponent_bits += '1'
            exponent -= 2**(7-i)
        else:
            exponent_bits += '0'

    return exponent_bits

def get_mantissa_bits(binary):
    if '.' in binary:
        integer_bits, fractional_bits = binary.split('.')
        binary = integer_bits + fractional_bits
    else:
        binary = binary.rstrip('0')

    mantissa_bits = binary[1:24]

    if len(mantissa_bits) == 23:
        last_bit = int(mantissa_bits[-1])
        second_last_bit = int(mantissa_bits[-2])
        if last_bit == 1 and second_last_bit == 1:
            mantissa_bits = mantissa_bits[:-1] + '0'
        elif last_bit == 1 or second_last_bit == 1:
            mantissa_bits = mantissa_bits[:-1] + '1'

    return mantissa_bits

def decimaltobinary(decimal):
    if isinstance(decimal, int):
        decimal = float(decimal)
    sign_bit = get_sign_bit(decimal)

    integer_part = int(abs(decimal))
    fractional_part = float('0.' + str(abs(decimal)).split('.')[1])

    binary = ''
    if integer_part > 0:
        while integer_part > 0:
            binary = str(integer_part % 2) + binary
            integer_part //= 2
    else:
        binary = '0'

    binary += '.'
    while fractional_part > 0 and len(binary) < 25:
        fractional_part *= 2
        if fractional_part >= 1:
            binary += '1'
            fractional_part -= 1
        else:
            binary += '0'

    exponent_bits = get_exponent_bits(binary)
    mantissa_bits = get_mantissa_bits(binary)

    mantissa_bits = mantissa_bits.ljust(23, '0')

    return sign_bit + exponent_bits + mantissa_bits



print("Witaj! Oto twoje liczby.")
print(decimaltobinary(31.34))
print(decimaltobinary(123.456))
print(decimaltobinary(-123.456))
print(decimaltobinary(997))
print(decimaltobinary(1.01))
print(decimaltobinary(112))