def binary_to_polynomial(binary_string):
    coefficients = [int(bit) for bit in binary_string.replace(" ", "")]
    first_non_zero_index = next((i for i, coeff in enumerate(coefficients) if coeff == 1), len(coefficients))
    coefficients = coefficients[first_non_zero_index:]
    degree = len(coefficients) - 1

    polynomial_terms = []
    for i, coeff in enumerate(coefficients):
        if coeff == 1:
            polynomial_terms.append(f"x^{degree - i}" if degree - i > 0 else "1")

    polynomial = " + ".join(polynomial_terms)
    vector = ''.join(map(str, coefficients))
    return polynomial, vector

def mod2_division(dividend, divisor):
    dividend = [int(bit) for bit in dividend]
    divisor = [int(bit) for bit in divisor]
    len_divisor = len(divisor)

    remainder = dividend[:]
    for i in range(len(dividend) - len_divisor + 1):
        if remainder[i] == 1:
            for j in range(len_divisor):
                remainder[i + j] ^= divisor[j]
    return remainder[-(len_divisor - 1):]

def verify_crc(message, crc, generator):
    full_message = message + crc
    remainder = mod2_division(full_message, generator)
    return all(bit == 0 for bit in remainder)

generators = {
    "1": "100101",
    "2": "101001",
    "3": "110101",
    "4": "1000011",
    "5": "100000111",
    "6": "100110001",
    "7": "100011101",
    "8": "111010101",
    "9": "101110000101",
    "10": "11000000000000101",
    "11": "10011"
}