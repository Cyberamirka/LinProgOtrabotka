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
    initial_state = [(node.char, round(node.frequency, 10)) for node in nodes]
    initial_state.sort(key=lambda x: (-x[1], x[0]))  # Сортируем для отображения (от большего к меньшему)
    steps.append(initial_state)

    # Создаем кучу (min-heap)
    heap = []
    for node in nodes:
        heapq.heappush(heap, HuffmanNode(node.char, node.frequency))

    # Процесс построения дерева
    while len(heap) > 1:
        # Берем два наименьших
        # (heapq всегда гарантирует, что мы берем самые маленькие)
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # Создаем новый узел
        new_char = f"{left.char}{right.char}"  # Имя для отладки
        new_freq = left.freq + right.freq

        # Важно: 'left' (меньший) может быть '1', 'right' (больший) '0'
        # или наоборот. Чтобы коды были стабильными (и как в
        # классических примерах), часто делают так:
        # узел с меньшей частотой идет влево (0),
        # с большей - вправо (1).
        # (В коде heapq left/right могут быть не отсортированы,
        # если у них одинаковая частота.
        # Но для самого алгоритма это не важно, он всё равно
        # будет оптимальным.
        # Давайте оставим left=0, right=1 для простоты.)

        new_node = HuffmanNode(new_char, new_freq, left, right)
        heapq.heappush(heap, new_node)

        # --- Сохранение шага для GUI ---
        # Копируем *текущее* состояние кучи
        current_state = []
        temp_heap = heap.copy()
        while temp_heap:
            node = heapq.heappop(temp_heap)
            current_state.append((node.char, round(node.freq, 10)))

        # Сортируем для красивой таблицы (от большего к меньшему)
        current_state.sort(key=lambda x: (-x[1], x[0]))
        steps.append(current_state)
        # ---------------------------------

    # Генерация кодов (без изменений)
    codes = {}

    def _generate_codes(node: HuffmanNode, current_code: str):
        if node is None:
            return
        # Если это "лист" (исходный символ)
        if node.left is None and node.right is None:
            codes[node.char] = current_code if current_code else "0"  # Если всего 1 символ
            return
        # Идем влево (0) и вправо (1)
        _generate_codes(node.left, current_code + '0')
        _generate_codes(node.right, current_code + '1')

    root = heap[0] if heap else None
    _generate_codes(root, '')

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

    # Возвращаем и коды, и ШАГИ
    return code_table, steps
# [file content end]