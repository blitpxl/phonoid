from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .uilib.util import shadowify


class SideTab(QtWidgets.QFrame):
    def __init__(self, p):
        super(SideTab, self).__init__(p)
        self.setObjectName("side-tab")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.setFixedSize(50, 258)

        self.homeButton = QtWidgets.QPushButton(QIcon("res/icons/home.svg"), "", self)
        self.playlistButton = QtWidgets.QPushButton(QIcon("res/icons/playlist.svg"), "", self)
        self.favouriteButton = QtWidgets.QPushButton(QIcon("res/icons/favourite.svg"), "", self)
        self.historyButton = QtWidgets.QPushButton(QIcon("res/icons/history.svg"), "", self)
        self.settingsButton = QtWidgets.QPushButton(QIcon("res/icons/settings.svg"), "", self)

        for idx, button in enumerate(self.findChildren(QtWidgets.QPushButton)):
            button.setIconSize(QSize(32, 32))
            self.vlay.addWidget(button)
            if not idx == 4:
                sep = QtWidgets.QFrame(self)
                sep.setFrameShape(QtWidgets.QFrame.HLine)
                sep.setFixedSize(20, 1)
                self.vlay.addWidget(sep, alignment=Qt.AlignCenter)

        shadowify(self)
