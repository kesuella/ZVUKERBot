# models.py
class AudioTrack:
    def __init__(self, file_id, title="", artist="", album="", duration=0):
        self.file_id = file_id
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration

    def to_dict(self):
        return {
            'file_id': self.file_id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration': self.duration
        }
