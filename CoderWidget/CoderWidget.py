# libs
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QFrame, QComboBox, QVBoxLayout, QLabel, QTextEdit, QPushButton, \
    QGridLayout, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView

# stdlib
import math


# user modules
from PyQt6_SwitchControl import SwitchControl as QSwitchControl

from CoderMethods.baseFunctions import *
from CoderMethods.Fano import *
from CoderMethods.Haffman import *
from CoderMethods.CRC import *



class CoderWidget(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setObjectName("FrameWidget")
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)

        # data
        self.code_table: CodeTable = CodeTable()
        self.table: list = list()
        self.GENERATORS = {
            "1": ("100101", "x⁵ + x² + 1"),
            "2": ("101001", "x⁵ + x³ + 1"),  
            "3": ("110101", "x⁵ + x⁴ + x² + 1"),
            "4": ("1000011", "x⁶ + x + 1"),
            "5": ("100000111", "x⁸ + x² + x + 1"),
            "6": ("100110001", "x⁸ + x⁵ + x⁴ + 1"),
            "7": ("100011101", "x⁸ + x⁴ + x³ + x² + 1"),
            "8": ("111010101", "x⁸ + x⁷ + x⁶ + x⁴ + x² + 1"),
            "9": ("101110000101", "x¹¹ + x⁸ + x⁷ + x⁶ + x² + 1"),
            "10": ("11000000000000101", "x¹⁶ + x¹⁵ + x² + 1"),  
            "11": ("10011", "x⁴ + x + 1")
        }
        self.crc_result = ""


        self.__init_ui()
        self.__add_ui()
        self.__connect_signals()



    def __init_ui(self):
        self.v_box: QVBoxLayout = QVBoxLayout()

        self.grid_settings: QGridLayout = QGridLayout()
        self.grid_button: QGridLayout = QGridLayout()

        self.select_coder: QComboBox = QComboBox()
        self.select_coder.addItems(["кодирование методом Шаннона-Фано", "кодирование методом Хаффмана"])
        self.switch_ch_bl: QSwitchControl = QSwitchControl(active_color="#20B2AA")
        self.switch_coder_decoder: QSwitchControl = QSwitchControl(active_color="#20B2AA")

        self.select_crc_generator: QComboBox = QComboBox()
        self.output_crc_generator: QLabel = QLabel("")
        self.select_crc_generator.addItem("Без ЦИК", "1")
        for key, (bits, poly) in self.GENERATORS.items():
            self.select_crc_generator.addItem(f"{poly}", bits)

        self.input_msg: QTextEdit = QTextEdit()
        self.input_msg.setPlaceholderText("Ввод сообщения")
        self.output_msg: QTextEdit = QTextEdit()
        self.output_msg.setPlaceholderText("Вывод закодированного сообщения")
        self.output_msg.setReadOnly(True)

        self.code_decode_button: QPushButton = QPushButton("Кодировать")
        self.show_table: QPushButton = QPushButton("Вывод таблицы")
        # self.save_result: QPushButton = QPushButton("Сохранить")
        # self.load_result: QPushButton = QPushButton("Загрузить")
        self.clear_button: QPushButton = QPushButton("Очистить")


    def __add_ui(self):
        self.v_box.addWidget(self.select_coder)

        self.grid_settings.addWidget(QLabel("Посимвольное кодирование"), 0, 0)
        self.grid_settings.addWidget(self.switch_ch_bl, 0, 1)
        self.grid_settings.addWidget(QLabel("Поблочное кодирование"), 0, 2)

        self.grid_settings.addWidget(QLabel("кодирование"), 1, 0)
        self.grid_settings.addWidget(self.switch_coder_decoder, 1, 1)
        self.grid_settings.addWidget(QLabel("декодирование"), 1, 2)
        self.v_box.addLayout(self.grid_settings)

        self.v_box.addWidget(self.select_crc_generator)
        self.v_box.addWidget(self.output_crc_generator)

        self.v_box.addWidget(self.input_msg)
        self.v_box.addWidget(self.output_msg)

        self.grid_button.addWidget(self.code_decode_button, 0, 0)
        self.grid_button.addWidget(self.show_table, 0, 1)
        # self.grid_button.addWidget(self.save_result, 1, 0)
        # self.grid_button.addWidget(self.load_result, 1, 1)
        self.grid_button.addWidget(self.clear_button, 2, 0, 2, 0)

        self.v_box.addLayout(self.grid_button)
        self.setLayout(self.v_box)


    def __connect_signals(self):
        self.switch_coder_decoder.stateChanged.connect(self.check_box_changed_state)

        self.code_decode_button.clicked.connect(self.coder_decoder)

        self.select_crc_generator.currentIndexChanged.connect(self.check_selected_verify)

        self.clear_button.clicked.connect(self.output_msg.clear)
        self.clear_button.clicked.connect(self.input_msg.clear)

        self.show_table.clicked.connect(self.showTable)



    # смена контекста при смене
    def check_box_changed_state(self, state):
        self.select_crc_generator.setHidden(state)
        self.output_crc_generator.setHidden(not state)
        self.output_crc_generator.setText(self.select_crc_generator.currentText())

        if not state:
            self.output_msg.setPlaceholderText("Вывод закодированного сообщения")
            self.code_decode_button.setText("Кодировать")
            return
        self.output_msg.setPlaceholderText("Вывод декодированного сообщения")
        self.code_decode_button.setText("Декодировать")
        # вывод и ввод поменяю местами что бы было не надо было вводить данные вручную
        self.input_msg.setText(self.output_msg.toPlainText())
        self.output_msg.clear()


    def check_selected_verify(self, index):
        if index == 0 and len(self.code_table.table) != 0:
            QMessageBox.warning(None, "Предупреждение", "Состояние переменных что на данный момент у вас имеется закодированы без ЦИК, рекомендуется перезакодировать значения!")


    # кодирование и декодирование, а так же вывод результатов
    def coder_decoder(self):
        input_data: str = self.input_msg.toPlainText()
        if len(input_data) == 0:
            QMessageBox.warning(None, "Предупреждение", f"Введите хотя бы один символ для {'кодирования' if self.select_coder.currentIndex() == 0 else 'декодирования'}")
            return

        # если кодируем
        if self.switch_coder_decoder.checkState() == Qt.CheckState.Unchecked:
            findPatternFunction = CharPatternFinder if self.switch_ch_bl.checkState() == Qt.CheckState.Unchecked else BlockPatternFinder
            if self.select_coder.currentIndex() == 0:
                self.code_table = ShannonFano(findPatternFunction(input_data))
            else:
                self.code_table, self.table = Huffman(findPatternFunction(input_data))

            code = coder_decoder(self.code_table, input_data)
            self.code_table.crc_gen = self.select_crc_generator.currentData()
            crc = calculate_crc_value( code,self.select_crc_generator.currentData() )
            self.output_msg.setText(code + crc)
        else:
            if self.select_crc_generator.currentIndex() != 0:
                gen = self.code_table.crc_gen
                if not verify_crc_for_bits(input_data, gen):
                    QMessageBox.warning(None, "Предупреждение", "Конечный результат проверки ЦИК вывел ошибки, сообщение передано с ошибками")
                else:
                    QMessageBox.information(None, "Успех", "Провека ЦИК корректна, сообщение передано без ошибок")

                self.output_msg.setText( coder_decoder(self.code_table, input_data[:-(len(gen) - 1)], decode_mode=True) )
            else:
                self.output_msg.setText( coder_decoder(self.code_table, input_data, decode_mode=True) )



    def showTable(self):
        child_window: QDialog = QDialog(self)
        child_window.resize(500, 300)
        dialog_layout: QVBoxLayout = QVBoxLayout()
        table_view: QTableWidget = QTableWidget()

        # строим таблицу для фано
        if self.select_coder.currentIndex() == 0:
            table = []

            table.append(["xi", "Pi"] + \
                    [i+1 for i in range(0, len(sorted(self.code_table.toDict().values(), key=lambda x: len(x), reverse=True)[0]))] + \
                    ["qi", "Pi*qi", "Pi*log(Pi)"])

            max_code_length = len(sorted(self.code_table.toDict().values(), key=lambda x: len(x), reverse=True)[0])
            sum_pi_log = 0.0
            sum_pi_qi = 0.0

            for i in self.code_table.table:
                sum_pi_log += -i.frequency*math.log2(i.frequency)
                sum_pi_qi += i.frequency*len(i.code)
                table.append(  [i.char, i.frequency] + \
                        [i.code[j] if j < len(i.code) else " " for j in range(max_code_length)] + \
                        [len(i.code), i.frequency*len(i.code), -i.frequency*math.log2(i.frequency)])
            table.append(["Сумма"] + [" " for i in range(len(table[0]) - 3)] + [sum_pi_qi, sum_pi_log])

            table_view.setRowCount(len(table))
            table_view.setColumnCount(len(table[0]))
            table_view.setHorizontalHeaderLabels( list(map(str, table[0])) )

            for i in range(1, len(table)):
                for j in range(len(table[i])):
                    table_view.setItem(i-1, j, QTableWidgetItem(str(table[i][j])))

        if self.select_coder.currentIndex() == 1:
            table_data = []
            table_data.append(["Символ", "Pi"] * len(self.table) + ["коды", "qi", "Pi*qi", "-Pi*log(Pi)"])
            
            t = self.table[0]

            for i in range(len(self.table)):
                table_data.append([])
                for j in range(len(self.table[i])):
                    table_data[-1].append(f"\"{self.table[j][i][0]}\"")
                    table_data[-1].append(self.table[j][i][1])
                table_data[-1] += [None, None] * (len(self.table) - len(self.table[i]))

                code = self.code_table.toDict()[t[i][0]]
                table_data[-1].append(code)
                frequency = t[i][1]
                table_data[-1].append(len(code))
                table_data[-1].append(frequency * len(code))
                table_data[-1].append(-frequency * math.log2(frequency))

            table_view.setRowCount(len(table_data))
            table_view.setColumnCount(len(table_data[0]))
            table_view.setHorizontalHeaderLabels(table_data[0])

            for i in range(1, len(table_data)):
                for j in range(len(table_data[i])):
                    if table_data[i][j] != None:
                        table_view.setItem(i-1, j, QTableWidgetItem(str(table_data[i][j])))
                    else:
                        table_view.setItem(i-1, j, QTableWidgetItem(' '))

        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()
        table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        dialog_layout.addWidget(table_view)
        child_window.setLayout(dialog_layout)
        child_window.show()
