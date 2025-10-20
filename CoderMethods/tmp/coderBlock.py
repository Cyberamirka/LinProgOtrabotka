from collections import defaultdict
import math
from tabulate import tabulate

from coder import Coder



class coderBlock(Coder):
    def __init__(self) -> None:
        super().__init__()


    def coders(self, s: str) -> str:
        # =======================================================
        n = len(s)
        blocks = defaultdict(int)
        defS = s

        # Функция для поиска всех подстрок
        def get_all_substrings(s):
            return [s[i:j] for i in range(n) for j in range(i + 1, n + 1)]

        # Получаем все подстроки и сортируем их по длине в порядке убывания
        substrings = sorted(get_all_substrings(s), key=len, reverse=True)

        # Проходим по всем подстрокам и считаем их вхождения
        for substr in substrings:
            if len(substr) < 2:
                continue
            count = s.count(substr)
            if count > 1:
                blocks[substr] += count
                s = s.replace(substr, '')

        # Подсчитываем оставшиеся символы
        for char in s:
            if char != '':
                blocks[char] += 1
        # =========================================================


        # добавляю всё полученное в список uniChar
        for i in blocks.keys():
            self.uniChar.append(i)
            self.uniCharCount.append(blocks[i])
            self.P_i.append(float(blocks[i]) / float(len(blocks)))

        # Сортировка
        for i in range(len(self.uniChar)):
            for j in range(len(self.uniChar) - 1):
                if self.P_i[j] < self.P_i[j + 1]:
                    self.uniCharCount[j], self.uniCharCount[j + 1] = self.uniCharCount[j + 1], self.uniCharCount[j]
                    self.uniChar[j], self.uniChar[j + 1] = self.uniChar[j + 1], self.uniChar[j]
                    self.P_i[j], self.P_i[j + 1] = self.P_i[j + 1], self.P_i[j]

        self._codeForming(self.uniChar, '-1')

        tmp = ''
        result = ''
        i = 0
        while i < len(defS):
            # Пытаемся найти самое длинное совпадение
            for j in range(len(defS), i, -1):
                current_tmp = defS[i:j]
                if current_tmp in self.uniChar:
                    result += self.codeChar[self.uniChar.index(current_tmp)]
                    i = j  # Перемещаем индекс на позицию после найденного слова
                    tmp = ''  # Сбрасываем tmp
                    break
            else:
                # Если не найдено совпадение, добавляем текущий символ к tmp
                tmp += defS[i]
                i += 1

        # Если остались необработанные символы в tmp
        if tmp:
            result += tmp
        
        
        return result