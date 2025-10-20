from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QFrame, QComboBox, QVBoxLayout, QLabel, QHBoxLayout, QTextEdit, QPushButton, \
    QGridLayout

# user modules
from PyQt6_SwitchControl import SwitchControl as QSwitchControl


class CoderWidget(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setObjectName("FrameWidget")
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)

        self.__init_ui()
        self.__add_ui()
        self.__connect_signals()



    def __init_ui(self):
        self.v_box: QVBoxLayout = QVBoxLayout()

        self.grid_settings: QGridLayout = QGridLayout()
        self.grid_button: QGridLayout = QGridLayout()

        self.select_coder: QComboBox = QComboBox()
        self.select_coder.addItems(["кодирование методом Шаннон-Фано", "кодирование методом Хаффман"])
        self.switch_ch_bl: QSwitchControl = QSwitchControl(active_color="#20B2AA")
        self.switch_coder_decoder: QSwitchControl = QSwitchControl(active_color="#20B2AA")

        self.input_msg: QTextEdit = QTextEdit()
        self.input_msg.setPlaceholderText("Ввод сообщения")
        self.output_msg: QTextEdit = QTextEdit()
        self.output_msg.setPlaceholderText("Вывод закодированного сообщения")
        self.output_msg.setReadOnly(True)

        self.code_decode_button: QPushButton = QPushButton("Кодировать")
        self.show_table: QPushButton = QPushButton("Вывод таблицы")
        self.save_result: QPushButton = QPushButton("Сохранить")
        self.load_result: QPushButton = QPushButton("Загрузить")


    def __add_ui(self):
        self.v_box.addWidget(self.select_coder)

        self.grid_settings.addWidget(QLabel("Посимвольное\nкодирование"), 0, 0)
        self.grid_settings.addWidget(self.switch_ch_bl, 0, 1)
        self.grid_settings.addWidget(QLabel("Поблочное\nкодирование"), 0, 2)

        self.grid_settings.addWidget(QLabel("кодирование"), 1, 0)
        self.grid_settings.addWidget(self.switch_coder_decoder, 1, 1)
        self.grid_settings.addWidget(QLabel("декодирование"), 1, 2)
        self.v_box.addLayout(self.grid_settings)

        self.v_box.addWidget(self.input_msg)
        self.v_box.addWidget(self.output_msg)

        self.grid_button.addWidget(self.code_decode_button, 0, 0)
        self.grid_button.addWidget(self.show_table, 0, 1)
        self.grid_button.addWidget(self.save_result, 1, 0)
        self.grid_button.addWidget(self.load_result, 1, 1)

        self.v_box.addLayout(self.grid_button)
        self.setLayout(self.v_box)



    # смена контекста при смене
    def check_box_changed_state(self, state):
        if not state:
            self.output_msg.setPlaceholderText("Вывод закодированного сообщения")
            self.code_decode_button.setText("Кодировать")
            return
        self.output_msg.setPlaceholderText("Вывод декодированного сообщения")
        self.code_decode_button.setText("Декодировать")




    def __connect_signals(self):
        self.switch_coder_decoder.stateChanged.connect(self.check_box_changed_state)