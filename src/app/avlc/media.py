from .event import MediaEvent
from urllib.parse import unquote, urlparse
import threading
import datetime
import vlc
import os


class AvlcMedia:

    pafy_obj = None
    # make the pafy module a singleton and don't import if not needed
    # pafy takes a lot of memory to import, so it will be imported automatically when needed

    def __init__(self, location, media_type, vlcInstance, *args):
        if len(args) == 0:
            self.location = location
            self.mediaType = media_type
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
        else:
            self.location = args[0]
            self.mediaType = args[1]
            self.filename = args[2]
            self.duration = args[3]
            self.title = args[4]
            self.artist = args[5]
            self.album = args[6]
            self.art = args[7]
            self.genre = args[8]
            self.channel = args[9]
            self.category = args[10]
            self.dateAdded = args[11]

        if self.mediaType == "local":
            self.vlcMediaObject = vlcInstance.media_new(self.location)
        else:
            self._import_pafy()
            self.p = self._get_pafy().new(self.location)
            import pafy
            a = self.p.getbest()
            self.vlcMediaObject = vlcInstance.media_new(a.url)

    def get_meta_as_dict(self):
        return {
            "location": self.location,
            "type": self.mediaType,
            "filename": self.filename,
            "duration": self.duration,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "art": self.art,
            "genre": self.genre,
            "channel": self.channel,
            "category": self.category,
            "date": self.dateAdded
        }

    def connect_event(self, event, function):
        if hasattr(event, "functionQueue"):
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
            self.duration = self.vlcMediaObject.get_duration()
            self.art: str = self.vlcMediaObject.get_meta(15)
            if self.art is not None:
                if self.art.startswith("file"):
                    self.art = unquote(urlparse(self.art).path)[1:]
                else:
                    self.art = None
        else:
            self.title = self.p.title
            self.channel = self.p.author
            self.category = self.p.category
            self.duration = self.vlcMediaObject.get_duration()
        MediaEvent.Parsed(self)

    @classmethod
    def _get_pafy(cls):
        return cls.pafy_obj

    @classmethod
    def _import_pafy(cls):
        if cls.pafy_obj is None:
            from pafy import pafy
            cls.pafy_obj = pafy
