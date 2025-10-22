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

    table: list[CoderNode] = list()
    _sum_count = sum(blocks.values())

    for char, count in blocks.items():
        table.append(CoderNode(char, '', count / _sum_count))

    # СОРТИРОВКА ПО УБЫВАНИЮ ЧАСТОТЫ
    table.sort(key=lambda x: x.frequency, reverse=True)
    return table


def CharPatternFinder(msg: str) -> list[CoderNode]:
    chars = list(set(msg))
    table: list[CoderNode] = list()

    for char in chars:
        table.append(CoderNode(char, '', msg.count(char) / len(msg)))

    # ПРАВИЛЬНАЯ СОРТИРОВКА ПО УБЫВАНИЮ ЧАСТОТЫ
    table.sort(key=lambda x: x.frequency, reverse=True)
    return table


# [file content end]

# [file name]: shannon_fano.py
# [file content begin]
from .CoderTypes import CoderNode, CodeTable


def _shannon_fano_recursive(nodes: list[CoderNode], current_code: str, code_table: CodeTable):
    """Рекурсивно строит коды Шеннона-Фано"""
    if len(nodes) == 1:
        nodes[0].code = current_code
        code_table.table.append(nodes[0])
        return

    if len(nodes) == 0:
        return

    # Находим точку разделения (примерно равные суммы вероятностей)
    total = sum(node.frequency for node in nodes)
    current_sum = 0
    split_index = 0

    for i, node in enumerate(nodes):
        current_sum += node.frequency
        if current_sum >= total / 2:
            split_index = i + 1
            break

    left_group = nodes[:split_index]
    right_group = nodes[split_index:]

    # Левая группа - '0', правая - '1'
    _shannon_fano_recursive(left_group, current_code + '1', code_table)
    _shannon_fano_recursive(right_group, current_code + '0', code_table)


def ShannonFano(nodes: list[CoderNode]) -> CodeTable:
    """Кодирование Шеннона-Фано для готового списка узлов"""
    # Убеждаемся, что узлы отсортированы по убыванию частоты
    # Пузырьковая сортировка по убыванию частоты
    n = len(nodes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nodes[j].frequency < nodes[j + 1].frequency:
                nodes[j], nodes[j + 1] = nodes[j + 1], nodes[j]


    code_table = CodeTable()
    code_table.table = []
    _shannon_fano_recursive(nodes, '', code_table)

    return code_table