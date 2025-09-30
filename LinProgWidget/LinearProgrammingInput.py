from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel, QPushButton, QLineEdit, QCheckBox, QVBoxLayout, \
    QGridLayout


from .LinProgTypes import *



FIXED_SIZE = QSize(50, 50)
ALIGNMENT = Qt.AlignmentFlag.AlignRight
SPACE = 3



class Headers(QHBoxLayout):
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)
        self.header = ["", "x1", "x2"]
        self.setSpacing(SPACE)
        self.count_header = 2
        self.__spaceLabel = QLabel()
        self.__spaceLabel.setFixedSize(FIXED_SIZE)

        self.addWidget(self.__spaceLabel, alignment=ALIGNMENT)
        for i in self.header:
            add_item = QLabel(i)
            add_item.setFixedSize(FIXED_SIZE)
            self.addWidget(add_item, alignment=ALIGNMENT)
        self.addWidget(self.__spaceLabel, alignment=ALIGNMENT)
        self.addWidget(self.__spaceLabel, alignment=ALIGNMENT)


    def add_item(self):
        self.count_header += 1
        add_item = QLabel(f"x{self.count_header}")
        add_item.setFixedSize(FIXED_SIZE)
        self.insertWidget(self.count() - 2 ,add_item)


    def sub_item(self):
        remove_item = self.takeAt(self.count() - 3)
        self.count_header -= 1
        remove_item.widget().deleteLater()
        self.update()



class ZFunctionInput(QHBoxLayout):
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)
        self.setSpacing(SPACE)

        self.__added_widget = QLabel("Z = ")
        self.__added_widget.setFixedSize(FIXED_SIZE)
        self.addWidget(self.__added_widget)

        for i in range(2):
            self.__added_widget = QLineEdit()
            self.__added_widget.setFixedSize(FIXED_SIZE)
            self.addWidget(self.__added_widget)

        self.__added_widget = QLabel("-->")
        self.__added_widget.setFixedSize(FIXED_SIZE)
        self.addWidget(self.__added_widget)

        self.__added_widget = QCheckBox("MAX")
        self.__added_widget.setFixedSize(FIXED_SIZE)
        self.addWidget(self.__added_widget)

    # +1 элемент
    def add_item(self):
        self.__added_widget = QLineEdit()
        self.__added_widget.setFixedSize(FIXED_SIZE)
        self.insertWidget(self.count() - 2, self.__added_widget)

    # -1 элемент
    def sub_item(self):
        remove_item = self.takeAt(self.count() - 4)
        remove_item.widget().deleteLater()
        self.update()


    # получение данных
    def get_data(self):
        # получение целевой задачи
        isMax = self.itemAt(self.count() - 1).widget().isChecked()

        lst: list = []
        for i in range(self.count()):
            item = self.itemAt(i).widget()
            if isinstance(item, QLineEdit):
                if not item.text(): raise Exception("ERROR::ZFunctionInput::get_data --> Не все поля были заполнены")
                try:
                    lst.append(int(item.text()))
                except ValueError:
                    raise Exception(f"ERROR::ZFunctionInput::get_data --> \"{item.text()}\" в число нельзя перевести!")

        return (lst, isMax)


    def clear(self):
        for i in range(self.count()):
            item = self.itemAt(i).widget()
            if isinstance(item, QLineEdit): item.clear()
            if isinstance(item, QCheckBox): item.setChecked(False)


# заранее заготовленный класс для выбора неравенства
class EquationSelect(QComboBox):
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)
        self.addItems(["<=", ">=", "=="])


class ConstraintInput(QVBoxLayout):
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)
        self.setSpacing(SPACE)

        self.column = 2
        self.row = 2

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
            widget = EquationSelect()
            widget.setFixedSize(FIXED_SIZE)
            self.__tmp_box.addWidget(widget)

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
        widget = EquationSelect()
        widget.setFixedSize(FIXED_SIZE)
        self.__tmp_box.addWidget(widget)

        widget = QLineEdit()
        widget.setFixedSize(FIXED_SIZE)
        self.__tmp_box.addWidget(widget)
        self.addLayout(self.__tmp_box)
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
                        if not item_2.text(): raise Exception("ERROR::ConstraintInput::get_data --> Не все поля были заполнены")
                        try: lst.append(int(item_2.text()))
                        except ValueError:
                            raise Exception(f"ERROR::ConstraintInput::get_data --> \"{item_2.text()}\" в число нельзя перевести!")

                    if isinstance(item_2, EquationSelect):
                        lst.append(item_2.currentText())

            mtrx.append(lst)

        return mtrx

    def clear(self):
        for i in range(self.count()):
            item = self.itemAt(i).layout()
            for j in range(item.count()):
                item_item = item.itemAt(j).widget()
                if isinstance(item_item, QLineEdit):
                    item_item.clear()


