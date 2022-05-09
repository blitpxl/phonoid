from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .uilib.util import mask_image_circ, shadowify
from .uilib.flowlayout import FlowLayout
from .uilib.window import Dialog, DialogContainer
from typing import Union


class ItemContainer(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(ItemContainer, self).__init__()
        self.setParent(parent)
        self.setWidgetResizable(True)
        self.setObjectName("item-container")

        self.widgetContainer = QtWidgets.QWidget()
        self.widgetContainer.setObjectName("widget-container")
        self.verticalScrollBar().setObjectName("vertical-scrollbar")
        self.widgetLayout = FlowLayout(self.widgetContainer)    # apply the flow layout to the widget container
        self.setWidget(self.widgetContainer)
        self.widgetLayout.setSpacing(32)

    def addItem(self, item):
        self.widgetLayout.addWidget(item)


class Page(QtWidgets.QWidget):
    def __init__(self, p, pageTitle):
        super(Page, self).__init__(p)
        self.setObjectName("page")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(30, 30, 8, 8)
        self.pageTitle = QtWidgets.QLabel(pageTitle, self)
        self.pageTitle.setObjectName("page-title")
        self.line = QtWidgets.QFrame(self)
        self.line.setFixedSize(150, 1)
        self.line.setObjectName("line-separator")
        self.vlay.addWidget(self.pageTitle, alignment=Qt.AlignLeft | Qt.AlignTop, stretch=-1)
        self.vlay.addWidget(self.line, alignment=Qt.AlignLeft | Qt.AlignTop, stretch=-1)
        self.vlay.addSpacing(25)


class EmptyLibrary(QtWidgets.QWidget):
    def __init__(self, p):
        super(EmptyLibrary, self).__init__(p)
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setAlignment(Qt.AlignCenter)
        self.vlay.setSpacing(25)
        self.vlay.setContentsMargins(0, 0, 30, 0)
        self.message = QtWidgets.QLabel("You haven't added any music yet.")
        self.message.setObjectName("empty-message")
        self.addButton = QtWidgets.QPushButton(QIcon("res/icons/add.svg"), "Add", self)
        self.addButton.setIconSize(QSize(24, 24))
        self.addButton.setFixedSize(108, 28)
        self.addButton.setObjectName("library-add")
        self.tipMessage = QtWidgets.QLabel("or go to settings -> path to auto scan your music")
        self.tipMessage.setObjectName("tip-message")
        self.vlay.addWidget(self.message, alignment=Qt.AlignCenter)
        self.vlay.addWidget(self.addButton, alignment=Qt.AlignCenter)
        self.vlay.addWidget(self.tipMessage, alignment=Qt.AlignCenter)


class LibraryPage(Page):
    def __init__(self, p, pageTitle):
        super(LibraryPage, self).__init__(p, pageTitle)
        self.emptyLibraryPrompt = EmptyLibrary(self)
        self.trackContainer = None
        self.vlay.addWidget(self.emptyLibraryPrompt, stretch=1)

    def closeEmptyPrompt(self):
        self.vlay.removeWidget(self.emptyLibraryPrompt)
        del self.emptyLibraryPrompt
        self.trackContainer = ItemContainer(self)
        self.vlay.addWidget(self.trackContainer)


class EmptyPlaylist(QtWidgets.QWidget):
    def __init__(self, p):
        super(EmptyPlaylist, self).__init__(p)
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setAlignment(Qt.AlignCenter)
        self.vlay.setSpacing(25)
        self.vlay.setContentsMargins(0, 0, 30, 0)
        self.message = QtWidgets.QLabel("You haven't created any playlist yet.")
        self.message.setObjectName("empty-message")
        self.addButton = QtWidgets.QPushButton(QIcon("res/icons/add.svg"), "Create", self)
        self.addButton.setIconSize(QSize(24, 24))
        self.addButton.setFixedSize(108, 28)
        self.addButton.setObjectName("library-add")
        self.vlay.addWidget(self.message, alignment=Qt.AlignCenter)
        self.vlay.addWidget(self.addButton, alignment=Qt.AlignCenter)


class CreatePlaylistDialog(Dialog):
    def __init__(self, p):
        super(CreatePlaylistDialog, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout()
        self.input_lay = QtWidgets.QVBoxLayout()
        self.cover_button_lay = QtWidgets.QVBoxLayout()

        self.addCoverButton = QtWidgets.QPushButton(self)
        self.addCoverButton.setIcon(QIcon("res/icons/create_playlist_add_cover.svg"))
        self.addCoverButton.setFixedSize(128, 128)
        self.addCoverButton.setIconSize(QSize(32, 32))
        self.addCoverButton.setObjectName("add-cover")

        self.addCoverLabel = QtWidgets.QLabel("Add a cover image\n(optional)")
        self.addCoverLabel.setAlignment(Qt.AlignCenter)

        self.playlistName = QtWidgets.QLineEdit(self)
        self.playlistName.setPlaceholderText("Give this playlist a name")
        self.playlistDesc = QtWidgets.QTextEdit(self)
        self.playlistDesc.setPlaceholderText("Give this playlist a description (optional)")
        shadowify(self.addCoverButton)
        shadowify(self.playlistName)
        shadowify(self.playlistDesc)

        self.input_lay.addWidget(self.playlistName)
        self.input_lay.addSpacing(10)
        self.input_lay.addWidget(self.playlistDesc)
        self.cover_button_lay.addWidget(self.addCoverButton, alignment=Qt.AlignHCenter)
        self.hlay.addLayout(self.cover_button_lay)
        self.hlay.addSpacing(25)
        self.hlay.addLayout(self.input_lay)
        self.mainLayout.addLayout(self.hlay)
        self.dialogButtonLayout.addWidget(self.addCoverLabel, alignment=Qt.AlignLeft)
        self.showDialogButtons()


class PlaylistPage(Page):
    def __init__(self, p, pageTitle):
        super(PlaylistPage, self).__init__(p, pageTitle)
        self.emptyPlaylistPrompt = EmptyPlaylist(self)
        self.playlistContainer: Union[ItemContainer, None] = None
        self.vlay.addWidget(self.emptyPlaylistPrompt, stretch=1)

    def closeEmptyPrompt(self):
        self.vlay.removeWidget(self.emptyPlaylistPrompt)
        del self.emptyPlaylistPrompt
        self.playlistContainer = ItemContainer(self)
        self.vlay.addWidget(self.playlistContainer)


class Favourite(Page):
    def __init__(self, p, pageTitle):
        super(Favourite, self).__init__(p, pageTitle)


class History(Page):
    def __init__(self, p, pageTitle):
        super(History, self).__init__(p, pageTitle)


class Settings(Page):
    def __init__(self, p, pageTitle):
        super(Settings, self).__init__(p, pageTitle)
