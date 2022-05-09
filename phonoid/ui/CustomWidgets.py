from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .uilib.util import elide, mask_image_rndcb, shadowify


class TrackItem(QtWidgets.QFrame):
    def __init__(self, p, title="Title", artist="Artist", cover="res/icons/cd.png"):
        super(TrackItem, self).__init__(p)
        self.setFixedSize(128, 170)
        self.setObjectName("track-item")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(0, 0, 0, 0)
        self.vlay.setSpacing(0)

        self.cover = QtWidgets.QLabel(self)
        self.cover.setFixedSize(128, 128)
        self.cover.setPixmap(mask_image_rndcb(cover, size=128, radius=8))

        self.title = QtWidgets.QLabel(self)
        self.title.setObjectName("track-item-title")
        self.title.resize(150, self.title.height())
        self.artist = QtWidgets.QLabel(self)
        self.artist.setObjectName("track-item-artist")
        self.title.resize(150, self.artist.height())
        self.setTitle(title)
        self.setArtist(artist)

        self.vlay.addWidget(self.cover, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.vlay.addWidget(self.title, alignment=Qt.AlignCenter)
        self.vlay.addSpacing(-10)
        self.vlay.addWidget(self.artist, alignment=Qt.AlignCenter)

        shadowify(self)

    def setCover(self, imgpath):
        self.cover.setPixmap(mask_image_rndcb(imgpath, size=128, radius=8))

    def setTitle(self, title):
        elide(self.title, title)
        if "…" in self.title.text():
            self.title.setToolTip(title)

    def setArtist(self, artist):
        elide(self.artist, artist)
        if "…" in self.artist.text():
            self.artist.setToolTip(artist)


class PlaylistItem(QtWidgets.QFrame):
    def __init__(self, p, title, date, desc="", count="--", duration="--:--"):
        super(PlaylistItem, self).__init__(p)
        self.setFixedSize(250, 128)
        self.setObjectName("playlist-item")
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(0, 0, 0, 0)
        self.vlay = QtWidgets.QVBoxLayout()
        self.vlay.setAlignment(Qt.AlignTop)
        self.vlay.setContentsMargins(0, 8, 0, 0)

        self.cover = QtWidgets.QLabel(self)
        self.cover.setFixedSize(128, 128)
        self.cover.setPixmap(mask_image_rndcb("res/icons/cd.png", 128, 8))

        self.title = QtWidgets.QLabel(title, self)
        self.title.setObjectName("playlist-title")

        self.date = QtWidgets.QLabel(date, self)
        self.date.setObjectName("playlist-properties-label")

        self.count = QtWidgets.QLabel(count, self)
        self.count.setObjectName("playlist-properties-label")

        self.duration = QtWidgets.QLabel(duration, self)
        self.duration.setObjectName("playlist-properties-label")

        self.vlay.addWidget(self.title)
        self.vlay.addWidget(self.date)
        self.vlay.addWidget(self.count)
        self.vlay.addWidget(self.duration)

        self.hlay.addWidget(self.cover)
        self.hlay.addSpacing(8)
        self.hlay.addLayout(self.vlay)

        self.setToolTip(desc)
        shadowify(self)

    def setCover(self, imgpath):
        self.cover.setPixmap(mask_image_rndcb(imgpath, size=128, radius=8))

    def setTitle(self, title):
        elide(self.title, title)
        if "…" in self.title.text():
            self.title.setToolTip(title)

    def setCount(self, count):
        elide(self.count, f"{count} tracks")
        if "…" in self.count.text():
            self.count.setToolTip(count)

    def setDuration(self, duration):
        elide(self.duration, f"{duration} long")
        if "…" in self.duration.text():
            self.count.setToolTip(duration)
