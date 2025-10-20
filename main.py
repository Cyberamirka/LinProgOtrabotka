from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QStackedWidget, QLabel
import sys

from menu import Menu
# задачи линейного программирования
from LinProgWidget.LinprogWidget import LinProgWidget
from MatrixMWidget.MatrixGameWidget import MatrixGameWidget
from CoderWidget.CoderWidget import CoderWidget


class MainView (QMainWindow):
    """ Главный класс для отображения информации """
    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)

        # main layout
        self.h_box: QHBoxLayout = QHBoxLayout()


        # create stacked widget
        self.stack_widget: QStackedWidget = QStackedWidget()
        self.stack_widget.addWidget(LinProgWidget())
        self.stack_widget.addWidget(MatrixGameWidget())
        self.stack_widget.addWidget(CoderWidget())


        # create menu
        self.menu = Menu()
        self.menu.addItem("Линейное\nпрограммирование")
        self.menu.addItem("Матричные игры")
        self.menu.addItem("Теория кодирования")
        self.menu.changeViewSignal.connect(self.stack_widget.setCurrentIndex)


        self.h_box.addWidget(self.menu)
        self.h_box.addWidget(self.stack_widget)

        # create and set cerntral widget
        centralWidget = QWidget()
        centralWidget.setLayout(self.h_box)
        self.setCentralWidget(centralWidget)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QFrame#FrameWidget {
            border: 1px solid #cccccc;
            border-radius: 8px;
        }
    """)

    # глобальное изменение шрифта
    font = app.font()
    font.setPointSize(11)
    app.setFont(font)

    
    main_win = MainView()
    main_win.show()
    
    exit(app.exec())
