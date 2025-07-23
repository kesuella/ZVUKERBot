# database.py
import sqlite3
from models import AudioTrack

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('music.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT UNIQUE,
                title TEXT,
                artist TEXT,
                album TEXT,
                duration INTEGER
            )
        ''')
        self.connection.commit()

    def add_track(self, track: AudioTrack):
        try:
            self.cursor.execute('''
                INSERT INTO tracks (file_id, title, artist, album, duration)
                VALUES (?, ?, ?, ?, ?)
            ''', (track.file_id, track.title, track.artist, track.album, track.duration))
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass  # Файл уже существует

    def get_track(self, file_id: str):
        self.cursor.execute('SELECT * FROM tracks WHERE file_id = ?', (file_id,))
        row = self.cursor.fetchone()
        if row:
            return AudioTrack(*row[1:])
        return None

    def close_connection(self):
        self.connection.close()
