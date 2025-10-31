from pprint import pprint

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QFrame, QDialog, \
    QTableWidget, QLabel, QMessageBox, QTableWidgetItem, QAbstractItemView, QTextEdit, QFileDialog

from PyQt6.QtCore import Qt, QSize

from .LinearProgrammingInput import InputEntry
from LinprogMethods.Simplex_method import standartize, Simplex, dual_LP, dual_simplex, dual_standartize

from fractions import Fraction

import csv, datetime



def get_all_index_find_to(lst: list, value) -> list:
    l = lst.copy()
    indexes = list()
    while value in l:
        indexes.append(l.index(value))
        l[l.index(value)] = None
    return indexes




class LinProgWidget (QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setObjectName("FrameWidget")
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


        self.button_save: QPushButton = QPushButton("Сохранить")
        self.button_save.clicked.connect(self.save_solution)
        

        self.result: tuple|str # type: ignore
        self.save_data: tuple|str # type: ignore
        self.limits_variable: list[tuple] = []
        self.num_variable: int

        self.button_box: QHBoxLayout = QHBoxLayout()
        self.button_box.addWidget(self.button_solve)
        self.button_box.addWidget(self.button_show)
        self.button_box.addWidget(self.button_result)
        self.button_box.addWidget(self.button_save)

        self.v_box.addWidget(self.simplex_method)
        self.v_box.addWidget(self.input_lin_prog)
        self.v_box.addLayout(self.button_box)

        self.setLayout(self.v_box)



    def solving(self):
        # classic simplex method and M-method
        if self.simplex_method.currentIndex() in (0, 1):
            print("Selected linear simplex method" if self.simplex_method.currentIndex() == 0 else "Selected M-method")
            z, limits, self.limits_variable, opt = self.input_lin_prog.get_data()
            self.num_variable = len(self.limits_variable) + self.limits_variable.count((None, None))
            
            not_negs = [i for i, j in enumerate(self.limits_variable) if j == (0, None)]
            opt = "max" if opt else "min"

            coefs, rparts, artifs = standartize(z, opt, limits, not_negs, self.simplex_method.currentIndex() == 1)
            result, no_limit, tables = Simplex(coefs, rparts, opt)

            if no_limit:
                QMessageBox.warning(None, "Предупреждение", "Задача не ограничена")

            if not set(artifs).isdisjoint(result['basis']):
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
            self.num_variable = len(self.limits_variable) + self.limits_variable.count((None, None))
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
                self.result += f"x{i+1}>=0\n"



        # dual simplex method
        elif self.simplex_method.currentIndex() == 3:
            print("Selected dual simplex method")
            z, limits, self.limits_variable, opt = self.input_lin_prog.get_data()
            self.num_variable = len(self.limits_variable) + self.limits_variable.count((None, None))
            not_negs = [i for i, j in enumerate(self.limits_variable) if j == (0, None)]
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

            # set horisontal title
            horisontal_labels = ["Базис", "Решение"]
            for i in range(len(steps[0]['coefs'][0])):
                if i < len(self.limits_variable):
                    if self.limits_variable[i] != (None, None):
                        horisontal_labels.append(f"x{i+1}")
                    else:
                        horisontal_labels.append(f"x{i+1}'")
                        horisontal_labels.append(f"x{i+1}''")
                else:
                        horisontal_labels.append(f"x{i+1}")

            split_table: list[list] = list()
            for elem in steps:
                basis: list = list()
                for j in elem['basis']:
                    basis.append(horisontal_labels[j + 2])
                basis += ["z"]
                coefs = elem['coefs']
                solution = elem['solution']

                # формирование строки и столбца, формирование будет 
                for j in range(len(coefs)):
                    split_table.append( [basis[j]] + [solution[j]] + coefs[j] )

            simplex_table.setRowCount(len(split_table))
            simplex_table.setColumnCount(len(split_table[0]))

            simplex_table.setHorizontalHeaderLabels(horisontal_labels)

            for i in range(len(split_table)):
                for j in range(len(split_table[i])):
                    item = QTableWidgetItem()
                    item.setText(str(split_table[i][j]))
                    simplex_table.setItem(i, j, item)

            simplex_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            simplex_table.resizeColumnsToContents()
            simplex_table.resizeRowsToContents()

            self.save_data = [horisontal_labels] + split_table
            
            dialog_layout.addWidget(QLabel("Результат решения симплекс-методом"), alignment=Qt.AlignmentFlag.AlignHCenter)
            dialog_layout.addWidget(simplex_table)


        # M-method
        elif self.simplex_method.currentIndex() == 1:
            simplex_table: QTableWidget = QTableWidget()

            steps: list[dict] = self.result[-2] # type: ignore
            long_variable: list = self.result[-1] # type: ignore
        
            horisontal_labels = ["Базис", "Решение"]

            for i in range(len(steps[0]['coefs'][0])):
                if i < len(self.limits_variable):
                    if self.limits_variable[i] != (None, None):
                        horisontal_labels.append(f"x{i+1}")
                    else:
                        horisontal_labels.append(f"x{i+1}'")
                        horisontal_labels.append(f"x{i+1}''")
                else:
                    if i not in long_variable:
                        horisontal_labels.append(f"x{i+1}")
                    else:
                        horisontal_labels.append(f"p{long_variable.index(i)+1}")


            split_table: list[list] = list()
            for elem in steps:
                basis: list = list()
                for j in elem['basis']:
                    basis.append(horisontal_labels[j + 2])
                basis += ["z"]
                coefs = elem['coefs']
                solution = elem['solution']

                # формирование строки и столбца, формирование будет 
                for j in range(len(coefs)):
                    split_table.append( [basis[j]] + [solution[j]] + coefs[j] )

            simplex_table.setRowCount(len(split_table))
            simplex_table.setColumnCount(len(split_table[0]))

            
            simplex_table.setHorizontalHeaderLabels(horisontal_labels)

            for i in range(len(split_table)):
                for j in range(len(split_table[i])):
                    item = QTableWidgetItem()
                    item.setText(str(split_table[i][j]))
                    simplex_table.setItem(i, j, item)

            simplex_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            simplex_table.resizeColumnsToContents()
            simplex_table.resizeRowsToContents()

            self.save_data = [horisontal_labels] + split_table

            dialog_layout.addWidget(QLabel("Результат решения M-методом"), alignment=Qt.AlignmentFlag.AlignHCenter)
            dialog_layout.addWidget(QLabel("Следует учесть, что, если число в таблице больше 1000, то это число умножено на большой штраф равный 1000"), alignment=Qt.AlignmentFlag.AlignHCenter)
            dialog_layout.addWidget(simplex_table)


        # двойственная задача
        elif self.simplex_method.currentIndex() == 2:
            dialog_layout.addWidget(QLabel("Вывод построенной двойственной задачи"), alignment=Qt.AlignmentFlag.AlignHCenter)
            output = QTextEdit()
            output.setReadOnly(True)
            self.save_data = self.result
            output.setText(self.result)
            dialog_layout.addWidget(output)            


        # двойственный симлпекс-метод
        elif self.simplex_method.currentIndex() == 3:
            simplex_table: QTableWidget = QTableWidget()

            steps: list[dict] = self.result[-1] # type: ignore

            horisontal_labels = ["Базис", "Решение"]
            for i in range(len(steps[0]['coefs'][0])):
                if i < len(self.limits_variable):
                    if self.limits_variable[i] != (None, None):
                        horisontal_labels.append(f"x{i+1}")
                    else:
                        horisontal_labels.append(f"x{i+1}'")
                        horisontal_labels.append(f"x{i+1}''")
                else:
                        horisontal_labels.append(f"x{i+1}")


            split_table: list[list] = list()
            for elem in steps:
                basis: list = list()
                for j in elem['basis']:
                    basis.append(horisontal_labels[j + 2])
                basis += ["z"]
                coefs = elem['coefs']
                solution = elem['solution']

                # формирование строки и столбца, формирование будет 
                for j in range(len(coefs)):
                    split_table.append( [basis[j]] + [solution[j]] + coefs[j] )

            simplex_table.setRowCount(len(split_table))
            simplex_table.setColumnCount(len(split_table[0]))

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

            self.save_data = [horisontal_labels] + split_table

            dialog_layout.addWidget(QLabel("Результат решения двойственным симплекс-методом"), alignment=Qt.AlignmentFlag.AlignHCenter)
            dialog_layout.addWidget(simplex_table)

        child_window.setLayout(dialog_layout)
        child_window.show()



    def show_result(self):
        result = self.result[-2 if self.simplex_method.currentIndex() in [0, 1] else -1][-1]
        basis = result['basis']
        solution = result['solution']
        
        pprint(basis)
        pprint(solution)

        index_list = [i for i in range(self.num_variable)]
        solution_list_var = [solution[basis.index(i)] if i in basis else 0 for i in index_list]
        for index, j in enumerate(self.limits_variable):
            if j == (None, None):
                solution_list_var[index] -= solution_list_var.pop(index + 1)
        
        output = f"Z = {solution[-1]}\n"
        for index, i in enumerate(solution_list_var):
            output += f"x{index+1} = {solution_list_var[index]}"
            output += "\n"
        print(output)

        child_window: QDialog = QDialog(self)
        child_window.resize(500, 300)
        dialog_layout: QVBoxLayout = QVBoxLayout()

        output_widget = QTextEdit()
        output_widget.setReadOnly(True)
        output_widget.setText(output)
        dialog_layout.addWidget(output_widget)

        child_window.setLayout(dialog_layout)
        child_window.show()


    def save_solution(self):
        file_path, filter = QFileDialog.getSaveFileName(
            self,
            "Сохранение таблицы" if self.simplex_method.currentIndex() != 2 else "Сохранить двойственную задачу",
            "",
            ".csv" if self.simplex_method.currentIndex() != 2 else ".txt"
        )

        if file_path:
            try:
                with open(file_path+filter, 'w', encoding='utf-8') as file:
                    if self.simplex_method.currentIndex() == 2:
                        file.write(self.save_data)
                    else:
                        csv_writer = csv.writer(file, delimiter=';')
                        for i in self.save_data:
                            csv_writer.writerow(i)

                    
                    QMessageBox.information(None, "Успешное сохранение", f"Файл сохранён:\n{file_path}")
            except Exception as e:
                    QMessageBox.critical(None, "Ошибка", f"Ошибка при сохранении:\n{e}")


    # смена названия кнопки и скрытия лишней
    def changeTextButton(self, textChanged: str):
        if textChanged.lower() in ["симплекс-метод", "м-метод", "двойственный симплекс-метод"]:
            self.button_show.setText("Показать симплекс-таблицу")
            self.button_result.show()
        else:
            self.button_show.setText("Вывести двойственную задачу")
            self.button_result.hide()
