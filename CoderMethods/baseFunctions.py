from .CoderTypes import CoderNode, CodeTable

from collections import defaultdict



def BlockPatternFinder(msg: str) -> list[CoderNode]:
    n = len(msg)
    blocks = defaultdict(int)
    def get_all_substrings(s):
        return [s[i:j] for i in range(n) for j in range(i + 1, n + 1)]
    substrings = sorted(get_all_substrings(msg), key=len, reverse=True)
    for substr in substrings:
        if len(substr) < 2:
            continue
        count = msg.count(substr)
        if count > 1:
            blocks[substr] += count
            msg = msg.replace(substr, '')
    for char in msg:
        if char != '':
            blocks[char] += 1

    # создаю таблицу кодов
    table: list[CoderNode] = list()

    _sum_count = sum(blocks.values())

    for i in blocks.keys():
        table.append(CoderNode(i, '', blocks[i] / _sum_count))

    return table



def CharPatternFinder(msg: str) -> list[CoderNode]:
    chars = list(set(msg))
    table: list[CoderNode] = list()

    for i in chars:
        table.append(CoderNode(i, '', msg.count(i) / len(msg)))

    return table




def coder_decoder(code_table: CodeTable, msg: str, decode_mode: bool = False):
    t = {node.char: node.code for node in code_table.table} if hasattr(code_table, 'table') else code_table

    if decode_mode:
        # Декодирование - простой побитовый разбор
        reverse_table = {code: char for char, code in t.items()}
        decoded_message = ''
        current_code = ''

        for bit in msg:
            current_code += bit
            if current_code in reverse_table:
                decoded_message += reverse_table[current_code]
                current_code = ''

        return decoded_message

    else:
        # Кодирование - ищем самый длинный совпадающий блок
        coded_message = ''
        i = 0

        while i < len(msg):
            found_block = None
            # Ищем от самых длинных к коротким (от 6 символов до 1)
            for length in range(min(6, len(msg) - i), 0, -1):  # максимальная длина блока ~6 символов
                block = msg[i:i + length]
                if block in t:
                    found_block = block
                    break

            if found_block:
                coded_message += t[found_block]
                i += len(found_block)
            else:
                # Если не нашли блок - берем один символ (должен быть в таблице)
                coded_message += t[msg[i]]
                i += 1

        return coded_message