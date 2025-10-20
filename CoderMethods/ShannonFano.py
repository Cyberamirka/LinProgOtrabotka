from collections import defaultdict
import math

# Глобальные переменные для хранения информации о последнем кодировании
last_encoded_string = ""
last_mode = ""              # "1" или "2"
last_compressed_data = None # Для режима 1
last_compressor = None      # Для режима 2 (или для режима 1, если понадобится)

# ==============================
# Кодирование по Шеннону-Фано
# ==============================

# Класс для хранения информации о символе или блоке
class Compress:
    def __init__(self, correspond):
        self.original = correspond
        self.count = 0
        self.code = ""
        self.probability = 0

# Режим 1 – поблочное кодирование
class ShannonFanoCompressionChar:
    def __getProbability(self, compressor):
        return compressor.probability

    def compress_data(self, data):
        processed = set()
        compressor = []
        total_length = len(data)

        for char in data:
            if char not in processed:
                processed.add(char)
                count = data.count(char)
                comp = Compress(char)
                comp.count = count
                comp.probability = count / total_length
                compressor.append(comp)

        # Сортируем по убыванию вероятности
        sorted_compressor = sorted(compressor, key=self.__getProbability, reverse=True)
        split = self.__splitter([i.probability for i in sorted_compressor], pointer=0)
        self.__encoder(sorted_compressor, split)
        return sorted_compressor

    def __splitter(self, probability, pointer):
        if pointer >= len(probability) - 1:
            return pointer
        diff = abs(sum(probability[:pointer + 1]) - sum(probability[pointer + 1:]))
        next_diff = abs(sum(probability[:pointer + 2]) - sum(probability[pointer + 2:]))
        return self.__splitter(probability, pointer + 1) if next_diff < diff else pointer

    def __encoder(self, compressor, split):
        if split >= 0:
            part_1, part_2 = compressor[:split + 1], compressor[split + 1:]
            for i in part_1:
                i.code += '1'
            if len(part_1) > 1:
                self.__encoder(part_1, self.__splitter([i.probability for i in part_1], pointer=0))
            for i in part_2:
                i.code += '0'
            if len(part_2) > 1:
                self.__encoder(part_2, self.__splitter([i.probability for i in part_2], pointer=0))

    def get_table(self, compressed_data):
        headers = ["xi", "pi"] + [str(i + 1) for i in range(max(len(c.code) for c in compressed_data))] + ["qi", "pi*qi", "-pi*log2(pi)"]
        table = []
        total_qavg = total_entropy = 0

        for item in compressed_data:
            qi = len(item.code)
            pi_qi = item.probability * qi
            entropy = -item.probability * math.log2(item.probability)
            total_qavg += pi_qi
            total_entropy += entropy
            table.append([
                item.original,
                f"{item.count}/{sum(c.count for c in compressed_data)}",
                *list(item.code.ljust(len(headers) - 5, ' ')),
                qi,
                f"{pi_qi:.4f}",
                f"{entropy:.4f}"
            ])
        table.append(["", "", *["" for _ in range(len(headers) - 4)], f"{total_qavg:.4f}", f"{total_entropy:.4f}"])
        return table

    def get_encoded_string(self, compressed_data, original_str):
        code_map = {item.original: item.code for item in compressed_data}
        encoded = []
        sorted_keys = sorted(code_map.keys(), key=lambda x: len(x), reverse=True)
        i = 0
        while i < len(original_str):
            for key in sorted_keys:
                if original_str.startswith(key, i):
                    encoded.append(code_map[key])
                    i += len(key)
                    break
            else:
                encoded.append(code_map[original_str[i]])
                i += 1
        return ''.join(encoded)

# Функция декодирования для режима 1
def decode_block(encoded_str, compressed_data):
    code_map = {item.original: item.code for item in compressed_data}
    reversed_code_map = {v: k for k, v in code_map.items()}
    current_code = ""
    decoded = []
    for bit in encoded_str:
        current_code += bit
        if current_code in reversed_code_map:
            decoded.append(reversed_code_map[current_code])
            current_code = ""
    if current_code:
        raise ValueError("Некорректная закодированная строка")
    return ''.join(decoded)

# Режим 2 – посимвольное кодирование
class ShannonFanoCompressionBlock:
    def __init__(self):
        self.code_map = {}
        self.encoded_string = ""

    def __getProbability(self, compressor):
        return compressor.probability

    def compress_data(self, data):
        processed = set()
        compressor = []
        total_length = len(data)

        for char in data:
            if char not in processed:
                processed.add(char)
                count = data.count(char)
                comp = Compress(char)
                comp.count = count
                comp.probability = count / total_length
                compressor.append(comp)

        sorted_compressor = sorted(compressor, key=self.__getProbability, reverse=True)
        split = self.__splitter([i.probability for i in sorted_compressor], pointer=0)
        self.__encoder(sorted_compressor, split)
        self.code_map = {item.original: item.code for item in sorted_compressor}
        self.encoded_string = ''.join([self.code_map[char] for char in data])
        return sorted_compressor

    def __splitter(self, probability, pointer):
        if pointer >= len(probability) - 1:
            return pointer
        diff = abs(sum(probability[:pointer + 1]) - sum(probability[pointer + 1:]))
        next_diff = abs(sum(probability[:pointer + 2]) - sum(probability[pointer + 2:]))
        return self.__splitter(probability, pointer + 1) if next_diff < diff else pointer

    def __encoder(self, compressor, split):
        if split >= 0:
            part_1, part_2 = compressor[:split + 1], compressor[split + 1:]
            for i in part_1:
                i.code += '1'
            if len(part_1) > 1:
                self.__encoder(part_1, self.__splitter([i.probability for i in part_1], pointer=0))
            for i in part_2:
                i.code += '0'
            if len(part_2) > 1:
                self.__encoder(part_2, self.__splitter([i.probability for i in part_2], pointer=0))

    def display_table(self, compressed_data):
        headers = ["xi", "pi"] + [str(i + 1) for i in range(max(len(c.code) for c in compressed_data))] + ["qi", "pi*qi", "-pi*log2(pi)"]
        table = []
        total_qavg = total_entropy = 0

        for item in compressed_data:
            qi = len(item.code)
            pi_qi = item.probability * qi
            entropy = -item.probability * math.log2(item.probability)
            total_qavg += pi_qi
            total_entropy += entropy
            table.append([
                item.original,
                f"{item.count}/{sum(c.count for c in compressed_data)}",
                *list(item.code.ljust(len(headers) - 5, ' ')),
                qi,
                f"{pi_qi:.4f}",
                f"{entropy:.4f}"
            ])
        table.append(["", "", *["" for _ in range(len(headers) - 4)], f"{total_qavg:.4f}", f"{total_entropy:.4f}"])
        return table

    def decode(self, encoded_str):
        reversed_code_map = {v: k for k, v in self.code_map.items()}
        current_code = ""
        decoded = []
        for bit in encoded_str:
            current_code += bit
            if current_code in reversed_code_map:
                decoded.append(reversed_code_map[current_code])
                current_code = ""
        if current_code:
            raise ValueError("Некорректная закодированная строка")
        return ''.join(decoded)

# Функция для поиска повторяющихся блоков (используется в режиме 1)
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