import pickle
from typing import List

class UserLikedSongs:
    def __init__(self, filename: str):
        self.filename = filename
        self.liked_song_ids: List[str] = self.load()

    def add_song(self, song_id: str):
        if song_id not in self.liked_song_ids:
            self.liked_song_ids.append(song_id)
            self.save()

    def remove_song(self, song_id: str):
        if song_id in self.liked_song_ids:
            self.liked_song_ids.remove(song_id)
            self.save()

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.liked_song_ids, f)

    def load(self) -> List[str]:
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []
