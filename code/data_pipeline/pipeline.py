from argparse import Namespace
from dataclasses import make_dataclass
import os
import sys
import requests
from typing import Optional

from lyricsgenius import Genius
import pandas as pd

from lyrics_cleaner import LyricsCleaner

class Pipeline:
    def __init__(self, args: Namespace):
        self.artist_names_file = args.filename
        self.max_songs_per_artist = int(args.max_songs_per_artist)
        self.ignore_duplicates = args.ignore_duplicates
        self.genius = Genius(args.api_token, sleep_time=1)

    def _get_artist_names(self) -> list[str]:
        if not os.path.isfile(self.artist_names_file):
            print('ERROR: The given file does not exists', file=sys.stderr)
            exit(1)

        with open(self.artist_names_file, 'r') as f:
            return f.readline().split(',')

    @staticmethod
    def _get_file_path(artist_name: str) -> str:
        if not os.path.exists('rappers'):
            os.mkdir('rappers')

        artist_name = artist_name.replace(' ', '_').lower()
        return f'rappers/{artist_name}.csv'

    def _extract_genius(self, artist_name: str) -> Optional[pd.DataFrame]:
        # Will time out if it takes too long, in this case we start again.
        tries = 15
        max_songs = self.max_songs_per_artist
        while True:
            try:
                artist = self.genius.search_artist(
                    artist_name, max_songs=max_songs)
                break
            except requests.exceptions.Timeout:
                print('TIMEOUT: Starting again...', file=sys.stderr)
                tries -= 1
                if tries == 0:
                    tries = 15
                    max_songs = max(1, max_songs//2)

        if artist is None:
            return None
        response = make_dataclass(
            "response", [('artist', str), ('song', str), ('lyrics', str)])
        genius_response = [
            response(artist_name, song.title,
                     LyricsCleaner(song.lyrics).clean())
            for song in artist.songs]
        return pd.DataFrame(genius_response)

    def process(self) -> None:
        artist_names = self._get_artist_names()
        artist_names.reverse()
        number_of_artist = len(artist_names)
        for i, artist_name in enumerate(artist_names):
            print(f'####\nProcessing artist {i+1}/{number_of_artist}\n#####')
            if (self.ignore_duplicates
                    and os.path.isfile(self._get_file_path(artist_name))):
                print(f'Already found a file for {artist_name}. Skipping')
                continue

            df = self._extract_genius(artist_name)
            if df is None:
                continue
            df.to_csv(self._get_file_path(artist_name), mode='w', index=False)
