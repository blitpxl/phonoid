from .ui.mainwindow import MainWindow
from .ui.widgets import TrackItem
from .ui.uilib.util import mask_image_circ
from .avlc import AudioPlayer, AudioPlayerEvent
from .avlc.util import ms2min
from .scanner import LibraryScanner
from pathlib import Path
from PyQt5.QtCore import QThreadPool


class Application(MainWindow):
    def __init__(self, p):
        super(Application, self).__init__(p)
        self.audioPlayer = AudioPlayer()
        self.threadPool = QThreadPool(self)
        self.libraryPage.closeEmptyPrompt()
        self.scan_library()

    def update_time(self, m):
        self.playerPanelLayout.timeFrame.time.setText(
            f"{ms2min(self.audioPlayer.get_position())}/{ms2min(m.duration)}")

    def updatePlayerPanel(self, media):
        self.playerPanelLayout.seekbarFrame.seekbar.setValue(self.audioPlayer.get_position())
        self.playerPanelLayout.timeFrame.time.setText(f"{ms2min(self.audioPlayer.get_position())}"
                                                      f"/{ms2min(media.duration)}")

    def on_track_play(self, media):
        self.audioPlayer.play(self.audioPlayer.mediaList.index(media))
        self.audioPlayer.set_volume(50)
        self.playerPanelLayout.playerInfoFrame.coverArt.setPixmap(mask_image_circ(media.art, size=58))
        self.playerPanelLayout.playerInfoFrame.trackTitle.setText(media.title)
        self.playerPanelLayout.playerInfoFrame.trackArtist.setText(media.artist)
        self.playerPanelLayout.seekbarFrame.seekbar.setRange(0, media.duration)
        self.audioPlayer.connect_event(AudioPlayerEvent.PositionChanged, lambda: self.updatePlayerPanel(media))

    def add_track(self, media):
        item = TrackItem(self, media)
        item.onPlay.connect(self.on_track_play)
        self.libraryPage.trackContainer.addItem(item)

    def scan_library(self):
        scanner = LibraryScanner(self.audioPlayer, f"{Path.home()}/Music")
        scanner.signal.scanned.connect(self.add_track)
        self.threadPool.start(scanner)
