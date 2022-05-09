from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from .uilib.window import Window, Dialog, DialogContainer
from .PlayerPanel import PlayerPanelLayout
from .SideTab import SideTab
from .CustomWidgets import PlaylistItem
from .Pages import PlaylistPage, CreatePlaylistDialog


class MainWindow(Window):
    def __init__(self, p):
        super(MainWindow, self).__init__(p)
        self.vlay = QtWidgets.QVBoxLayout(self)  # our main layout
        self.upper_hlay = QtWidgets.QHBoxLayout()

        self.sideTab = SideTab(self)
        self.playerPanelLayout = PlayerPanelLayout()

        self.page = PlaylistPage(self, "Playlist")
        self.page.emptyPlaylistPrompt.addButton.clicked.connect(self.add_item)

        self.upper_hlay.addWidget(self.sideTab)
        self.upper_hlay.addWidget(self.page)

        self.vlay.addLayout(self.upper_hlay)
        self.vlay.addLayout(self.playerPanelLayout)
        self.raiseBaseWidget()

    def add_item(self):
        self.page.closeEmptyPrompt()

        for i in range(8):
            self.page.playlistContainer.addItem(PlaylistItem(self, "test", "test"))
