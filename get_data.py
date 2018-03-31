import pathlib
import traceback

from api_helpers import song_names_clean, get_lyrics, get_popular_artists
import glob
import os

from config import *
from data_helpers import save_text
from remove_similar_songs import remove_similar_songs


def as_filename(str):
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(c for c in str if c in valid_chars)


def save_songs(artists, location):
    for artist in artists:
        print("Downloading artist: {}".format(artist))
        for song in song_names_clean(artist):
            print(artist + " --- " + song)
            filename = "{}-{}.txt".format(as_filename(artist), as_filename(song))
            downloaded_songs = [os.path.basename(p) for p in glob.glob(os.path.join(location, "*.txt"))]
            if filename in downloaded_songs:
                print("Already saved! Skipping...")
                continue

            lyric = get_lyrics(artist, song)
            if lyric:
                filename = os.path.join(location, filename)
                print("Saving to a file {}".format(filename))
                save_text(filename, lyric)


not_suicidal_as_popular_in_usa = False

artists = open(suicidal_artists_list_file_path, "r").read().split("\n")
artists += open(suicidal_bands_list_file_path, "r").read().split("\n")
artists += open(depressing_bands_list_file_path, "r").read().split("\n")
save_songs(artists, suicidal_folder_path)


artists = get_popular_artists("united%20states")["topartists"]["artist"]
artists += [a["name"] for a in artists]
artists += open(not_suicidal_artists_list_file_path, "r").read().split("\n")
save_songs(artists, not_suicidal_folder_path)
remove_similar_songs()



