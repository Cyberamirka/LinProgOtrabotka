from PyQt6.QtWidgets import QFrame, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import Qt

from .MatrixInput import MatrixInput


class MatrixGameWidget(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)

        # begin data
        row: int = 2
        column: int = 2
        # end data

        self.__init_ui()
        self.__add_ui()




    def __init_ui(self):
        self.selected_method: QComboBox = QComboBox()
        self.selected_method.addItems(["Смешанные стратегии", "Приближенное значение", "Игры с природой"])

        # main layout
        self.v_box: QVBoxLayout = QVBoxLayout()

        # pay matrix input block
        self.h_box_layout: QHBoxLayout = QHBoxLayout()

        self.grid_button_action: QGridLayout = QGridLayout()

        self.addRowAction: QPushButton = QPushButton("+")
        self.subRowAction: QPushButton = QPushButton("-")
        self.addColumnAction: QPushButton = QPushButton("+")
        self.subColumnAction: QPushButton = QPushButton("-")
        self.clearAction: QPushButton = QPushButton("очистить")

        # платёжная матрица
        self.pay_matrix_label: QLabel = QLabel("Платёжная матрица")
        self.pay_matrix: MatrixInput = MatrixInput(row=2, column=2)





    def __add_ui(self):
        # добавление в grid элементов
        self.grid_button_action.addWidget(QLabel("Строка"), 0, 0)
        self.grid_button_action.addWidget(self.addRowAction, 0, 1)
        self.grid_button_action.addWidget(self.subRowAction, 0, 2)
        self.grid_button_action.addWidget(QLabel("Колонка"), 1, 0)
        self.grid_button_action.addWidget(self.addColumnAction, 1, 1)
        self.grid_button_action.addWidget(self.subColumnAction, 1, 2)
        self.grid_button_action.addWidget(self.clearAction, 2, 0, 1, 3)

        # добавление платёжной матрицы
        self.h_box_layout.addLayout(self.pay_matrix)
        self.h_box_layout.addLayout(self.grid_button_action)

        

        self.v_box.addWidget(self.selected_method)
        self.v_box.addWidget(self.pay_matrix_label)
        self.v_box.addLayout(self.h_box_layout)
        self.setLayout(self.v_box)



    def change_selected(self):
        pass
