from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .uilib.util import mask_image_circ, shadowify


class PlayerInfoFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(PlayerInfoFrame, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(4, 0, 0, 0)
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


class PlayerControllerFrame(QtWidgets.QFrame):
    def __init__(self, p):
        super(PlayerControllerFrame, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(8, 0, 8, 0)
        self.hlay.setSpacing(0)
        self.hlay.setAlignment(Qt.AlignCenter)
        self.setFixedSize(168, 34)
        self.setObjectName("player-controller-frame")

        self.skipBack = QtWidgets.QPushButton(QIcon("res/icons/skipback.svg"), "", self)
        self.rewind = QtWidgets.QPushButton(QIcon("res/icons/rewind.svg"), "", self)
        self.playPause = QtWidgets.QPushButton(QIcon("res/icons/play.svg"), "", self)
        self.fastForward = QtWidgets.QPushButton(QIcon("res/icons/forward.svg"), "", self)
        self.skipForward = QtWidgets.QPushButton(QIcon("res/icons/skipforward.svg"), "", self)

        self.skipBack.setIconSize(QSize(16, 16))
        self.rewind.setIconSize(QSize(16, 16))
        self.playPause.setIconSize(QSize(24, 24))
        self.fastForward.setIconSize(QSize(16, 16))
        self.skipForward.setIconSize(QSize(16, 16))

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

        self.volumeButton = QtWidgets.QPushButton(QIcon("res/icons/volume.svg"), "", self)
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
        self.seekbar = QtWidgets.QSlider(self)
        self.seekbar.setOrientation(Qt.Horizontal)
        self.hlay.addWidget(self.seekbar)

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
        self.timeFrame = TimeFrame(self.parent())

        self.bottom_hlay.addWidget(self.playerControllerFrame)
        self.bottom_hlay.addWidget(self.playbackControllerFrame)
        self.bottom_hlay.addWidget(self.timeFrame, alignment=Qt.AlignRight)
        self.vlay.addWidget(self.seekbarFrame)
        self.vlay.addLayout(self.bottom_hlay)
        self.addWidget(self.playerInfoFrame)
        self.addLayout(self.vlay)
