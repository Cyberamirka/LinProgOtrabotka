from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from .MatrixInput import MatrixInput


class GameWithNatureWidget (QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.v_box: QVBoxLayout = QVBoxLayout()
        self.h_box: QHBoxLayout = QHBoxLayout()

        self.select_method: QComboBox = QComboBox()
        self.select_method.addItems([
            "критерий Байеса",
            "критерий Лапласа",
            "критерий Вальда",
            "критерий Севиджа",
            "критерий Гурвица"
        ])

        self.select_method.currentIndexChanged.connect(self.change_kriteri)

        self.row: int = 2

        self.nature_input: MatrixInput = MatrixInput(row=self.row, column=1)
        self.h_box.addWidget(QLabel("Природа"))
        self.h_box.addWidget(self.nature_input)

        self.v_box.addWidget(self.select_method)
        self.v_box.addLayout(self.h_box)

        self.setLayout(self.v_box)



    def change_kriteri(self, index: int):
        if index == 0:
            # Показать все виджеты
            for i in range(self.h_box.count()):
                widget = self.h_box.itemAt(i).widget()
                if isinstance(widget, QWidget) or isinstance(widget, MatrixInput):
                    widget.show()
            return

        # Скрыть все виджеты (или выполнить другую логику)
        for i in range(self.h_box.count()):
            widget = self.h_box.itemAt(i).widget()
            if isinstance(widget, QWidget) or isinstance(widget, MatrixInput):
                widget.hide()


    def addNatureStrategy(self):
        self.nature_input.add_column()
        self.row += 1


    def subNatureStrategy(self):
        if self.row > 1:
            self.nature_input.sub_column()
            self.row -= 1


    def clear(self):
        self.nature_input.clear()


    def get_data(self):
        return self.nature_input.get_data()


    def get_current_criteri(self):
        return self.select_method.currentIndex()