class ConstrainVariables(QHBoxLayout):
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)
        self.__tmp_widget: QWidget

        self.__tmp_widget = QLabel()
        self.__tmp_widget.setFixedSize(FIXED_SIZE)
        self.addWidget(self.__tmp_widget)

        self.count_var = 2

        for i in range(self.count_var):
            self.__tmp_widget = QCheckBox(">=0")
            self.__tmp_widget.setFixedSize(FIXED_SIZE)
            self.addWidget(self.__tmp_widget)
        for i in range(2):
            self.__tmp_widget = QLabel()
            self.__tmp_widget.setFixedSize(FIXED_SIZE)
            self.addWidget(self.__tmp_widget)

    # +1 столбец
    def add_column(self):
        self.__tmp_widget = QCheckBox(">=0")
        self.__tmp_widget.setFixedSize(FIXED_SIZE)
        self.insertWidget(self.count() - 2, self.__tmp_widget)
        self.invalidate()
        self.update()

    # -1 столбец
    def sub_column(self):
        self.takeAt(self.count() - 3).widget().deleteLater()
        self.invalidate()
        self.update()

    # получение данных
    def get_data(self):
        lst = []
        for i in range(self.count()):
            item = self.itemAt(i).widget()
            if isinstance(item, QCheckBox):
                lst.append((0, None) if item.isChecked() else (None, None))
        return lst

    def clear(self):
        for i in range(self.count()):
            item = self.itemAt(i).widget()
            if isinstance(item, QCheckBox):
                item.setChecked(False)


# ===== main ======
class InputEntry (QWidget):
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)

        self.main_layout: QHBoxLayout = QHBoxLayout(self)


        self.button_grid: QGridLayout = QGridLayout()

        self.label_row = QLabel("Строка")
        self.add_row_button: QPushButton = QPushButton("+")
        self.add_row_button.clicked.connect(self.__add_row)
        self.sub_row_button: QPushButton = QPushButton("-")
        self.sub_row_button.clicked.connect(self.__sub_row)

        self.label_column = QLabel("Столбец")
        self.add_column_button: QPushButton = QPushButton("+")
        self.add_column_button.clicked.connect(self.__add_column)
        self.sub_column_button: QPushButton = QPushButton("-")
        self.sub_column_button.clicked.connect(self.__sub_column)

        self.clear_button: QPushButton = QPushButton("очистить")
        self.clear_button.clicked.connect(self.__clear_input)

        self.button_grid.addWidget(self.label_row, 0, 0)
        self.button_grid.addWidget(self.add_row_button, 0, 1)
        self.button_grid.addWidget(self.sub_row_button, 0, 2)

        self.button_grid.addWidget(self.label_column, 1, 0)
        self.button_grid.addWidget(self.add_column_button, 1, 1)
        self.button_grid.addWidget(self.sub_column_button, 1, 2)

        self.button_grid.addWidget(self.clear_button, 2, 1)

        # расстановка элементов ввода данных
        self.v_box_table: QVBoxLayout = QVBoxLayout()

        # заголовки
        self.header: Headers = Headers()
        self.v_box_table.addLayout(self.header)

        # z function
        self.z_func: ZFunctionInput = ZFunctionInput()
        self.v_box_table.addLayout(self.z_func)

        # constraint equations
        self.constraint: ConstraintInput = ConstraintInput()
        self.v_box_table.addLayout(self.constraint)

        self.constraint_variable: ConstrainVariables = ConstrainVariables()
        self.v_box_table.addLayout(self.constraint_variable)


        self.main_layout.addLayout(self.button_grid)
        self.main_layout.addLayout(self.v_box_table)

        self.table_size = [2, 2]


    def get_data(self):
        z, ismax = self.z_func.get_data()
        return (z,
            self.constraint.get_data(),
            self.constraint_variable.get_data(),
            ismax)


    def __clear_input(self):
        self.z_func.clear()
        self.constraint.clear()
        self.constraint_variable.clear()
        print("clear method")


    def __add_row(self):
        self.constraint.add_row()
        self.table_size[0] += 1


    def __add_column(self):
        print(f"add column method {self.table_size}")
        self.table_size[1] += 1
        self.header.add_item()
        self.z_func.add_item()
        self.constraint.add_column()
        self.constraint_variable.add_column()
        self.adjustSize()
        print(f"add row method {self.table_size}")


    def __sub_row(self):
        if self.table_size[0] > 2:
            self.constraint.sub_row()
            self.table_size[0] -= 1


    def __sub_column(self):
        print("sub columnt method")
        if self.table_size[1] > 2:
            self.header.sub_item()
            self.z_func.sub_item()
            self.constraint.sub_column()
            self.constraint_variable.sub_column()
            self.table_size[1] -= 1
            self.adjustSize()
        print(f"sub row method {self.table_size}")
