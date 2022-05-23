from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QVariantAnimation, QEasingCurve
from .uilib.flowlayout import FlowLayout
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
        self.widgetLayout = FlowLayout(self.widgetContainer)  # apply the flow layout to the widget container
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
        self.opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.opacity.setEnabled(False)
        self.setGraphicsEffect(self.opacity)

        self.inTransition = QVariantAnimation(self)
        self.inTransition.setEasingCurve(QEasingCurve.OutCubic)
        self.inTransition.setDuration(250)
        self.inTransition.setStartValue(0.0)
        self.inTransition.setEndValue(1.0)
        self.inTransition.valueChanged.connect(self.opacity.setOpacity)
        self.inTransition.finished.connect(lambda: self.opacity.setEnabled(False))
        self.inTransition.start()

    def showEvent(self, a0) -> None:
        self.opacity.setEnabled(True)
        self.inTransition.start()


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


class EmptyFavourite(QtWidgets.QWidget):
    def __init__(self, p):
        super(EmptyFavourite, self).__init__(p)
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setAlignment(Qt.AlignCenter)
        self.vlay.setSpacing(25)
        self.vlay.setContentsMargins(0, 0, 30, 0)
        self.message = QtWidgets.QLabel("You haven't favourited any song yet.")
        self.message.setObjectName("empty-message")
        self.tipMessage = QtWidgets.QLabel("press the heart button when a song is playing to add it as favourite")
        self.tipMessage.setObjectName("tip-message")
        self.vlay.addWidget(self.message, alignment=Qt.AlignCenter)
        self.vlay.addWidget(self.tipMessage, alignment=Qt.AlignCenter)


class FavouritePage(Page):
    def __init__(self, p, pageTitle):
        super(FavouritePage, self).__init__(p, pageTitle)
        self.emptyFavouritePrompt = EmptyFavourite(self)
        self.trackContainer = None
        self.vlay.addWidget(self.emptyFavouritePrompt, stretch=1)

    def closeEmptyPrompt(self):
        self.vlay.removeWidget(self.emptyFavouritePrompt)
        del self.emptyFavouritePrompt
        self.trackContainer = ItemContainer(self)
        self.vlay.addWidget(self.trackContainer)


class EmptyHistory(QtWidgets.QWidget):
    def __init__(self, p):
        super(EmptyHistory, self).__init__(p)
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setAlignment(Qt.AlignCenter)
        self.vlay.setSpacing(25)
        self.vlay.setContentsMargins(0, 0, 30, 0)
        self.message = QtWidgets.QLabel("You have no playing history yet.")
        self.message.setObjectName("empty-message")
        self.tipMessage = QtWidgets.QLabel("start playing some track and it will show up here")
        self.tipMessage.setObjectName("tip-message")
        self.vlay.addWidget(self.message, alignment=Qt.AlignCenter)
        self.vlay.addWidget(self.tipMessage, alignment=Qt.AlignCenter)


class HistoryPage(Page):
    def __init__(self, p, pageTitle):
        super(HistoryPage, self).__init__(p, pageTitle)
        self.emptyFavouritePrompt = EmptyHistory(self)
        self.trackContainer = None
        self.vlay.addWidget(self.emptyFavouritePrompt, stretch=1)

    def closeEmptyPrompt(self):
        self.vlay.removeWidget(self.emptyFavouritePrompt)
        del self.emptyFavouritePrompt
        self.trackContainer = ItemContainer(self)
        self.vlay.addWidget(self.trackContainer)


class SettingsPage(Page):
    def __init__(self, p, pageTitle):
        super(SettingsPage, self).__init__(p, pageTitle)
        raise NotImplementedError
