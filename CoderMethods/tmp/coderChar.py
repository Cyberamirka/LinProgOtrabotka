from coder import Coder

class CoderChar(Coder):
    def __init__(self):
        super().__init__()

    def coders(self, s: str):
        """
        Принимает на вход строку, и возвращает тоже строку, но уже закодированную в виде последовательности 0 и 1, Шеннона-Фано
        Кодирует полученное сообщение
        """

        # Перед каждым кодированием мы очищаем всю таблицу
        self.uniChar.clear()
        self.uniCharCount.clear()
        self.codeChar.clear()
        self.P_i.clear()

        self.uniChar = list(set(s))
        for i in self.uniChar:
            self.uniCharCount.append(s.count(i))

        for i in self.uniCharCount:
            self.P_i.append(i / len(s))

        # Сортировка
        for i in range(len(self.uniChar)):
            for j in range(len(self.uniChar) - 1):
                if self.P_i[j] < self.P_i[j + 1]:
                    self.uniCharCount[j], self.uniCharCount[j + 1] = self.uniCharCount[j + 1], self.uniCharCount[j]
                    self.uniChar[j], self.uniChar[j + 1] = self.uniChar[j + 1], self.uniChar[j]
                    self.P_i[j], self.P_i[j + 1] = self.P_i[j + 1], self.P_i[j]

        # формирую код, первый символ последовательности у нас будет после 1 прохода рекурсии, по этому отправлю туда -1
        self._codeForming(self.uniChar, '-1')

        result = ""
        for i in s:
            result += self.codeChar[ self.uniChar.index(i) ]        

        return result