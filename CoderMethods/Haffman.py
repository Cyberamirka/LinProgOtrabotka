# [file name]: Haffman.py
# [file content begin]
from .CoderTypes import CoderNode, CodeTable
import heapq
from typing import List, Tuple


class HuffmanNode:
    def __init__(self, char: str, freq: float, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def Huffman(nodes: list[CoderNode]) -> Tuple[CodeTable, List[List[Tuple[str, float]]]]:
    """Кодирование Хаффмана с сохранением шагов для таблицы"""
    if not nodes:
        return CodeTable(), []

    steps = []

    # Начальное состояние
    nodes_list = [(node.char, node.frequency, None, None) for node in nodes]  # (char, freq, left, right)
    nodes_list.sort(key=lambda x: (-x[1], x[0]))  # сортируем по убыванию
    steps.append([(char, round(freq, 10)) for char, freq, _, _ in nodes_list])

    # Работаем с обычным списком
    while len(nodes_list) > 1:
        # Берем два последних (самых маленьких) элемента
        nodes_list.sort(key=lambda x: (-x[1], x[0]))  # всегда сортируем перед взятием
        
        # Последние два элемента - самые маленькие
        left_char, left_freq, left_left, left_right = nodes_list.pop()
        right_char, right_freq, right_left, right_right = nodes_list.pop()
        
        # Создаем новый узел
        new_char = f"{left_char}{right_char}"
        new_freq = left_freq + right_freq
        
        # Добавляем обратно
        nodes_list.append((new_char, new_freq, 
                          (left_char, left_freq, left_left, left_right),
                          (right_char, right_freq, right_left, right_right)))
        
        # Сохраняем шаг
        current_state = [(char, round(freq, 10)) for char, freq, _, _ in nodes_list]
        current_state.sort(key=lambda x: (-x[1], x[0]))  # сортируем для отображения
        steps.append(current_state)

    # Генерация кодов
    codes = {}
    
    def _generate_codes(node_tuple, current_code):
        if node_tuple is None:
            return
        char, freq, left, right = node_tuple
        if left is None and right is None:  # лист
            codes[char] = current_code if current_code else "0"
            return
        _generate_codes(left, current_code + '0')
        _generate_codes(right, current_code + '1')
    
    if nodes_list:
        _generate_codes(nodes_list[0], '')

    # Создаем таблицу кодов
    code_table = CodeTable()
    code_table.table = []
    for original_node in nodes:
        if original_node.char in codes:
            code_table.table.append(CoderNode(
                original_node.char,
                codes[original_node.char],
                original_node.frequency
            ))

    return code_table, steps