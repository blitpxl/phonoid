from vlc import EventType
from .util import hasparam


class AvlcEvent:
    def __init__(self, onefunc: bool = False):
        super(AvlcEvent, self).__init__()
        self.isOneFunc = onefunc
        self.functionQueue = []
        self.oneFunction = lambda x=None: ...   # placeholder when there's no one function connected

    def __call__(self, *args, **kwargs):
        if not self.isOneFunc:
            for function in self.functionQueue:
                function(*args, **kwargs)
        else:
            self.oneFunction(*args, **kwargs)

    def connect_callback(self, func):
        if not self.isOneFunc:
            self.functionQueue.append(func)
        else:
            self.oneFunction = func


class AudioPlayerEvent(object):
    NI_TrackEndReached = EventType(265)
    N_Opening = EventType(258)
    N_Buffering = EventType(259)
    N_Playing = EventType(260)
    N_Paused = EventType(261)
    N_Stopped = EventType(262)
    N_Error = EventType(266)
    N_VolumeChanged = EventType(283)
    N_PositionChanged = EventType(267)
    Opening = AvlcEvent()
    Buffering = AvlcEvent()
    Playing = AvlcEvent()
    Paused = AvlcEvent()
    Stopped = AvlcEvent()
    Error = AvlcEvent()
    VolumeChanged = AvlcEvent()
    PositionChanged = AvlcEvent()
    TrackEndReached = AvlcEvent()
    PlaylistEndRepeat = AvlcEvent()
    PlaylistEndReached = AvlcEvent()
    NextTrack = AvlcEvent()
    PrevTrack = AvlcEvent()
    MediaAdded = AvlcEvent()
    PlaybackModeChanged = AvlcEvent()
    VolumeLimitReached = AvlcEvent()
    CleanupFinishedEvent = AvlcEvent()
    InstanceReloaded = AvlcEvent()
    MediaSorted = AvlcEvent()


class MediaEvent(object):
    NI_Parsed = EventType(3)
    N_DurationChanged = EventType(2)
    Parsed = AvlcEvent(True)
    ParseFailed = AvlcEvent(True)


class EqualizerEvent(object):
    EqualizerEnabled = AvlcEvent()
    EqualizerDisabled = AvlcEvent()
    Enabled2Pass = AvlcEvent()
    Disabled2Pass = AvlcEvent()
