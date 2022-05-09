class PlaybackMode(object):
    normal = 0
    repeatTrack = 1
    shuffle = 2
    repeatPlaylist = 3


class SortMode(object):
    ascending = 0
    descending = 1


class SortBy(object):
    filename = "filename"
    title = "title"
    artist = "artist"
    album = "album"
    duration = "duration"
    dateAdded = "dateAdded"
