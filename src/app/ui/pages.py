import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QVariantAnimation, QEasingCurve, QRunnable, QThreadPool, pyqtSignal, QObject
from .uilib.flowlayout import FlowLayout
from .uilib.util import shadowify
from .widgets import SearchBar
from typing import Union


class SearchSignals(QObject):
    delItemFromLayout = pyqtSignal(object)
    addItemToLayout = pyqtSignal(object)
    hideItem = pyqtSignal(object)
    showItem = pyqtSignal(object)


class ItemContainer(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(ItemContainer, self).__init__()
        self.setParent(parent)
        self.setWidgetResizable(True)
        self.setObjectName("item-container")
        self.items = []

        self.widgetContainer = QtWidgets.QWidget()
        self.widgetContainer.setObjectName("widget-container")
        self.verticalScrollBar().setObjectName("vertical-scrollbar")
        self.widgetLayout = FlowLayout(self.widgetContainer)  # apply the flow layout to the widget container
        self.setWidget(self.widgetContainer)
        self.widgetLayout.setSpacing(32)

    def addItem(self, item):
        self.widgetLayout.addWidget(item)
        self.items.append(item)


class Page(QtWidgets.QWidget):
    def __init__(self, p, title):
        super(Page, self).__init__(p)
        self.setObjectName("page")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(30, 30, 8, 8)
        self.toplay = QtWidgets.QHBoxLayout()
        self.pageTitle = QtWidgets.QLabel(title, self)
        self.pageTitle.setObjectName("page-title")
        self.searchBar = SearchBar(self)
        self.searchBar.setPlaceholderText(f"Search in {title}")
        self.searchBar.textChanged.connect(self.onSearch)
        self.line = QtWidgets.QFrame(self)
        self.line.setFixedSize(150, 1)
        self.line.setObjectName("line-separator")
        self.toplay.addWidget(self.pageTitle)
        self.toplay.addWidget(self.searchBar, alignment=Qt.AlignRight)
        self.vlay.addLayout(self.toplay)
        self.vlay.addWidget(self.line, alignment=Qt.AlignLeft | Qt.AlignTop, stretch=-1)
        self.vlay.addSpacing(25)
        self.opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.opacity.setEnabled(False)
        self.setGraphicsEffect(self.opacity)

        shadowify(self.searchBar)
        self.searchThread = QThreadPool.globalInstance()

        self.inTransition = QVariantAnimation(self)
        self.inTransition.setEasingCurve(QEasingCurve.OutCubic)
        self.inTransition.setDuration(250)
        self.inTransition.setStartValue(0.0)
        self.inTransition.setEndValue(1.0)
        self.inTransition.valueChanged.connect(self.opacity.setOpacity)
        self.inTransition.finished.connect(lambda: self.opacity.setEnabled(False))
        self.inTransition.start()
        self.running_search_thread = None

    # override this to implement searching algorithm
    def onSearch(self, term):
        pass

    def showEvent(self, a0) -> None:
        self.opacity.setEnabled(True)
        self.inTransition.start()
        QtWidgets.QWidget.showEvent(self, a0)


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
        self.trackContainer: Union[ItemContainer, None] = None
        self.vlay.addWidget(self.emptyLibraryPrompt, stretch=1)

    def closeEmptyPrompt(self):
        self.vlay.removeWidget(self.emptyLibraryPrompt)
        del self.emptyLibraryPrompt
        self.trackContainer = ItemContainer(self)
        self.vlay.addWidget(self.trackContainer)

    def onSearch(self, term):
        term = term.lower()

        class SearchTrack(QRunnable):
            items = self.trackContainer.items
            signal = SearchSignals()

            def run(self) -> None:
                if term:
                    for item in self.items:
                        if term in item.searchid:
                            self.signal.showItem.emit(item)
                            self.signal.addItemToLayout.emit(item)
                        else:
                            self.signal.hideItem.emit(item)
                            self.signal.delItemFromLayout.emit(item)
                else:
                    for item in self.items:
                        self.signal.showItem.emit(item)
                        self.signal.addItemToLayout.emit(item)
                        time.sleep(0.01)

        self.running_search_thread = SearchTrack()
        task = self.running_search_thread
        task.signal.showItem.connect(lambda app: app.show())
        task.signal.hideItem.connect(lambda app: app.hide())
        task.signal.addItemToLayout.connect(self.trackContainer.widgetLayout.addWidget)
        task.signal.delItemFromLayout.connect(self.trackContainer.widgetLayout.removeWidget)
        if self.running_search_thread:
            self.searchThread.cancel(self.running_search_thread)
            self.running_search_thread = None
        self.searchThread.start(task)


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
