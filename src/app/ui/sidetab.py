from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSignal
from .uilib.util import shadowify


class SideTabButton(QtWidgets.QPushButton):
    onClicked = pyqtSignal(int)
    clicked_ = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(SideTabButton, self).__init__(*args, **kwargs)
        self.setCheckable(True)

    def setTabIndex(self, index):
        self.clicked.connect(lambda: self.onClicked.emit(index))
        self.clicked.connect(lambda: self.clicked_.emit(self))


class SideTab(QtWidgets.QFrame):
    def __init__(self, p):
        super(SideTab, self).__init__(p)
        self.setObjectName("side-tab")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(0, 0, 0, 0)
        self.vlay.setSpacing(2)
        self.setFixedSize(50, 258)

        self.homeButton = SideTabButton(QIcon("res/icons/home.svg"), "", self)
        self.playlistButton = SideTabButton(QIcon("res/icons/playlist.svg"), "", self)
        self.favouriteButton = SideTabButton(QIcon("res/icons/favourite.svg"), "", self)
        self.historyButton = SideTabButton(QIcon("res/icons/history.svg"), "", self)
        self.settingsButton = SideTabButton(QIcon("res/icons/settings.svg"), "", self)

        self.homeButton.setChecked(True)

        for idx, button in enumerate(self.findChildren(SideTabButton)):
            button.setIconSize(QSize(32, 32))
            button.setFixedSize(50, 50)
            button.clicked_.connect(self.tabButtonClicked)
            self.vlay.addWidget(button)

        shadowify(self)

    # called if one of the tab button is clicked
    def tabButtonClicked(self, clicked_button):
        # check the clicked button and uncheck all the other button
        for button in self.findChildren(SideTabButton):
            if button != clicked_button:
                button.setChecked(False)
