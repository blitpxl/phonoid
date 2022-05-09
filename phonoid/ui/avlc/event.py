from vlc import EventType


class AvlcEventObject(object):
    def __init__(self, allowMultipleAssignment: bool = True):
        super(AvlcEventObject, self).__init__()
        self.multipleAssignment = allowMultipleAssignment

        self.callbacks = []
        self.callback = lambda x=None: None

    def __call__(self, *args, **kwargs):
        if self.multipleAssignment:
            if args == ():
                for callback in self.callbacks:
                    callback()
            else:
                for callback in self.callbacks:
                    callback(*args, **kwargs)
        else:
            if args is None:
                self.callback()
            else:
                self.callback(*args, **kwargs)

    def connect_callback(self, callback_fn):
        if self.multipleAssignment:
            self.callbacks.append(callback_fn)
        else:
            self.callback = callback_fn


# =================     Event naming    =================
# NI            =       Native Internal Event
# N             =       Native Event
# No Prefix     =       Avlc Event

# =================     Description     =================
# Native Internal Events:
#           These type of events is used internally within certain objects.
#           For example, the "NI_TrackEndReached" event which is used internally in the AudioPlayer object
#           For notifying the object when a song ends, In this case it will call the function
#           "next()" which will play the next song in playlist. Because a native event can only be connected
#           to a single callback function, you shouldn't use native internal events to call other functions.
# Native Event:
#           These event objects are native to libvlc, which means that you can connect them to only one function.
#           And you should reconnect them everytime the vlcInstance is updated, see "InstanceReloaded" event.
# Avlc Event:
#           These event objects is defined in python rather than libvlc so it is more flexible.
#           You can connect multiple callback functions to them and you can call the event manually.
#           You can even create your own custom event with it by assigning an AvlcEventObject to a variable
#           like this: MyCustomEvent = AvlcEventObject()
#           And you can call them manually like how you would call a function: MyCustomEvent()


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
    TrackEndReached = AvlcEventObject()
    PlaylistEndRepeat = AvlcEventObject()
    PlaylistEndReached = AvlcEventObject()
    NextTrack = AvlcEventObject()
    PrevTrack = AvlcEventObject()
    MediaAdded = AvlcEventObject()
    PlaybackModeChanged = AvlcEventObject()
    VolumeLimitReached = AvlcEventObject()
    CleanupFinishedEvent = AvlcEventObject()
    InstanceReloaded = AvlcEventObject()
    MediaSorted = AvlcEventObject()


class MediaEvent(object):
    NI_Parsed = EventType(3)
    N_DurationChanged = EventType(2)
    Parsed = AvlcEventObject(False)
    ParseFailed = AvlcEventObject(False)


class EqualizerEvent(object):
    EqualizerEnabled = AvlcEventObject()
    EqualizerDisabled = AvlcEventObject()
    Enabled2Pass = AvlcEventObject()
    Disabled2Pass = AvlcEventObject()
