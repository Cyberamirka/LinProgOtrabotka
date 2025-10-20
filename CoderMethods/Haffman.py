from collections import defaultdict, Counter
import math


# ==== Узел дерева Хаффмана ====
class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.char}:{self.freq})"

# ==== Поиск повторяющихся блоков ====
def find_repeated_blocks(s):
    n = len(s)
    blocks = defaultdict(int)

    def get_all_substrings(s):
        return [s[i:j] for i in range(n) for j in range(i + 1, n + 1)]

    substrings = sorted(get_all_substrings(s), key=len, reverse=True)

    for substr in substrings:
        if len(substr) < 2:
            continue
        count = s.count(substr)
        if count > 1:
            blocks[substr] += count
            s = s.replace(substr, '')

    for char in s:
        if char != '':
            blocks[char] += 1

    return blocks

# ==== Преобразование строки в блоковую ====
def convert_to_block_string(s, blocks):
    block_string = []
    i = 0
    while i < len(s):
        for block in blocks:
            if s[i:i+len(block)] == block:
                block_string.append(block)
                i += len(block)
                break
        else:
            block_string.append(s[i])
            i += 1
    return block_string

# ==== Построение дерева Хаффмана ====
def build_huffman_tree(text, blocks=None):
    total = len(text)

    if blocks is None:
        freq = Counter(text)
    else:
        freq = blocks

    print("Исходное сообщение:", ''.join(text), "\n")
    print("Начальные вероятности:")
    for ch, count in sorted(freq.items()):
        print(f"{ch:3} | {count}/{total}")

    nodes = [Node(char=ch, freq=count) for ch, count in freq.items()]
    states = []
    state0 = sorted([(node.char, node.freq) for node in nodes],
                    key=lambda tup: tup[1], reverse=True)
    states.append(state0)

    while len(nodes) > 1:
        nodes.sort(key=lambda node: node.freq, reverse=True)
        n1 = nodes.pop()
        n2 = nodes.pop()
        merged = Node(char=n1.char + n2.char, freq=n1.freq + n2.freq, left=n1, right=n2)
        nodes.append(merged)

        current_state = sorted([(node.char, node.freq) for node in nodes],
                               key=lambda tup: tup[1], reverse=True)
        states.append(current_state)

    return nodes[0], states

# ==== Генерация кодов ====
def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.left is None and node.right is None:
        codebook[node.char] = prefix or "0"
    else:
        if node.left:
            generate_codes(node.left, prefix + "0", codebook)
        if node.right:
            generate_codes(node.right, prefix + "1", codebook)
    return codebook

# ==== Рисование дерева ====
def compute_positions(node, pos=None, x_counter=[0], depth=0):
    if pos is None:
        pos = {}
    if node.left:
        compute_positions(node.left, pos, x_counter, depth+1)
    pos[id(node)] = (x_counter[0], -depth)
    x_counter[0] += 1
    if node.right:
        compute_positions(node.right, pos, x_counter, depth+1)
    return pos

# def draw_tree(root):
#     pos = compute_positions(root)
#     max_x = max(x for x, _ in pos.values())
#     for key in pos:
#         x, y = pos[key]
#         pos[key] = (max_x - x, y)
#
#     fig, ax = plt.subplots(figsize=(8, 6))
#
#     def draw_node(node):
#         x, y = pos[id(node)]
#         circle = plt.Circle((x, y), 0.3, color='lightblue', ec='black', zorder=2)
#         ax.add_patch(circle)
#         label = f"{node.char}\n{node.freq}"
#         ax.text(x, y, label, ha='center', va='center', zorder=3)
#         if node.right:
#             x_r, y_r = pos[id(node.right)]
#             ax.plot([x, x_r], [y, y_r], color='black', zorder=1)
#             ax.text((x + x_r) / 2, (y + y_r) / 2, "1", color='red', fontsize=12, ha='center', va='center')
#             draw_node(node.right)
#         if node.left:
#             x_l, y_l = pos[id(node.left)]
#             ax.plot([x, x_l], [y, y_l], color='black', zorder=1)
#             ax.text((x + x_l) / 2, (y + y_l) / 2, "0", color='red', fontsize=12, ha='center', va='center')
#             draw_node(node.left)
#
#     draw_node(root)
#     ax.set_aspect('equal')
#     ax.axis('off')
#     plt.show()

# ==== Таблица итераций ====
def print_iterations_table(states, total, codes=None):
    num_cols = len(states)
    col_formats = []
    for state in states:
        max_letter_len = max([len(ch) for ch, _ in state] + [len("буква")])
        max_prob_len = max([len(f"{freq}/{total}") for _, freq in state] + [len("P")])
        col_formats.append((max_letter_len, max_prob_len))

    header_cells = [f"{'буква':<{l}} | {'P':<{p}}" for l, p in col_formats]
    header_cells += [f"{'Код':<10}", f"{'qi':<3}", f"{'Pi*qi':<8}", f"{'-Pi*log2(Pi)':<14}"]
    header_line = " | ".join(header_cells)
    print("\n" + header_line)
    print("-" * len(header_line))

    max_rows = max(len(state) for state in states)
    freq = {ch: f for ch, f in states[0]} if codes else {}
    code_items = [(ch, freq[ch], codes[ch]) for ch in freq] if codes else []

    avg_len = 0
    entropy = 0

    for row in range(max(max_rows, len(code_items))):
        row_cells = []
        for col in range(num_cols):
            l, p = col_formats[col]
            if row < len(states[col]):
                ch, f = states[col][row]
                prob = f"{f}/{total}"
                row_cells.append(f"{ch:<{l}} | {prob:<{p}}")
            else:
                row_cells.append(" " * (l + 3 + p))

        if row < len(code_items):
            ch, f, code = code_items[row]
            p_i = f / total
            qi = len(code)
            pi_qi = p_i * qi
            h_i = -p_i * math.log2(p_i) if p_i > 0 else 0
            avg_len += pi_qi
            entropy += h_i
            row_cells += [f"{code:<10}", f"{qi:<3}", f"{pi_qi:<8.4f}", f"{h_i:<14.4f}"]
        else:
            row_cells += [" " * 10, " " * 3, " " * 8, " " * 14]

        print(" | ".join(row_cells))

    if codes:
        total_offset = sum(l + 3 + p for l, p in col_formats)
        print("-" * len(header_line))
        print(" " * total_offset + f"  {'Σ':<10}   {'':<3} {avg_len:<8.4f} {entropy:<14.4f}")
