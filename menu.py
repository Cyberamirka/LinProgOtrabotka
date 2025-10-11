from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal, Qt, QSize


class Menu (QFrame):
    changeViewSignal = pyqtSignal(int)

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)

        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)

        self.v_box: QVBoxLayout = QVBoxLayout()
        self.button_list: list[QPushButton] = []

        self.title: QLabel = QLabel("MENU")
        self.v_box.addWidget(self.title, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.title.setFixedHeight(20)

        self.setLayout(self.v_box)
        self.setMaximumSize(180, 1000)



    def addItem(self, ButtonStr: str):
        adding_button: QPushButton = QPushButton(ButtonStr)
        button_index = len(self.button_list)

        adding_button.clicked.connect(lambda checked, idx=button_index: self.__onButtonClicked(idx))
        self.button_list.append(adding_button)
        self.v_box.addWidget(adding_button, 0, Qt.AlignmentFlag.AlignCenter)
        self.adjustSize()
        self.v_box.update()


    def __onButtonClicked(self, index: int):
        self.changeViewSignal.emit(index)
