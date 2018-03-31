import traceback
from config import last_key
import requests
from bs4 import BeautifulSoup
import urllib.parse
from difflib import SequenceMatcher


last_fm_songs = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={}&api_key={}&format=json&limit=300"
last_fm_popular_artists = "http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={}&api_key={}&format=json"
song_info_url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist={}&song={}"
lyric_url = "http://api.chartlyrics.com/apiv1.asmx/GetLyric?lyricId={}&lyricCheckSum={}"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_popular_artists(country, verbose=False):
    url = last_fm_popular_artists.format(country, last_key)
    if verbose:
        print("Requesting {}".format(url))
    r = requests.get(url)
    return r.json()


def get_songs(artist, verbose=False):
    url = last_fm_songs.format(urllib.parse.quote_plus(artist), last_key)
    if verbose:
        print("Requesting {}".format(url))
    r = requests.get(url)
    return r.json()


def _get_song_info(artist, song, verbose=False):
    url = song_info_url.format(urllib.parse.quote_plus(artist), urllib.parse.quote_plus(song))
    if verbose:
        print("Requesting {}".format(url))
    r = requests.get(url)
    try:
        # pip install lxml
        tree = BeautifulSoup(r.content, "lxml")
        songs = []
        for res in tree.find_all("searchlyricresult"):

            if res.artist and res.lyricid and res.lyricchecksum and res.song:
                songs.append({
                    "lyricid": res.lyricid.string,
                    "lyricchecksum": res.lyricchecksum.string,
                    "artist": res.artist.string,
                    "song": res.song.string
                })
        songs = sorted(songs, key=lambda x: similar(x["artist"], artist) + similar(x["song"], song), reverse=True)
        if len(songs) > 0:
            return songs[0]["lyricid"], songs[0]["lyricchecksum"]
        else:
            return None
    except:
        traceback.print_exc()
        return None


def _get_lyrics(id, hash):
    r = requests.get(lyric_url.format(id, hash))
    try:
        # pip install lxml
        tree = BeautifulSoup(r.content, "lxml")
        return str(tree.getlyricresult.lyric.string)
    except:
        traceback.print_exc()
        return None


def get_lyrics(artist, song, verbose=False):
    id_hash = _get_song_info(artist, song)
    if id_hash:
        lyric = _get_lyrics(id_hash[0], id_hash[1])
        return lyric
    return None


def song_names_clean(artist):
    songs = get_songs(artist)
    if "error" in songs:
        return []
    tracks = songs["toptracks"]["track"]
    total_songs_count = len(tracks)
    if total_songs_count>0:
        max_listeners = int(tracks[0]["listeners"])
        tracks = [t for t in tracks if int(t["listeners"]) > max_listeners*0.125]
        return [track["name"] for track in tracks]
    else:
        return []

