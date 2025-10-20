from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from numpy.ma.extras import column_stack

from .MatrixInput import MatrixInput



class MixStrategyWidget (QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # data
        self.row: int = 2
        self.column: int = 2


        self.grid: QGridLayout = QGridLayout()

        self.input_player_a: MatrixInput = MatrixInput(row=self.row, column=1)
        self.input_player_b: MatrixInput = MatrixInput(row=self.column, column=1)

        self.grid.addWidget(QLabel("Вероятности стратегии игроков"), 0, 0)
        self.grid.addWidget(QLabel("Игрок A"), 1, 0)
        self.grid.addWidget(self.input_player_a, 1, 1)
        self.grid.addWidget(QLabel("Игрок B"), 2, 0)
        self.grid.addWidget(self.input_player_b, 2, 1)

        self.setLayout(self.grid)


    def addStrategyA(self):
        self.input_player_a.add_column()
        self.row += 1

    def addStrategyB(self):
        self.input_player_b.add_column()
        self.column += 1

    def subStrategyA(self):
        if self.row > 1:
            self.input_player_a.sub_column()
            self.row -= 1

    def subStrategyB(self):
        if self.column > 1:
            self.input_player_b.sub_column()
            self.column -= 1


    def get_data(self): return self.input_player_a.get_data(), self.input_player_b.get_data()

    def clear(self):
        self.input_player_a.clear()
        self.input_player_b.clear()
