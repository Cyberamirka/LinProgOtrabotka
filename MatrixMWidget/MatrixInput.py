from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import QSize, Qt

FIXED_SIZE = QSize(50, 50)
ALIGNMENT = Qt.AlignmentFlag.AlignRight
SPACE = 3

# матрица
class MatrixInput(QVBoxLayout):
    def __init__(self, parent: QWidget|None = None, row: int = 2, column: int = 2):
        super().__init__(parent)
        self.setSpacing(SPACE)

        self.column = row
        self.row = column

        self.__tmp_box: QHBoxLayout
        for i in range(self.row):
            self.__tmp_box = QHBoxLayout()
            self.__tmp_box.setSpacing(SPACE)
            widget = QLabel()
            widget.setFixedSize(FIXED_SIZE)
            self.__tmp_box.addWidget(widget)

            for j in range(self.column):
                widget = QLineEdit()
                widget.setFixedSize(FIXED_SIZE)
                self.__tmp_box.addWidget(widget)

            self.__tmp_box.update()
            self.__tmp_box.invalidate()
            self.addLayout(self.__tmp_box)

    # +1 столбец
    def add_column(self):
        for i in range(self.count()):
            layout: QHBoxLayout = self.itemAt(i).layout()
            widget = QLineEdit()
            widget.setFixedSize(FIXED_SIZE)
            layout.insertWidget(layout.count() - 2, widget)
            layout.update()
        self.column+=1
        self.update()
        self.invalidate()

    # -1 столбец
    def sub_column(self):
        for i in range(self.count()):
            layout: QHBoxLayout = self.itemAt(i).layout()
            layout.takeAt(layout.count() - 3).widget().deleteLater()
            layout.update()
        self.column-=1
        self.update()
        self.invalidate()

    # +1 строка
    def add_row(self):
        widget = QLabel()
        widget.setFixedSize(FIXED_SIZE)

        self.__tmp_box = QHBoxLayout()
        self.__tmp_box.addWidget(widget)

        for j in range(self.column):
            widget = QLineEdit()
            widget.setFixedSize(FIXED_SIZE)
            self.__tmp_box.addWidget(widget)

        self.update()
        self.invalidate()
        self.row+=1

    # -1 строка
    def sub_row(self):
        item = self.takeAt(self.count() - 1).layout()
        # Удаляем все виджеты, пока они есть
        while item.count() > 0:
            widget_item = item.takeAt(0)  # Берём первый элемент
            if widget_item and widget_item.widget():  # Проверяем, что он существует
                widget_item.widget().deleteLater()
        self.update()
        self.invalidate()
        self.row -= 1

    # получение данных
    def get_data(self):
        mtrx = []

        for i in range(self.count()):
            item = self.itemAt(i).layout()
            lst = []
            if isinstance(item, QHBoxLayout):
                for j in range(item.count()):
                    item_2 = item.itemAt(j).widget()
                    if isinstance(item_2, QLineEdit):
                        if not item_2.text(): raise Exception("ERROR::MatrixInput::get_data --> Не все поля были заполнены")
                        try: lst.append(int(item_2.text()))
                        except ValueError:
                            raise Exception(f"ERROR::MatrixInput::get_data --> \"{item_2.text()}\" в число нельзя перевести!")

            mtrx.append(lst)

        return mtrx

    def clear(self):
        for i in range(self.count()):
            item = self.itemAt(i).layout()
            for j in range(item.count()):
                item_item = item.itemAt(j).widget()
                if isinstance(item_item, QLineEdit):
                    item_item.clear()