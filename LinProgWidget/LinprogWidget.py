from pprint import pprint

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QFrame, QDialog, \
    QTableWidget, QLabel, QMessageBox, QTableWidgetItem, QAbstractItemView, QTextEdit

from PyQt6.QtCore import Qt, QSize

from .LinearProgrammingInput import InputEntry
from LinprogMethods.Simplex_method import standartize, Simplex, dual_LP, dual_simplex, dual_standartize

from fractions import Fraction

import csv, datetime



class LinProgWidget (QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)

        self.v_box: QVBoxLayout = QVBoxLayout()
        self.simplex_method: QComboBox = QComboBox()
        self.simplex_method.addItems(["Симплекс-Метод", "М-метод", "Двойственная задача", "Двойственный симплекс-метод"])
        self.simplex_method.currentTextChanged.connect(self.changeTextButton)

        self.input_lin_prog: InputEntry = InputEntry()


        self.button_solve: QPushButton = QPushButton("Решить")
        self.button_solve.clicked.connect(self.solving)


        self.button_show: QPushButton = QPushButton("Показать симплекс-таблицу")
        self.button_show.clicked.connect(self.show_table)

        self.button_result: QPushButton = QPushButton("Показать результат")
        self.button_result.clicked.connect(self.show_result)


        # self.button_save: QPushButton = QPushButton("Сохранить")
        

        self.result: tuple|str # type: ignore
        self.save_data: tuple|str # type: ignore
        self.limits_variable: tuple|list
        self.num_variable: int

        self.button_box: QHBoxLayout = QHBoxLayout()
        self.button_box.addWidget(self.button_solve)
        self.button_box.addWidget(self.button_show)
        self.button_box.addWidget(self.button_result)

        self.v_box.addWidget(self.simplex_method)
        self.v_box.addWidget(self.input_lin_prog)
        self.v_box.addLayout(self.button_box)

        self.setLayout(self.v_box)



    def solving(self):
        # classic simplex method and M-method
        if self.simplex_method.currentIndex() in (0, 1):
            print("Selected linear simplex method" if self.simplex_method.currentIndex() == 0 else "Selected M-method")
            z, limits, not_negs, opt = self.input_lin_prog.get_data()
            self.limits_variable = not_negs
            not_negs = [i for i, j in enumerate(not_negs) if j == (0, None)]
            self.num_variable = len(z)
            opt = "max" if opt else "min"

            coefs, rparts, artifs = standartize(z, opt, limits, not_negs, self.simplex_method.currentIndex() == 1)
            result, no_limit, tables = Simplex(coefs, rparts, opt)

            if no_limit:
                QMessageBox.warning(None, "Предупреждение", "Задача не ограничена")

            if artifs in result['basis']:
                QMessageBox.warning(None, "Предупреждение", "Задача не имеет допустимого решения\nПричина: Базисное решение содержит в себе искусственные переменные")

            # обработка данных
            for i in range(len(tables)):
                for cols in range(len(tables[i]['coefs'])):
                    for rows in range(len(tables[i]['coefs'][cols])):
                        if isinstance(tables[i]['coefs'][cols][rows], Fraction):
                            tables[i]['coefs'][cols][rows] = tables[i]['coefs'][cols][rows].numerator / tables[i]['coefs'][cols][rows].denominator

                for j in range(len(tables[i]['solution'])):
                    if isinstance(tables[i]['solution'][j], Fraction):
                        tables[i]['solution'][j] = tables[i]['solution'][j].numerator / tables[i]['solution'][j].denominator

            self.result = (result, no_limit, tables, artifs) # type: ignore



        # dual linear programming
        elif self.simplex_method.currentIndex() == 2:
            print("Selected dual lineap programming")
            z, limits, not_negs, opt = self.input_lin_prog.get_data()
            not_negs = [i for i, j in enumerate(not_negs) if j == (0, None)]
            opt = "max" if opt else "min"

            coefs, rparts, artifs = standartize(z, opt, limits, not_negs, False)
            w, opt, limits, not_negs, not_pos = dual_LP(coefs, rparts, opt)
            self.result: str = "w = "

            # formating
            for i, j in enumerate(w):
                self.result += f"{"+" if i > 0 else ""}{j if j != 1 else ""}x{i+1}"
            self.result += f" -> {opt}\n"

            for index, i in enumerate(limits):
                for var_num, j in enumerate(i):
                    if type(j) in [int, float]:
                        self.result += f"{"+" if var_num > 0 and var_num != 0 and var_num != len(limits[0])-1 and j > 0 else ""} {j}{f'x{var_num+1}' if var_num != len(limits[0]) - 1 else ""}" + ("\n" if var_num == len(limits[0]) - 1 else "")
                    else:
                        self.result += j

            for i in not_negs:
                self.result += f"x{i+1}>=0"



        # dual simplex method
        elif self.simplex_method.currentIndex() == 3:
            print("Selected dual simplex method")
            z, limits, not_negs, opt = self.input_lin_prog.get_data()
            not_negs = [i for i, j in enumerate(not_negs) if j == (0, None)]
            opt = "max" if opt else "min"
            

            coefs, rparts = dual_standartize(z, limits, not_negs)
            simplex_table, no_limit, no_accept, tables = dual_simplex(coefs, rparts, opt)

            if no_limit:
                QMessageBox.warning(None, "Предупреждение", "Задача не ограничена")

            if no_accept:
                QMessageBox.warning(None, "Предупреждение", "Задача не имеет решения")


            # обработка данных
            for i in range(len(tables)):
                for cols in range(len(tables[i]['coefs'])):
                    for rows in range(len(tables[i]['coefs'][cols])):
                        if isinstance(tables[i]['coefs'][cols][rows], Fraction):
                            tables[i]['coefs'][cols][rows] = tables[i]['coefs'][cols][rows].numerator / tables[i]['coefs'][cols][rows].denominator
                
                for j in range(len(tables[i]['solution'])):
                    if isinstance(tables[i]['solution'][j], Fraction):
                        tables[i]['solution'][j] = tables[i]['solution'][j].numerator / tables[i]['solution'][j].denominator

            self.result = (simplex_table, no_limit, no_accept, tables) # type: ignore



    def show_table(self):
        child_window: QDialog = QDialog(self)
        child_window.resize(500, 300)
        dialog_layout: QVBoxLayout = QVBoxLayout()
        
        # classic simplex method
        if self.simplex_method.currentIndex() == 0:
            simplex_table: QTableWidget = QTableWidget()

            steps: list[dict] = self.result[-2] # type: ignore
        
            split_table: list[list] = list()
            for elem in steps:
                basis = [f"x{j+1}" for j in elem['basis']] + ["z"]

                coefs = elem['coefs']
                solution = elem['solution']

                # формирование строки и столбца, формирование будет 
                for j in range(len(coefs)):
                    split_table.append( [basis[j]] + [solution[j]] + coefs[j] )

            simplex_table.setRowCount(len(split_table))
            simplex_table.setColumnCount(len(split_table[0]))

            # set horisontal title
            horisontal_labels = ["Базис", "Решение"] + [f"x{i+1}" for i in range(len(steps[0]['coefs'][0]))]
            simplex_table.setHorizontalHeaderLabels(horisontal_labels)

            for i in range(len(split_table)):
                for j in range(len(split_table[i])):
                    item = QTableWidgetItem()
                    item.setText(str(split_table[i][j]))
                    simplex_table.setItem(i, j, item)

            simplex_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            simplex_table.resizeColumnsToContents()
            simplex_table.resizeRowsToContents()
            pprint(split_table)

            dialog_layout.addWidget(QLabel("Результат решения симплекс-методом"), alignment=Qt.AlignmentFlag.AlignHCenter)
            dialog_layout.addWidget(simplex_table)


        # M-method
        elif self.simplex_method.currentIndex() == 1:
            simplex_table: QTableWidget = QTableWidget()

            steps: list[dict] = self.result[-2] # type: ignore
            long_variable: list = self.result[-1] # type: ignore
        
            split_table: list[list] = list()
            for elem in steps:
                basis = [f"x{i+1}" if i not in long_variable else f"p{long_variable.index(i)+1}" for i in elem['basis']] + ["z"]
                coefs = elem['coefs']
                solution = elem['solution']

                # формирование строки и столбца, формирование будет 
                for j in range(len(coefs)):
                    split_table.append( [basis[j]] + [solution[j]] + coefs[j] )

            simplex_table.setRowCount(len(split_table))
            simplex_table.setColumnCount(len(split_table[0]))

            horisontal_labels = ["Базис", "Решение"] + [f"x{i+1}" for i in range(len(steps[0]['coefs'][0]))]
            for i in long_variable:
                horisontal_labels[i] = f"p{long_variable.index(i)+1}"
            
            simplex_table.setHorizontalHeaderLabels(horisontal_labels)

            for i in range(len(split_table)):
                for j in range(len(split_table[i])):
                    item = QTableWidgetItem()
                    item.setText(str(split_table[i][j]))
                    simplex_table.setItem(i, j, item)

            simplex_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            simplex_table.resizeColumnsToContents()
            simplex_table.resizeRowsToContents()

            dialog_layout.addWidget(QLabel("Результат решения M-методом"), alignment=Qt.AlignmentFlag.AlignHCenter)
            dialog_layout.addWidget(simplex_table, alignment=Qt.AlignmentFlag.AlignHCenter)


        # двойственная задача
        elif self.simplex_method.currentIndex() == 2:
            dialog_layout.addWidget(QLabel("Вывод построенной двойственной задачи"), alignment=Qt.AlignmentFlag.AlignHCenter)
            output = QTextEdit()
            output.setReadOnly(True)
            output.setText(self.result)
            dialog_layout.addWidget(output)            


        # двойственный симлпекс-метод
        elif self.simplex_method.currentIndex() == 3:
            simplex_table: QTableWidget = QTableWidget()

            steps: list[dict] = self.result[-1] # type: ignore

            split_table: list[list] = list()
            for elem in steps:
                basis = [f"x{j+1}" for j in elem['basis']] + ["z"]
                coefs = elem['coefs']
                solution = elem['solution']

                # формирование строки и столбца, формирование будет 
                for j in range(len(coefs)):
                    split_table.append( [basis[j]] + [solution[j]] + coefs[j] )

            simplex_table.setRowCount(len(split_table))
            simplex_table.setColumnCount(len(split_table[0]))

            horisontal_labels = ["Базис", "Решение"] + [f"x{i+1}" for i in range(len(steps[0]['coefs'][0]))]
            simplex_table.setHorizontalHeaderLabels(horisontal_labels)

            for i in range(len(split_table)):
                for j in range(len(split_table[i])):
                    item = QTableWidgetItem()
                    item.setText(str(split_table[i][j]))
                    simplex_table.setItem(i, j, item)

            simplex_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            simplex_table.resizeColumnsToContents()
            simplex_table.resizeRowsToContents()
            pprint(split_table)

            dialog_layout.addWidget(QLabel("Результат решения двойственным симплекс-методом"), alignment=Qt.AlignmentFlag.AlignHCenter)
            dialog_layout.addWidget(simplex_table)

        child_window.setLayout(dialog_layout)
        child_window.show()



    def show_result(self):
        result = self.result[0][-1]
        pprint(result)



    # смена названия кнопки и скрытия лишней
    def changeTextButton(self, textChanged: str):
        if textChanged.lower() in ["симплекс-метод", "м-метод", "двойственный симплекс-метод"]:
            self.button_show.setText("Показать симплекс-таблицу")
            self.button_result.show()
        else:
            self.button_show.setText("Вывести двойственную задачу")
            self.button_result.hide()
