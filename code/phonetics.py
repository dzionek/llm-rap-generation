# -*- coding: utf-8 -*-
import eng_to_ipa as ipa

def is_vow(character):
    '''
    Is the given (lowercase) character a vowel or not.
    '''
    #ipa_vowels = "iɪeɛæuʊoɔɑəʌ"
    ipa_vowels = "yøœɶɒɔoʊuʉiɪeɛæaɐɑʌɤɯɨɜ"
    return character in ipa_vowels

def is_space(character):
    '''
    Is the given character a space or newline (other space characters are 
    cleaned in the preprocessing phase).
    '''
    return character==' ' or character=='\n'

def get_phonetic_transcription(lyrics):
    lines = lyrics.splitlines()
    phonetic_lines = [ipa.convert(line) for line in lines]
    phonetic = "\n".join(phonetic_lines)

    return phonetic
