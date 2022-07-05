import json
from .avlc import AvlcMedia


def serialize_library(media_list, file_path):
    with open(file_path, "w") as file:
        file.truncate(0)  # wipe the content
        media_list = [media.get_meta_as_dict() for media in media_list]
        json.dump({"library": media_list}, file, indent=2)


def deserialize_library(file_path, vlc_instance):
    result = []
    with open(file_path, "r") as file:
        library = json.load(file)["library"]
        for track in library:
            media = AvlcMedia(None, None, vlc_instance,
                              track["location"],
                              track["type"],
                              track["filename"],
                              track["duration"],
                              track["title"],
                              track["artist"],
                              track["album"],
                              track["art"],
                              track["genre"],
                              track["channel"],
                              track["category"],
                              track["date"]
                              )
            result.append(media)
    return result
