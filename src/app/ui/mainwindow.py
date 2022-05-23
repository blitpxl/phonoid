from PyQt5 import QtWidgets
from .uilib.window import Window
from .playerpanel import PlayerPanelLayout
from .sidetab import SideTab, SideTabButton
from .pages import Page, LibraryPage, PlaylistPage, FavouritePage, HistoryPage


class MainWindow(Window):
    def __init__(self, p):
        super(MainWindow, self).__init__(p)
        self.titlebar.windowNotch.setTitle("Phonoid")
        self.vlay = QtWidgets.QVBoxLayout(self)  # our main layout
        self.upper_hlay = QtWidgets.QHBoxLayout()
        self.sideTab = SideTab(self)

        self.playerPanelLayout = PlayerPanelLayout()
        self.pageContainer = QtWidgets.QStackedWidget(self)

        self.libraryPage = LibraryPage(self, "Library")
        self.playlistPage = PlaylistPage(self, "Playlist")
        self.favouritePage = FavouritePage(self, "Favourite")
        self.historyPage = HistoryPage(self, "History")

        for page in self.findChildren(Page):
            self.pageContainer.addWidget(page)

        for idx, button in enumerate(self.sideTab.findChildren(SideTabButton)):
            button.setTabIndex(idx)
            button.onClicked.connect(self.pageContainer.setCurrentIndex)

        self.upper_hlay.addWidget(self.sideTab)
        self.upper_hlay.addWidget(self.pageContainer)

        self.vlay.addLayout(self.upper_hlay)
        self.vlay.addLayout(self.playerPanelLayout)
        self.raiseBaseWidget()
