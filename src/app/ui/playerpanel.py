from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .widgets import PlayerPanelButton, ScrollableButton, Seekbar
from .uilib.util import mask_image_circ, shadowify, setElide


class PlayerInfoFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(PlayerInfoFrame, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(4, 0, 16, 0)
        self.vlay = QtWidgets.QVBoxLayout()
        self.setFixedSize(208, 64)
        self.setObjectName("player-info-frame")

        self.coverArt = QtWidgets.QLabel(self)
        self.coverArt.setObjectName("player-info-cover-art")
        self.coverArt.setFixedSize(58, 58)
        self.coverArt.setPixmap(mask_image_circ("res/icons/cd.png", imgtype="png", size=58))

        self.trackTitle = QtWidgets.QLabel("----", self)
        self.trackTitle.setObjectName("player-info-track-title")

        self.trackArtist = QtWidgets.QLabel("--", self)
        self.trackArtist.setObjectName("player-info-track-artist")

        self.vlay.addWidget(self.trackTitle)
        self.vlay.addSpacing(-35)
        self.vlay.addWidget(self.trackArtist)

        self.hlay.addWidget(self.coverArt)
        self.hlay.addLayout(self.vlay)

        shadowify(self)

    def setCoverArt(self, coverPath):
        if coverPath is None:
            self.coverArt.setPixmap(mask_image_circ("res/icons/cd.png", imgtype="png", size=58))
        else:
            self.coverArt.setPixmap(mask_image_circ(coverPath, imgtype="jpg", size=58))

    def setTitle(self, trackTitle):
        setElide(self.trackTitle, trackTitle)

    def setArtist(self, trackArtist):
        setElide(self.trackArtist, trackArtist)


class PlayerControllerFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(PlayerControllerFrame, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(8, 0, 8, 0)
        self.hlay.setSpacing(0)
        self.hlay.setAlignment(Qt.AlignCenter)
        self.setFixedSize(168, 34)
        self.setObjectName("player-controller-frame")

        self.previousButton = PlayerPanelButton(16, QIcon("res/icons/skipback.svg"), "", self)
        self.rewind = PlayerPanelButton(16, QIcon("res/icons/rewind.svg"), "", self)
        self.playPause = PlayerPanelButton(24, QIcon("res/icons/play.svg"), "", self)
        self.fastForward = PlayerPanelButton(16, QIcon("res/icons/forward.svg"), "", self)
        self.nextButton = PlayerPanelButton(16, QIcon("res/icons/skipforward.svg"), "", self)

        self.rewind.setAutoRepeat(True)
        self.rewind.setAutoRepeatDelay(500)
        self.rewind.setAutoRepeatInterval(100)

        self.fastForward.setAutoRepeat(True)
        self.fastForward.setAutoRepeatDelay(500)
        self.fastForward.setAutoRepeatInterval(100)

        for button in self.findChildren(QtWidgets.QPushButton):
            button.setFixedSize(30, 30)
            self.hlay.addWidget(button)

        shadowify(self)


class PlaybackControllerFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(PlaybackControllerFrame, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(0, 0, 0, 0)
        self.hlay.setSpacing(0)
        self.hlay.setAlignment(Qt.AlignCenter)
        self.setFixedSize(97, 34)
        self.setObjectName("playback-controller-frame")

        self.volumeButton = ScrollableButton(16, QIcon("res/icons/volume.svg"), "", self)
        self.repeatButton = QtWidgets.QPushButton(QIcon("res/icons/repeat.svg"), "", self)
        self.equalizerButton = QtWidgets.QPushButton(QIcon("res/icons/equalizer.svg"), "", self)

        for button in self.findChildren(QtWidgets.QPushButton):
            button.setIconSize(QSize(16, 16))
            button.setFixedSize(30, 30)
            self.hlay.addWidget(button)

        shadowify(self)


class SeekbarFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(SeekbarFrame, self).__init__(p)
        self.setObjectName("seekbar-frame")
        self.setFixedHeight(25)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(8, 0, 8, 0)
        self.seekbar = Seekbar(self)
        self.seekbar.setOrientation(Qt.Horizontal)
        self.hlay.addWidget(self.seekbar)

        shadowify(self)


class FavouriteFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(FavouriteFrame, self).__init__(p)
        self.setObjectName("favourite-frame")
        self.setFixedSize(34, 34)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(0, 0, 0, 0)
        self.favouriteButton = QtWidgets.QPushButton(QIcon("res/icons/fav-untoggled.svg"), "", self)
        self.favouriteButton.setIconSize(QSize(16, 16))
        self.favouriteButton.setFixedSize(30, 30)
        self.hlay.addWidget(self.favouriteButton)

        shadowify(self)


class TimeFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(TimeFrame, self).__init__(p)
        self.setObjectName("time-frame")
        self.setFixedHeight(34)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.time = QtWidgets.QLabel("--:--/--:--", self)
        self.hlay.addWidget(self.time, alignment=Qt.AlignCenter)

        shadowify(self)


class PlayerPanelLayout(QtWidgets.QHBoxLayout):
    def __init__(self):
        super(PlayerPanelLayout, self).__init__()
        self.setSpacing(10)
        self.bottom_hlay = QtWidgets.QHBoxLayout()
        self.vlay = QtWidgets.QVBoxLayout()

        self.playerInfoFrame = PlayerInfoFrame(self.parent())
        self.playerControllerFrame = PlayerControllerFrame(self.parent())
        self.playbackControllerFrame = PlaybackControllerFrame(self.parent())
        self.seekbarFrame = SeekbarFrame(self.parent())
        self.favouriteFrame = FavouriteFrame(self.parent())
        self.timeFrame = TimeFrame(self.parent())

        self.bottom_hlay.addWidget(self.playerControllerFrame)
        self.bottom_hlay.addWidget(self.playbackControllerFrame)
        self.bottom_hlay.addStretch()
        self.bottom_hlay.addWidget(self.favouriteFrame)
        self.bottom_hlay.addWidget(self.timeFrame)
        self.vlay.addWidget(self.seekbarFrame)
        self.vlay.addLayout(self.bottom_hlay)
        self.addWidget(self.playerInfoFrame)
        self.addLayout(self.vlay)
