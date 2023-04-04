import re
from unidecode import unidecode

class LyricsCleaner:
    def __init__(self, lyrics: str):
        self.lyrics = lyrics

    def _clean_lyrics_text(self) -> None:
        found = re.search(r'^.*Lyrics', self.lyrics)
        if found:
            self.lyrics = self.lyrics.replace(found[0], '')

    def _remove_square_brackets(self) -> None:
        pattern = r"\[.*\]"
        brackets = re.findall(pattern, self.lyrics)
        for found in brackets:
            self.lyrics = self.lyrics.replace(found + '\n', '')
            self.lyrics = self.lyrics.replace('\n' + found, '')

    def _replace_special_characters(self) -> None:
        self.lyrics = self.lyrics.replace('\u00A0', '')
        self.lyrics = self.lyrics.replace('\u200f', '')
        self.lyrics = self.lyrics.replace('\u200b', '')
        self.lyrics = self.lyrics.replace('<br/>', '\n')
        self.lyrics = self.lyrics.replace('’', "'")
        self.lyrics = unidecode(self.lyrics)

    def _replace_final_embed(self) -> None:
        found = re.findall(r'(?<=\D)\d.*Embed', self.lyrics)
        if found:
            self.lyrics = self.lyrics.replace(found[-1], '')

    def _replace_added_text(self) -> None:
        self.lyrics = self.lyrics.replace('You might also like', '')

    def clean(self) -> str:
        self._clean_lyrics_text()
        self._remove_square_brackets()
        self._replace_special_characters()
        self._replace_final_embed()
        self._replace_added_text()
        return self.lyrics
