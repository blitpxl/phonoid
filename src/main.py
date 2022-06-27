from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from app.ui.uilib.window import WindowContainer
from app.app import Application
import sys


class Phonoid(Application):
    def __init__(self, p):
        super().__init__(p)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("JetBrains Mono"))
    wcon = WindowContainer(window=Phonoid)
    wcon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
