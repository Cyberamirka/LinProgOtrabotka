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


def calculate_crc(message: str, generator: str = "10011",
                  initial_value: str = "0", reverse_bits: bool = False,
                  final_xor: str = "0") -> Tuple[str, str]:
    """
    Вычисляет CRC для сообщения

    Args:
        message: Исходное сообщение
        generator: Порождающий полином (например "10011")
        initial_value: Начальное значение регистра ("0" или "1")
        reverse_bits: Обратный порядок битов
        final_xor: Дополнительный XOR для финального результата

    Returns:
        Tuple[encoded_message, crc_value]
    """
    # Преобразуем сообщение в биты
    message_bits = string_to_bits(message, reverse_bits)

    # Добавляем нули в конец (длина CRC = len(generator) - 1)
    crc_length = len(generator) - 1
    dividend = message_bits + '0' * crc_length

    # Выполняем деление по модулю 2
    remainder = mod2_division(dividend, generator)

    # Применяем final XOR если нужно
    if final_xor != "0":
        xor_mask = final_xor.zfill(crc_length)
        remainder = ''.join('1' if remainder[i] != xor_mask[i] else '0'
                            for i in range(crc_length))

    # Формируем закодированное сообщение
    encoded_bits = message_bits + remainder
    encoded_message = bits_to_string(encoded_bits, reverse_bits)

    return encoded_message, remainder


def verify_crc(encoded_message: str, generator: str = "10011",
               reverse_bits: bool = False) -> bool:
    """
    Проверяет корректность CRC сообщения

    Returns:
        True если сообщение не содержит ошибок
    """
    # Преобразуем в биты
    encoded_bits = string_to_bits(encoded_message, reverse_bits)

    # Делим на порождающий полином
    remainder = mod2_division(encoded_bits, generator)

    # Если остаток нулевой - ошибок нет
    return all(bit == '0' for bit in remainder)