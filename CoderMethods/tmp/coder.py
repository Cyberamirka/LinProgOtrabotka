import math

class Coder:
    def __init__(self):
        self.uniChar = []
        self.uniCharCount = []
        self.codeChar = []
        self.P_i = []


    # формирует для символов код соответствующий каждому символу
    # ВНИМАНИЕ: данный метод не должен быть переопределён т.к. процесс формирования кодов не меняется!
    def _codeForming(self, s: list, code: str):
        # Базовый случай: если список пуст или содержит один элемент
        if len(s) <= 1:
            if s:  # Если список не пуст
                self.codeChar.append(code if code != '-1' else '0')  # Обрабатываем начальное значение -1
            return

        left, right = 0, len(s) - 1
        left_sum = right_sum = 0

        # Разделяем список на две части с примерно равными суммами весов
        while left <= right:
            if left_sum <= right_sum:
                left_sum += self.uniCharCount[self.uniChar.index(s[left])]
                left += 1
            else:
                right_sum += self.uniCharCount[self.uniChar.index(s[right])]
                right -= 1

        # Формируем коды для левой и правой частей
        if code == '-1':
            # Первый вызов: начинаем с '1' и '0'
            self._codeForming(s[:left], '1')
            self._codeForming(s[left:], '0')
        else:
            # Рекурсивные вызовы с добавлением '1' или '0' к текущему коду
            self._codeForming(s[:left], code + '1')
            self._codeForming(s[left:], code + '0')


    # переопределяемый метод
    def coders(self, s: str):
        """
        Принимает на вход строку, и возвращает тоже строку, но уже закодированную в виде последовательности 0 и 1, Шеннона-Фано
        Кодирует полученное сообщение
        """
        pass


    # не переопределяемый метод т.к. процесс декодирования индентичен как и формирования кодов для блоков или символов
    def decoder(self, s: str):
        """
            Декодирует последнее сообщение принимая на себя последовательность 0 и 1,
            но стоит учесть, что на новом сообщений декодирование не пройдёт, т.к. нужно обновлять таблицу!
        """
        tmp = ""
        result = ""
        for i in s:
            tmp += i
            if tmp in self.codeChar:
                result += self.uniChar[self.codeChar.index(tmp)]
                tmp = ""

        return result
