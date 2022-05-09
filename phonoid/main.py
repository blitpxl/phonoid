from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui.uilib.window import WindowContainer
from ui.MainWindow import MainWindow
import sys


class App(MainWindow):
    def __init__(self, p):
        super().__init__(p)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("JetBrains Mono"))
    wcon = WindowContainer(window=App)
    wcon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
