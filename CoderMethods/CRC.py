from .CoderTypes import CodeTable, CoderNode
from typing import Tuple


def string_to_bits(message: str, reverse_bits: bool = False) -> str:
    """Преобразует строку в битовую последовательность"""
    bits = ""
    for char in message:
        char_bits = format(ord(char), '08b')
        if reverse_bits:
            char_bits = char_bits[::-1]
        bits += char_bits
    return bits


def bits_to_string(bits: str, reverse_bits: bool = False) -> str:
    """Преобразует битовую последовательность обратно в строку"""
    result = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if reverse_bits:
            byte = byte[::-1]
        result += chr(int(byte, 2))
    return result


def mod2_division(dividend: str, divisor: str) -> str:
    """Деление по модулю 2 (XOR)"""
    divisor_len = len(divisor)
    dividend = list(dividend)

    for i in range(len(dividend) - divisor_len + 1):
        if dividend[i] == '1':
            for j in range(divisor_len):
                dividend[i + j] = '1' if dividend[i + j] != divisor[j] else '0'

    return ''.join(dividend)[-divisor_len + 1:]


def calculate_crc_value(message_bits: str, generator: str = "10011") -> str:
    """Вычисляет CRC значение или возвращает пустоту если отключено"""
    if generator == "1":  # специальное значение для "CRC отключен"
        return ""  # пустая строка - CRC не добавляется
    
    crc_length = len(generator) - 1
    dividend = message_bits + '0' * crc_length
    remainder = mod2_division(dividend, generator)
    return remainder


def verify_crc_for_bits(encoded_bits: str, generator: str = "10011") -> bool:
    """
    Проверяет CRC для готовой битовой последовательности
    """
    remainder = mod2_division(encoded_bits, generator)
    return all(bit == '0' for bit in remainder)