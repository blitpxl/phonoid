from PyQt5.QtCore import QRunnable, QObject, pyqtSignal
from .avlc import AudioPlayer, MediaEvent
from .util import get_files


class Signals(QObject):
    scanned = pyqtSignal(object)


class LibraryScanner(QRunnable):
    def __init__(self, player: AudioPlayer, scanPath: str):
        super(LibraryScanner, self).__init__()
        self.signal = Signals()
        self.scanPath = scanPath
        self.audioPlayer = player

    def run(self) -> None:
        for file in get_files(self.scanPath, [".mp3"]):
            self.audioPlayer.add_local_media(file)
        for media in self.audioPlayer.mediaList:
            media.connect_event(MediaEvent.Parsed, lambda x: self.signal.scanned.emit(x))
            media.parse()
