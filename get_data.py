import requests
from bs4 import BeautifulSoup

last_key = "88208b241c65e6ae5e86acdb1b81996f"
last_fm_songs = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={}&api_key={}&format=json&limit=300"

song_info_url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist={}&song={}"

lyric_url = "http://api.chartlyrics.com/apiv1.asmx/GetLyric?lyricId={}&lyricCheckSum={}"

def get_songs(artist):
    r = requests.get(last_fm_songs.format(artist, last_key))
    return r.json()

def get_song_info(artist, song):
    r = requests.get(song_info_url.format(artist, song))
    try:
        tree = BeautifulSoup(r.content)
        return tree.arrayofsearchlyricresult.lyricid.string, tree.arrayofsearchlyricresult.lyricchecksum.string
    except Exception:
        return None

def get_lyrics(id, hash):
    r = requests.get(lyric_url.format(id, hash))
    try:
        tree = BeautifulSoup(r.content)
        return tree.getlyricresult.lyric.string
    except Exception:
        return None


def song_names_clean(artist):
    songs = get_songs(artist)
    tracks = songs["toptracks"]["track"]
    total_songs_count = len(tracks)
    max_listeners = int(tracks[0]["listeners"])
    tracks = [t for t in tracks if int(t["listeners"]) > max_listeners*0.125]
    return [track["name"] for track in tracks]


artists = ["Radiohead", "Motorama", "linkin park", "nirvana", "lil peep", "kooks", "two door cinema club"]

for artist in artists:
    for song in song_names_clean(artist):
        print(artist + " --- " + song)
        id_hash = get_song_info(artist, song)
        if id_hash:
            lyric = get_lyrics(id_hash[0], id_hash[1])
            print(lyric)