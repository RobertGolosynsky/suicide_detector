import requests
from bs4 import BeautifulSoup

last_key = "88208b241c65e6ae5e86acdb1b81996f"
last_fm_songs = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={}&api_key={}&format=json&limit=300"
last_fm_popular_artists = "http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={}&api_key={}&format=json"
song_info_url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist={}&song={}"
lyric_url = "http://api.chartlyrics.com/apiv1.asmx/GetLyric?lyricId={}&lyricCheckSum={}"

def get_popular_artists(country):
    r = requests.get(last_fm_popular_artists.format(country, last_key))
    return r.json()

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
def save_in_file(file_name,lyrics):
    try:
        file = open(file_name, "w")
        file.write(lyrics)
        file.close()
    except Exception:
        print("Cannot write the file")
        return

def as_filename(str):
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(c for c in str if c in valid_chars)


def save_songs(artists,location):
    for artist in artists:
        for song in song_names_clean(artist):
            print(artist + " --- " + song)
            id_hash = get_song_info(artist, song)
            if id_hash:
                lyric = get_lyrics(id_hash[0], id_hash[1])
                if lyric:
                    save_in_file("{}/{}-{}.txt".format(location, as_filename(artist), as_filename(song)),
                                 song + '\n' + lyric)


# artists = open("artists.txt", "r").read().split("\n")
# artists += open("bands.txt", "r").read().split("\n")
# save_songs(artists, "suicide")
artists = get_popular_artists("united%20states")["topartists"]["artist"]
artists = [a["name"] for a in artists]
save_songs(artists, "nosuicide")



