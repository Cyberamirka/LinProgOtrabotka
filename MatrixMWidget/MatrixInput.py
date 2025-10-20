from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import QSize, Qt

FIXED_SIZE = QSize(50, 50)
ALIGNMENT = Qt.AlignmentFlag.AlignRight
SPACE = 3

# матрица
class MatrixInput(QWidget):
    def __init__(self, parent: QWidget|None = None, row: int = 2, column: int = 2):
        super().__init__(parent)

        self.column = row
        self.row = column

        self.v_box: QVBoxLayout = QVBoxLayout()
        self.v_box.setSpacing(SPACE)
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
            self.v_box.addLayout(self.__tmp_box)
            self.setLayout(self.v_box)

    # +1 столбец
    def add_column(self):
        for i in range(self.v_box.count()):
            layout: QHBoxLayout = self.v_box.itemAt(i).layout()
            widget = QLineEdit()
            widget.setFixedSize(FIXED_SIZE)
            layout.insertWidget(layout.count() - 2, widget)
            layout.update()
        self.column+=1
        self.v_box.update()
        self.v_box.invalidate()

    # -1 столбец
    def sub_column(self):
        for i in range(self.v_box.count()):
            layout: QHBoxLayout = self.v_box.itemAt(i).layout()
            layout.takeAt(layout.count() - 3).widget().deleteLater()
            layout.update()
        self.column-=1
        self.v_box.update()
        self.v_box.invalidate()

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

        self.v_box.addLayout(self.__tmp_box)
        self.v_box.update()
        self.v_box.invalidate()
        self.row+=1

    # -1 строка
    def sub_row(self):
        item = self.v_box.takeAt(self.v_box.count() - 1).layout()
        # Удаляем все виджеты, пока они есть
        while item.count() > 0:
            widget_item = item.takeAt(0)  # Берём первый элемент
            if widget_item and widget_item.widget():  # Проверяем, что он существует
                widget_item.widget().deleteLater()
        self.v_box.update()
        self.v_box.invalidate()
        self.row -= 1

    # получение данных
    def get_data(self):
        mtrx = []

        for i in range(self.v_box.count()):
            item = self.v_box.itemAt(i).layout()
            lst = []
            if isinstance(item, QHBoxLayout):
                for j in range(item.count()):
                    item_2 = item.itemAt(j).widget()
                    if isinstance(item_2, QLineEdit):
                        if not item_2.text(): raise Exception("ERROR::MatrixInput::get_data --> Не все поля были заполнены")
                        try: lst.append(float(item_2.text()))
                        except ValueError:
                            raise Exception(f"ERROR::MatrixInput::get_data --> \"{item_2.text()}\" в число нельзя перевести!")

            mtrx.append(lst)

        return mtrx


    def clear(self):
        for i in range(self.v_box.count()):
            item = self.v_box.itemAt(i).layout()
            for j in range(item.count()):
                item_item = item.itemAt(j).widget()
                if isinstance(item_item, QLineEdit):
                    item_item.clear()
