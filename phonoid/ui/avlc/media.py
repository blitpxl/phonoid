from .event import MediaEvent
import threading
import datetime
import vlc
import os


class AvlcMedia(object):

    pafy_obj = None

    def __init__(self, location, mediaType, vlcInstance):
        self.location = location
        self.mediaType = mediaType
        self.filename = os.path.basename(os.path.splitext(location)[0])
        self.duration = None
        self.title = None
        self.artist = None
        self.album = None
        self.art = None
        self.genre = None
        self.channel = None
        self.category = None
        self.dateAdded = datetime.datetime.now().timestamp()

        if mediaType == "local":
            self.vlcMediaObject = vlcInstance.media_new(location)
        else:
            self._import_pafy()
            self.p = self._get_pafy().new(location)
            a = self.p.getbestaudio()
            self.vlcMediaObject = vlcInstance.media_new(a.url)

    def connect_event(self, event, function):
        if hasattr(event, "callbacks"):
            event.connect_callback(function)
        else:
            def callback_thread(_):
                threading.Thread(target=function).start()
            self.vlcMediaObject.event_manager().event_attach(event, callback_thread)

    def parse(self):
        self.vlcMediaObject.parse_with_options(vlc.MediaParseFlag(0x1), -1)
        self.connect_event(MediaEvent.NI_Parsed, self._on_parsed_done)

    def _on_parsed_done(self):
        if str(self.vlcMediaObject.get_parsed_status()) != "MediaParsedStatus.FIXME_(0)":
            self._set_meta()
        else:
            MediaEvent.ParseFailed(self)

    def _set_meta(self):
        if self.mediaType == "local":
            self.title = self.vlcMediaObject.get_meta(0)
            self.artist = self.vlcMediaObject.get_meta(1)
            self.album = self.vlcMediaObject.get_meta(4)
            self.genre = self.vlcMediaObject.get_meta(2)
            self.art = self.vlcMediaObject.get_meta(15)
            self.duration = self.vlcMediaObject.get_duration()
        else:
            self.title = self.p.title
            self.channel = self.p.author
            self.category = self.p.category
            self.duration = self.vlcMediaObject.get_duration()
        MediaEvent.Parsed(
            {
                "location": self.location,
                "filename": self.filename,
                "type": self.mediaType,
                "date": self.dateAdded,
                "title": self.title,
                "artist": self.artist,
                "album": self.album,
                "art": self.art,
                "genre": self.genre,
                "duration": self.duration,
                "channel": self.channel,
                "category": self.category
            }
        )

    @classmethod
    def _get_pafy(cls):
        return cls.pafy_obj

    @classmethod
    def _import_pafy(cls):
        if cls.pafy_obj is None:
            from pafy import pafy
            cls.pafy_obj = pafy
