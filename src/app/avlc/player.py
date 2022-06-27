from .util import RandomMediaIndexGenerator
from .enums import PlaybackMode, SortMode, SortBy
from .event import AudioPlayerEvent
from .media import AvlcMedia

from operator import attrgetter
from natsort import os_sorted
from typing import Union

import threading
import warnings
import vlc


class AudioPlayer(object):

    # set_lib(get_local_file("dll/libvlc.dll"))

    def __init__(self, *vlcArgs):
        super(AudioPlayer, self).__init__()
        self.vlcInstanceArgs = [*vlcArgs]
        self.vlcInstance = vlc.Instance(self.vlcInstanceArgs)
        self.vlcPlayer = self.vlcInstance.media_player_new()

        self.mediaList = []
        self.currentIndex = 0
        self.playbackMode = PlaybackMode.normal
        self.volumeLimit = 100
        self.isPaused = True
        self.isPlaying = False
        self.mediaIndexGenerator = RandomMediaIndexGenerator()

        self._connect_native_events()  # connect native events
        self.connect_event(AudioPlayerEvent.InstanceReloaded, self._connect_native_events)

    def __del__(self):
        self.cleanup()

    def _connect_native_events(self):
        self.connect_event(AudioPlayerEvent.NI_TrackEndReached, self._on_track_end_reached)
        self.connect_event(AudioPlayerEvent.N_Opening, AudioPlayerEvent.Opening)
        self.connect_event(AudioPlayerEvent.N_Buffering, AudioPlayerEvent.Buffering)
        self.connect_event(AudioPlayerEvent.N_Playing, AudioPlayerEvent.Playing)
        self.connect_event(AudioPlayerEvent.N_Paused, AudioPlayerEvent.Paused)
        self.connect_event(AudioPlayerEvent.N_Stopped, AudioPlayerEvent.Stopped)
        self.connect_event(AudioPlayerEvent.N_Error, AudioPlayerEvent.Error)
        self.connect_event(AudioPlayerEvent.N_PositionChanged, AudioPlayerEvent.PositionChanged)

    def _on_track_end_reached(self):  # called everytime a playlist finished playing
        self.next()
        AudioPlayerEvent.TrackEndReached()

    def _on_playlist_end_reached(self):  # called everytime a song finished playing
        if self.playbackMode == 3:
            self.play(0)
            AudioPlayerEvent.PlaylistEndRepeat()
        else:
            AudioPlayerEvent.PlaylistEndReached()

    # NOTE: Reloading vlcInstance/vlcPlayer will require the user to reconnect the native events (not the avlc events)
    # because the native events were tied to the vlcPlayer. You can listen to AudioPlayerEvent.InstanceReloaded to be
    # notified when the vlcInstance/vlcPlayer is reloaded

    def _reload_instance(self, new_args):               # ====== method to reload vlcInstance and vlcPlayer ======
        self.vlcPlayer.release()                        # delete the player object, which will also stop playback
        self.vlcInstance.release()                      # delete the old vlcInstance
        self.vlcInstance = vlc.Instance(new_args)       # create new vlcInstance with new args passed into it
        self.vlcPlayer = self.vlcInstance.media_player_new()  # create new player object from the new vlcInstance
        AudioPlayerEvent.InstanceReloaded()             # emit signal that the instance finished reloading

    def add_args(self, *vlcArgs):                       # ====== add new args into vlcInstance at runtime ======
        position = self.get_position()                  # remember song position
        playback_rate = self.get_playback_rate()        # remember the playback rate/speed
        self.vlcInstanceArgs += list(vlcArgs)           # add new argument/s to the argument container
        self._reload_instance(self.vlcInstanceArgs)     # reload the vlcInstance and apply the args inside the container
        if self.vlcPlayer.is_playing():
            self.play(self.currentIndex, position)           # continue playing the song from the saved position
        else:
            pass
        self.set_playback_rate(playback_rate)           # reapply the playback rate to the new player

    def remove_args(self, *vlcArgs):                    # does the same thing as above, but this time it's removing the
        position = self.get_position()                  # arguments instead of adding it into the vlcInstance
        playback_rate = self.get_playback_rate()
        for args in vlcArgs:
            self.vlcInstanceArgs.remove(args)
        self._reload_instance(self.vlcInstanceArgs)
        if self.vlcPlayer.is_playing():
            self.play(self.currentIndex, position)
        else:
            pass
        self.set_playback_rate(playback_rate)

    def sort_media_list(self, sortBy=SortBy.filename, sortMode=SortMode.ascending):
        currentPlayingMedia = self.mediaList[self.currentIndex]
        self.mediaList = os_sorted(self.mediaList, key=attrgetter(sortBy), reverse=sortMode)
        self.currentIndex = self.mediaList.index(currentPlayingMedia)
        AudioPlayerEvent.MediaSorted()

    def add_avlc_media(self, avlcmedia):
        self.mediaList.append(avlcmedia)

    def add_local_media(self, uri: str):
        self.mediaList.append(AvlcMedia(uri, "local", self.vlcInstance))
        AudioPlayerEvent.MediaAdded()
        return self

    def add_youtube_media(self, url: str):
        self.mediaList.append(AvlcMedia(url, "youtube", self.vlcInstance))
        AudioPlayerEvent.MediaAdded()
        return self

    def play(self, trackIndex: int = 0, position: int = 0):
        if not trackIndex >= self.get_media_count():
            self.currentIndex = trackIndex
        else:
            msg = f"Track Index out of range ({trackIndex}), Defaulting to 0"
            warnings.warn(msg, RuntimeWarning)
            self.currentIndex = 0
        self.vlcPlayer.set_media(self.mediaList[self.currentIndex].vlcMediaObject)
        self.vlcPlayer.play()
        self.vlcPlayer.set_time(position)
        self.isPaused = False
        self.isPlaying = True
        return self

    def pause(self):
        self.vlcPlayer.pause()
        if self.isPaused:
            self.isPaused = False
        else:
            self.isPaused = True
        return self

    def stop(self):
        self.vlcPlayer.stop()
        self.isPlaying = False
        return self

    def next(self):
        if self.playbackMode == PlaybackMode.normal or self.playbackMode == PlaybackMode.repeatPlaylist:
            if not self.currentIndex + 1 >= self.get_media_count():
                self.currentIndex += 1
                self.play(self.currentIndex)
                AudioPlayerEvent.NextTrack()
            else:
                self._on_playlist_end_reached()
        elif self.playbackMode == PlaybackMode.repeatTrack:
            self.play(self.currentIndex)
            AudioPlayerEvent.NextTrack()
        elif self.playbackMode == PlaybackMode.shuffle:
            randomIndex = self.mediaIndexGenerator(self.get_media_count())
            if randomIndex is None:
                AudioPlayerEvent.PlaylistEndReached()
            else:
                self.play(randomIndex)
            AudioPlayerEvent.NextTrack()
        else:
            msg = f"Invalid playback mode, Resetting playlist position index"
            warnings.warn(msg, RuntimeWarning)
            self.play(0)
            AudioPlayerEvent.NextTrack()
        return self

    def previous(self):
        if not self.currentIndex - 1 < 0:
            self.currentIndex -= 1
            self.play(self.currentIndex)
            AudioPlayerEvent.PrevTrack()
        else:
            pass
        return self

    def set_playback_rate(self, playback_rate: float):
        self.vlcPlayer.set_rate(playback_rate)
        return self

    def set_position(self, position: int):
        self.vlcPlayer.set_time(position)
        return self

    def set_volume(self, value: int):
        if not value > self.volumeLimit:
            self.vlcPlayer.audio_set_volume(value)
        else:
            AudioPlayerEvent.VolumeLimitReached()
        return self

    def set_volume_limit(self, value: int):
        self.volumeLimit = value
        return self

    def set_playback_mode(self, playbackMode: Union[int, PlaybackMode]):
        self.playbackMode = playbackMode
        AudioPlayerEvent.PlaybackModeChanged()
        return self

    def get_playback_rate(self):
        return self.vlcPlayer.get_rate()

    def get_position(self):
        return self.vlcPlayer.get_time()

    def get_length(self):
        return self.vlcPlayer.get_length()

    def get_volume(self):
        return self.vlcPlayer.audio_get_volume()

    def get_volume_limit(self):
        return self.volumeLimit

    def get_media_count(self):
        return len(self.mediaList)

    def connect_event(self, event, function):
        if hasattr(event, "functionQueue"):
            event.connect_callback(function)
        else:  # if the event is from vlc then call it from other thread because libvlc methods is non-reentrant
            def callback_thread(_):
                threading.Thread(target=function).start()
            self.vlcPlayer.event_manager().event_attach(event, callback_thread)
        return self

    def wait(self):
        input()
        self.cleanup()

    def cleanup(self):
        self.vlcPlayer.release()
        for media in self.mediaList:
            media.vlcMediaObject.release()
            del media
        self.vlcInstance.release()
        AudioPlayerEvent.CleanupFinishedEvent()
