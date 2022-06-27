from .ui.mainwindow import MainWindow
from .ui.widgets import TrackItem
from .avlc import AudioPlayer, AudioPlayerEvent, AvlcMedia, ms2min
from .scanner import LibraryScanner
from typing import Union
from PyQt5.QtCore import QThreadPool


class Application(MainWindow):
    """
    This is where the application logics are implemented
    """

    def __init__(self, p):
        super(Application, self).__init__(p)
        self.threadPool = QThreadPool(self)
        self.audioPlayer: Union[AudioPlayer, None] = None

        self.init_player()
        self.scan_library()

    def init_player(self):
        self.audioPlayer = AudioPlayer()
        self.audioPlayer.set_volume(50)
        self.audioPlayer.connect_event(AudioPlayerEvent.PositionChanged, self.on_pos_changed)
        self.audioPlayer.connect_event(AudioPlayerEvent.TrackEndReached, self.on_track_changed)

        self.playerPanelLayout.seekbarFrame.seekbar.seek.connect(self.audioPlayer.set_position)
        self.playerPanelLayout.playbackControllerFrame.volumeButton.onValueChanged.connect(self.audioPlayer.set_volume)
        self.playerPanelLayout.playerControllerFrame.playPause.clicked.connect(self.on_play_pause)
        self.playerPanelLayout.playerControllerFrame.nextButton.clicked.connect(self.on_next)
        self.playerPanelLayout.playerControllerFrame.previousButton.clicked.connect(self.on_previous)
        self.playerPanelLayout.playerControllerFrame.fastForward.clicked.connect(self.on_fast_forward)
        self.playerPanelLayout.playerControllerFrame.rewind.clicked.connect(self.on_rewind)

    def on_play_pause(self):
        self.audioPlayer.pause()
        if self.audioPlayer.isPaused:
            self.playerPanelLayout.playerControllerFrame.playPause.changeIcon("res/icons/play.svg")
        else:
            self.playerPanelLayout.playerControllerFrame.playPause.changeIcon("res/icons/pause.svg")

    def on_next(self):
        self.audioPlayer.next()
        self.on_track_changed()

    def on_previous(self):
        self.audioPlayer.previous()
        self.on_track_changed()

    def on_fast_forward(self):
        self.audioPlayer.set_position(self.audioPlayer.get_position() + 5000)

    def on_rewind(self):
        self.audioPlayer.set_position(self.audioPlayer.get_position() - 5000)

    def library_add_track(self, media: AvlcMedia):
        track = TrackItem(self, media)
        track.onPlay.connect(self.quick_play)
        self.libraryPage.trackContainer.addItem(track)

    def scan_library(self):
        self.libraryPage.closeEmptyPrompt()
        libraryScanner = LibraryScanner(self.audioPlayer, "C:/Users/Kevin/Music/demo")
        libraryScanner.signal.scanned.connect(self.library_add_track)
        self.threadPool.start(libraryScanner)

    def on_pos_changed(self):
        if not self.isUpdating:
            self.playerPanelLayout.seekbarFrame.seekbar.updatePosition(self.audioPlayer.get_position())
            self.playerPanelLayout.timeFrame.time.setText(
                f"{ms2min(self.audioPlayer.get_position())}/{ms2min(self.audioPlayer.get_length())}"
            )

    def on_track_changed(self):
        media: AvlcMedia = self.audioPlayer.mediaList[self.audioPlayer.currentIndex]
        self.update_player_info(media.art, media.title, media.artist, media.duration)

    # double-click on a track item to quick play
    def quick_play(self, media: AvlcMedia):
        self.audioPlayer.play(self.audioPlayer.mediaList.index(media))
        self.update_player_info(media.art, media.title, media.artist, media.duration)
        self.playerPanelLayout.playerControllerFrame.playPause.changeIcon("res/icons/pause.svg")

    def update_player_info(self, cover, title, artist, duration):
        self.playerPanelLayout.playerInfoFrame.setCoverArt(cover)
        self.playerPanelLayout.playerInfoFrame.setTitle(title)
        self.playerPanelLayout.playerInfoFrame.setArtist(artist)
        self.playerPanelLayout.seekbarFrame.seekbar.setRange(0, duration)
