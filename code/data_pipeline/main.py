import argparse

from pipeline import Pipeline

parser = argparse.ArgumentParser(
    description='Scraps Genius to get lyrics for artists from a file')

parser.add_argument('api_token')
parser.add_argument('filename')
parser.add_argument('-i', '--ignore_duplicates', action='store_true')
parser.add_argument('-m', '--max_songs_per_artist', action='store')

args = parser.parse_args()
Pipeline(args).process()