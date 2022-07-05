import time

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal
from os.path import exists
from .avlc import AudioPlayer, MediaEvent
from .util import get_files
from .serializer import deserialize_library


class Signals(QObject):
    scanned = pyqtSignal(object)


class LibraryScanner(QRunnable):
    def __init__(self, player: AudioPlayer, scanPath: str):
        super(LibraryScanner, self).__init__()
        self.signal = Signals()
        self.scanPath = scanPath
        self.audioPlayer = player

    def run(self) -> None:
        if not exists("conf/library.json"):
            for file in get_files(self.scanPath, [".mp3"]):
                self.audioPlayer.add_local_media(file)
            for media in self.audioPlayer.mediaList:
                media.connect_event(MediaEvent.Parsed, lambda med: self.signal.scanned.emit(med))
                media.parse()
        else:
            library = deserialize_library("conf/library.json", self.audioPlayer.vlcInstance)
            for media in library:
                self.audioPlayer.add_avlc_media(media)
                self.signal.scanned.emit(media)
