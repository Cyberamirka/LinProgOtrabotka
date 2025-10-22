# libs
from PyQt6.QtWidgets import QFrame, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, \
    QTextEdit, QStackedWidget, QTableWidget, QDialog, QMessageBox, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt
import numpy as np
from pprint import pprint

from MatrixMethod.Matrix import find_matrix_risk
# visual module
from .GameWithNature import GameWithNatureWidget
from .MatrixInput import MatrixInput
from .MixStrategyWidget import MixStrategyWidget

# modules
import MatrixMethod.Matrix
from MatrixMethod.MatrixTypes import ApproximateResult





class MatrixGameWidget(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setObjectName("FrameWidget")
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)

        # data
        self.table: list[list] | None = None

        self.__init_ui()
        self.__connect_signals()
        self.__add_ui()



    def __init_ui(self):
        self.selected_method: QComboBox = QComboBox()
        self.selected_method.addItems(["Смешанные стратегии", "Приближенное значение", "Игры с природой"])

        # виджеты которые будут иногда скрываться из виду в зависимости от выбранной настройки
        self.contextControl: QStackedWidget = QStackedWidget()

        self.mix_strategy_widget: MixStrategyWidget = MixStrategyWidget()
        self.game_with_nature: GameWithNatureWidget = GameWithNatureWidget()


        # main layout
        self.v_box: QVBoxLayout = QVBoxLayout()

        # pay matrix input block
        self.h_box_layout: QHBoxLayout = QHBoxLayout()
        self.grid_button_action: QGridLayout = QGridLayout()


        # кнопки
        self.addRowAction: QPushButton = QPushButton("+")
        self.subRowAction: QPushButton = QPushButton("-")
        self.addColumnAction: QPushButton = QPushButton("+")
        self.subColumnAction: QPushButton = QPushButton("-")
        self.clearAction: QPushButton = QPushButton("очистить")

        # платёжная матрица
        self.pay_matrix_label: QLabel = QLabel("Платёжная матрица")
        self.pay_matrix: MatrixInput = MatrixInput(row=2, column=2)

        # глобальные кнопки
        self.main_h_box_action_button: QHBoxLayout = QHBoxLayout()
        self.solveAction: QPushButton = QPushButton("Решить")
        self.showTableAction: QPushButton = QPushButton("Показать таблицу")
        self.showTableAction.hide()

        # решение
        self.output_solution: QTextEdit = QTextEdit()
        self.output_solution.setPlaceholderText("Вывод ответа, только для чтения")
        self.output_solution.setReadOnly(True)



    def __add_ui(self):
        self.selected_method.currentIndexChanged.connect(self.changeIndexAction)

        # добавление в QStackedWidget
        self.contextControl.addWidget(self.mix_strategy_widget)
        self.contextControl.addWidget(QWidget())
        self.contextControl.addWidget(self.game_with_nature)

        # добавление в grid элементов
        self.grid_button_action.addWidget(QLabel("Строка"), 0, 0)
        self.grid_button_action.addWidget(self.addRowAction, 0, 1)
        self.grid_button_action.addWidget(self.subRowAction, 0, 2)
        self.grid_button_action.addWidget(QLabel("Колонка"), 1, 0)
        self.grid_button_action.addWidget(self.addColumnAction, 1, 1)
        self.grid_button_action.addWidget(self.subColumnAction, 1, 2)
        self.grid_button_action.addWidget(self.clearAction, 2, 0, 1, 3)

        # добавление платёжной матрицы
        self.h_box_layout.addWidget(self.pay_matrix)
        self.h_box_layout.addLayout(self.grid_button_action)

        self.main_h_box_action_button.addWidget(self.solveAction)
        self.main_h_box_action_button.addWidget(self.showTableAction)

        self.v_box.addWidget(self.selected_method)
        self.v_box.addWidget(self.pay_matrix_label)
        self.v_box.addLayout(self.h_box_layout)
        self.v_box.addWidget(self.contextControl)
        self.v_box.addLayout(self.main_h_box_action_button)
        self.v_box.addWidget(self.output_solution)

        self.setLayout(self.v_box)



    def __connect_signals(self):
        self.addRowAction.clicked.connect(self.pay_matrix.add_row)
        self.addRowAction.clicked.connect(self.mix_strategy_widget.addStrategyA)

        self.subRowAction.clicked.connect(self.pay_matrix.sub_row)
        self.subRowAction.clicked.connect(self.mix_strategy_widget.subStrategyA)

        self.addColumnAction.clicked.connect(self.pay_matrix.add_column)
        self.addColumnAction.clicked.connect(self.mix_strategy_widget.addStrategyB)
        self.subColumnAction.clicked.connect(self.pay_matrix.sub_column)
        self.addColumnAction.clicked.connect(self.game_with_nature.addNatureStrategy)

        self.subColumnAction.clicked.connect(self.mix_strategy_widget.subStrategyB)
        self.subColumnAction.clicked.connect(self.game_with_nature.subNatureStrategy)

        self.solveAction.clicked.connect(self.solve)
        self.showTableAction.clicked.connect(self.show_table)

        self.clearAction.clicked.connect(self.mix_strategy_widget.clear)
        self.clearAction.clicked.connect(self.pay_matrix.clear)
        self.clearAction.clicked.connect(self.output_solution.clear)
        self.clearAction.clicked.connect(self.game_with_nature.clear)


    def show_table(self):
        child_window: QDialog = QDialog()
        v_box: QVBoxLayout = QVBoxLayout()

        if self.table == None:
            QMessageBox.critical(None, "Ошибка", "Без решения вывод таблицы не возможен!")
            return


        if self.selected_method.currentIndex() == 2 and self.game_with_nature.get_current_criteri() == 0:
            pprint(self.table[0])
            pprint(self.table[1])
            
            A_table = self.table[0]
            B_table = self.table[1]

            table_view_a: QTableWidget = QTableWidget()
            table_view_p: QTableWidget = QTableWidget()

            table_view_a.setRowCount(len(A_table) - 1)
            table_view_a.setColumnCount(len(A_table[0]))
            table_view_a.setHorizontalHeaderLabels(A_table[0])

            table_view_p.setRowCount(len(B_table))
            table_view_p.setColumnCount(len(B_table[0]))
            table_view_p.setHorizontalHeaderLabels(B_table[0])


            for i in range(1, len(A_table)):
                for j in range(len(A_table[i])):
                    table_view_a.setItem(i - 1, j, QTableWidgetItem(str(A_table[i][j])))

            for i in range(1, len(B_table)):
                for j in range(len(B_table[i])):
                    table_view_p.setItem(i - 1, j, QTableWidgetItem(str(B_table[i][j])))

            table_view_a.resizeColumnsToContents()
            table_view_a.resizeRowsToContents()
            table_view_a.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            table_view_p.resizeColumnsToContents()
            table_view_p.resizeRowsToContents()
            table_view_p.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


            v_box.addWidget(QLabel("Платёжная матрица"))
            v_box.addWidget(table_view_a)
            v_box.addWidget(QLabel("Матрица рисков"))
            v_box.addWidget(table_view_p)

        else:
            table_view: QTableWidget = QTableWidget()

            table_view.setRowCount(len(self.table))
            table_view.setColumnCount(len(self.table[0]))
            table_view.setHorizontalHeaderLabels(self.table[0])

            for i in range(1, len(self.table)):
                for j in range(len(self.table[i])):
                    table_view.setItem(i-1, j, QTableWidgetItem(str(self.table[i][j])))

            table_view.resizeColumnsToContents()
            table_view.resizeRowsToContents()
            table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            v_box.addWidget(table_view)
        child_window.setLayout(v_box)
        child_window.exec()


    # получает информацию и выдаёт конечный ответ в текстовое поле
    def solve(self):
        self.table = None
        self.output_solution.clear()
        result: str = ""

        mtrx = np.array(self.pay_matrix.get_data())

        # смешанные стратегии
        if self.selected_method.currentIndex() == 0:
            if MatrixMethod.Matrix.saddle_point(mtrx) != None:
                result += f"Игра имеет седловую точку\nv* = {MatrixMethod.Matrix.saddle_point(mtrx)}"
            else:
                A, B = self.mix_strategy_widget.get_data()
                A = np.array(A[0])
                B = np.array(B[0])
                solving = MatrixMethod.Matrix.MixStrategy(mtrx, A, B)
                result += f"Цена игры при применении игроками смешанных стретегий\nv* = {solving}"

        # приближенное значение
        elif self.selected_method.currentIndex() == 1:
            if MatrixMethod.Matrix.saddle_point(mtrx) != None:
                result += f"Игра имеет седловую точку\nv* = {MatrixMethod.Matrix.saddle_point(mtrx)}"
            else:
                result_approximate: ApproximateResult = MatrixMethod.Matrix.ApproximateSolving(mtrx, 20)
                self.table = result_approximate.table.tolist()
                result += f"Кол-во применёных игроками каждой из своих чистых статегий:\n"
                for i in range(len(result_approximate.count_clean_strategy_a)):
                    result += f"m(A{i+1}) = {result_approximate.count_clean_strategy_a[i]}; "
                result += '\n'
                for i in range(len(result_approximate.count_clean_strategy_b)):
                    result += f"m(B{i+1}) = {result_approximate.count_clean_strategy_b[i]}; "
                result += 'Вероятности применения своих чистых стратегий игроком А:\n'
                for i in range(len(result_approximate.frequency_a)):
                    result += f"x{i+1}* = {result_approximate.frequency_a[i]}; "
                result += 'Вероятности применения своих чистых стратегий игроком B:\n'
                for i in range(len(result_approximate.frequency_b)):
                    result += f"y{i+1}* = {result_approximate.frequency_b[i]}; "
                result += '\n'
                result += f"Приближенное значение игры: {result_approximate.price}"

        # игры с природой
        elif self.selected_method.currentIndex() == 2:
            # критерий Байеса
            if self.game_with_nature.get_current_criteri() == 0:
                res_game = MatrixMethod.Matrix.Bayes_criterion(
                    mtrx,
                    MatrixMethod.Matrix.find_matrix_risk(mtrx),
                    self.game_with_nature.get_data()[0])

                self.table = (res_game[0], res_game[1])
                result += f"Согласно матрице рисков оптимальной стратегией является стратегия {res_game[1][res_game[-1] + 1][0]}. Ожидаемый выйгрыш - {res_game[1][res_game[-1] + 1][-1]}\n"
                result += f"Согласно матрице выйгрышей оптимальной стратегией является стратегия {res_game[0][res_game[-2] + 1][0]}. Ожидаемый выйгрыш - {res_game[0][res_game[-2] + 1][-1]}\n"

            # критерий Лапласа
            if self.game_with_nature.get_current_criteri() == 1:
                p = [1 / len(mtrx[0]) for i in range(len(mtrx[0]))]
                res_game = MatrixMethod.Matrix.Bayes_criterion(
                    mtrx,
                    mtrx,
                    p)

                self.table = res_game[0]
                
                result += f"Согласно матрице выйгрышей оптимальной стратегией является стратегия {res_game[0][res_game[-2] + 1][0]}. Ожидаемый выйгрыш - {res_game[0][res_game[-2] + 1][-1]}\n"

            # критерий Вальда
            if self.game_with_nature.get_current_criteri() == 2:
                matrix = np.array(self.pay_matrix.get_data())
                res_game = MatrixMethod.Matrix.Wild_criterion(matrix)
                self.table = res_game[0]
                result += f"Согласно матрице выйгрышей оптимальной стратегией является стратегия {self.table[res_game[-1] + 1][0]}. Ожидаемый выйгрыш - {self.table[res_game[-1] + 1][-1]}\n"

            # критерий Сэвиджа
            if self.game_with_nature.get_current_criteri() == 3:
                res_game = MatrixMethod.Matrix.Savage_criterion(find_matrix_risk(mtrx))
                self.table = res_game[0]
                result += f"Согласно матрице выйгрышей оптимальной стратегией является стратегия {self.table[res_game[-1] + 1][0]}. Ожидаемый выйгрыш - {self.table[res_game[-1] + 1][-1]}\n"

            # критерий Гурвица
            if self.game_with_nature.get_current_criteri() == 4:
                res_game = MatrixMethod.Matrix.Hurwitz_criterion(mtrx)
                self.table = res_game[0]
                result += f"Согласно матрице выйгрышей оптимальной стратегией является стратегия {self.table[res_game[-1] + 1][0]}. Ожидаемый выйгрыш - {self.table[res_game[-1] + 1][-1]}\n"


        self.output_solution.setText(result)



    def changeIndexAction(self, index: int):
        self.showTableAction.setHidden(index == 0)
        self.contextControl.setCurrentIndex(index)