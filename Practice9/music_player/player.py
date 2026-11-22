
import os
import pygame


class MusicPlayer:

    def __init__(self, music_folder="music"):
        # Initialize music mixer
        pygame.mixer.init()

        self.music_folder = music_folder
        self.playlist = []

        # Current track position
        self.current_index = 0
        self.is_playing = False

        # Find music files automatically
        self.load_playlist()

    def load_playlist(self):
        # Supported audio formats
        supported_formats = (".mp3", ".wav", ".ogg")

        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)

        # Get all music files
        files = os.listdir(self.music_folder)

        self.playlist = [
            file for file in files
            if file.lower().endswith(supported_formats)
        ]

        self.playlist.sort()

        print("Playlist loaded:")
        for song in self.playlist:
            print("-", song)

        if not self.playlist:
            print("No music files found!")

    def play(self):
        if not self.playlist:
            return

        # Load current song
        song_path = os.path.join(
            self.music_folder,
            self.playlist[self.current_index]
        )

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        self.is_playing = True

        print("Playing:", self.get_current_track())

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        print("Music stopped.")

    def next_track(self):
        if not self.playlist:
            return

        self.current_index = (
            self.current_index + 1
        ) % len(self.playlist)

        self.play()

    def previous_track(self):
        if not self.playlist:
            return

        self.current_index = (
            self.current_index - 1
        ) % len(self.playlist)

        self.play()

    def get_current_track(self):
        if not self.playlist:
            return "No tracks available"

        return self.playlist[self.current_index]

    def get_position(self):
        # Get playback position in milliseconds
        if self.is_playing:
            position = pygame.mixer.music.get_pos()

            if position >= 0:
                return position // 1000

        return 0

    def update(self):
        # Automatically play next track
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.next_track()

    def quit(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.is_playing = False
